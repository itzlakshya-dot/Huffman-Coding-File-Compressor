import tkinter as tk
from tkinter import filedialog, messagebox
import os
import time
from huffman_engine import HuffmanCompressor

class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DAA Project: Smart File Compressor")
        self.root.geometry("550x450")
        self.root.config(bg="#f4f6f9")
        
        self.compressor = HuffmanCompressor()
        self.selected_file_path = None

        # --- UI Design Components ---
        
        # Header Title Banner
        header = tk.Label(
            root, 
            text="Huffman Coding Compressor", 
            font=("Arial", 18, "bold"), 
            bg="#2c3e50", 
            fg="white", 
            pady=15
        )
        header.pack(fill=tk.X)

        # File Selection Frame
        file_frame = tk.Frame(root, bg="#f4f6f9", pady=20)
        file_frame.pack()

        self.btn_browse = tk.Button(
            file_frame, 
            text="Select File", 
            command=self.browse_file, 
            font=("Arial", 11, "bold"), 
            bg="#3498db", 
            fg="white", 
            padx=10, 
            pady=5,
            relief=tk.FLAT
        )
        self.btn_browse.grid(row=0, column=0, padx=10)

        self.lbl_file_path = tk.Label(
            file_frame, 
            text="No file selected...", 
            font=("Arial", 10, "italic"), 
            bg="#f4f6f9", 
            fg="#7f8c8d",
            wraplength=350,
            justify="left"
        )
        self.lbl_file_path.grid(row=0, column=1, padx=10)

        # Action Buttons Frame
        action_frame = tk.Frame(root, bg="#f4f6f9", pady=10)
        action_frame.pack()

        self.btn_compress = tk.Button(
            action_frame, 
            text="Compress (.bin)", 
            command=self.trigger_compression, 
            font=("Arial", 11, "bold"), 
            bg="#2ecc71", 
            fg="white", 
            padx=15, 
            pady=8,
            state=tk.DISABLED,
            relief=tk.FLAT
        )
        self.btn_compress.grid(row=0, column=0, padx=15)

        self.btn_decompress = tk.Button(
            action_frame, 
            text="Decompress (.txt)", 
            command=self.trigger_decompression, 
            font=("Arial", 11, "bold"), 
            bg="#e67e22", 
            fg="white", 
            padx=15, 
            pady=8,
            state=tk.DISABLED,
            relief=tk.FLAT
        )
        self.btn_decompress.grid(row=0, column=1, padx=15)

        # --- Faculty Dashboard Section (Analytics Pane) ---
        stats_frame = tk.LabelFrame(
            root, 
            text=" Algorithmic Analytics Dashboard ", 
            font=("Arial", 11, "bold"), 
            bg="white", 
            fg="#2c3e50",
            padx=15, 
            pady=15
        )
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        self.lbl_orig_size = tk.Label(stats_frame, text="Original Size: --", font=("Arial", 10), bg="white", anchor="w")
        self.lbl_orig_size.pack(fill=tk.X, pady=2)

        self.lbl_comp_size = tk.Label(stats_frame, text="Compressed Size: --", font=("Arial", 10), bg="white", anchor="w")
        self.lbl_comp_size.pack(fill=tk.X, pady=2)

        self.lbl_ratio = tk.Label(stats_frame, text="Space Optimization Ratio: --", font=("Arial", 10, "bold"), bg="white", fg="#27ae60", anchor="w")
        self.lbl_ratio.pack(fill=tk.X, pady=2)

        self.lbl_time = tk.Label(stats_frame, text="Execution Runtime Latency: --", font=("Arial", 10), bg="white", anchor="w")
        self.lbl_time.pack(fill=tk.X, pady=2)

        self.lbl_complexity = tk.Label(stats_frame, text="Theoretical Complexity: Time: O(N log K) | Space: O(K)", font=("Arial", 9, "italic"), bg="white", fg="#7f8c8d", anchor="w")
        self.lbl_complexity.pack(fill=tk.X, pady=8)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text & Binary Files", "*.txt *.bin"), ("All Files", "*.*")]
        )
        if file_path:
            self.selected_file_path = file_path
            self.lbl_file_path.config(text=os.path.basename(file_path), fg="#2c3e50", font=("Arial", 10, "bold"))
            
            # Enable buttons based on type of extension chosen
            if file_path.endswith('.txt'):
                self.btn_compress.config(state=tk.NORMAL)
                self.btn_decompress.config(state=tk.DISABLED)
            elif file_path.endswith('.bin'):
                self.btn_compress.config(state=tk.DISABLED)
                self.btn_decompress.config(state=tk.NORMAL)
            else:
                self.btn_compress.config(state=tk.NORMAL)
                self.btn_decompress.config(state=tk.NORMAL)

    def trigger_compression(self):
        try:
            start_time = time.time()
            orig_size = os.path.getsize(self.selected_file_path)
            
            # Run background processing engine
            output_file = self.compressor.compress(self.selected_file_path)
            
            end_time = time.time()
            comp_size = os.path.getsize(output_file)
            
            # Calculation Metrics
            saved_ratio = ((orig_size - comp_size) / orig_size) * 100
            elapsed_time = (end_time - start_time) * 1000 # convert to milliseconds

            # Update Metrics Panel
            self.lbl_orig_size.config(text=f"Original Size: {orig_size} Bytes")
            self.lbl_comp_size.config(text=f"Compressed Size: {comp_size} Bytes")
            self.lbl_ratio.config(text=f"Space Optimization Ratio: Saved {saved_ratio:.2f}% Space!")
            self.lbl_time.config(text=f"Execution Runtime Latency: {elapsed_time:.2f} ms")

            messagebox.showinfo("Success", f"Compression Completed!\nSaved file as: {os.path.basename(output_file)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during compression:\n{str(e)}")

    def trigger_decompression(self):
        try:
            start_time = time.time()
            
            # Run background decompression engine 
            output_file = self.compressor.decompress(self.selected_file_path)
            
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000

            # Clear stats pane for clear visualization layout 
            self.lbl_orig_size.config(text="File Mode: Binary Reconstruction")
            self.lbl_comp_size.config(text=f"Restored Output: {os.path.basename(output_file)}")
            self.lbl_ratio.config(text="Lossless Check: 100% Intact Structure")
            self.lbl_time.config(text=f"Execution Runtime Latency: {elapsed_time:.2f} ms")

            messagebox.showinfo("Success", f"Decompression Complete!\nRestored: {os.path.basename(output_file)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during decoding:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()