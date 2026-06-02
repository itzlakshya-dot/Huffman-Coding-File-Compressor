import heapq
import os
import pickle

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Defining comparators for the priority queue (Min-Heap)
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCompressor:
    def __init__(self):
        self.reverse_mapping = {}

    def _make_frequency_dict(self, text):
        """Step 1: Count character frequencies."""
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def _make_heap(self, frequency):
        """Step 2: Push leaf nodes into a Min-Heap."""
        heap = []
        for key in frequency:
            node = HuffmanNode(key, frequency[key])
            heapq.heappush(heap, node)
        return heap

    def _merge_nodes(self, heap):
        """Step 2 Continued: Combine lowest nodes until one root remains."""
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)

            # Combined internal node (has no character assigned)
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(heap, merged)
        return heap

    def _make_codes_helper(self, root, current_code, codes):
        """Step 3: Recursively traverse tree to generate 0s and 1s codes."""
        if root is None:
            return

        if root.char is not None:
            codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self._make_codes_helper(root.left, current_code + "0", codes)
        self._make_codes_helper(root.right, current_code + "1", codes)

    def _make_codes(self, heap):
        root = heapq.heappop(heap)
        codes = {}
        self._make_codes_helper(root, "", codes)
        return codes

    def _get_encoded_text(self, text, codes):
        """Replaces text characters with their generated binary bitstrings."""
        encoded_text = ""
        for character in text:
            encoded_text += codes[character]
        return encoded_text

    def _pad_encoded_text(self, encoded_text):
        """Files must be read in full bytes (multiples of 8 bits). Add padding if needed."""
        extra_padding = 8 - (len(encoded_text) % 8)
        for i in range(extra_padding):
            encoded_text += "0"

        # Store padding amount in 8 bits format at the very front of the string
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def _get_byte_array(self, padded_encoded_text):
        """Converts strings of '0's and '1's into actual raw, physical bytes."""
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self, input_path):
        """Main entry point to compress a text file."""
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + ".bin"

        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.rstrip()

        if not text:
            print("File is empty!")
            return output_path

        # Generate frequencies and trees
        frequency = self._make_frequency_dict(text)
        heap = self._make_heap(frequency)
        heap = self._merge_nodes(heap)
        codes = self._make_codes(heap)

        encoded_text = self._get_encoded_text(text, codes)
        padded_encoded_text = self._pad_encoded_text(encoded_text)
        bytes_to_write = self._get_byte_array(padded_encoded_text)

        # OPTIMIZATION: Dump the small frequency map instead of the heavy string-bit mapping
        with open(output_path, 'wb') as output:
            pickle.dump(frequency, output)
            output.write(bytes_to_write)

        return output_path

    def _remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def _decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        """Main entry point to decompress a .bin file back to text."""
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed.txt"

        with open(input_path, 'rb') as file:
            # Load the small frequency map back
            frequency = pickle.load(file)
            
            # RECONSTRUCT the exact same mapping tree using the frequencies
            heap = self._make_heap(frequency)
            heap = self._merge_nodes(heap)
            self.reverse_mapping = {}
            self._make_codes(heap) # This repopulates self.reverse_mapping automatically
            
            # Read the remaining raw compressed payload bytes
            bit_string = ""
            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].zfill(8)
                bit_string += bits
                byte = file.read(1)

        encoded_text = self._remove_padding(bit_string)
        decompressed_text = self._decode_text(encoded_text)

        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(decompressed_text)

        return output_path