# Smart File Compressor using Huffman Coding

A cross-platform desktop application built to demonstrate optimal data compression using **Huffman Coding (Greedy Paradigm)**. This project was developed as a laboratory implementation for the Design and Analysis of Algorithms (DAA) course in the 4th Semester.

## 🚀 Key Features
* **Universal Compression:** Processes raw byte streams, making it capable of handling `.txt`, `.docx`, `.pdf`, and image files.
* **Algorithmic Dashboard:** Displays live execution latency metrics down to the millisecond.
* **Measurable Optimization:** Provides a real-time tracking display of the space optimization percentage ratio achieved.
* **Lossless Integrity:** Implements precise prefix-free binary decoding, ensuring 100% data preservation upon decompression.

## 📊 Performance Benchmark (Sample Case)
Using the classic text payload *Alice's Adventures in Wonderland*:
* **Original Footprint:** 171,821 Bytes
* **Compressed Footprint:** 94,415 Bytes
* **Space Saved Ratio:** **45.05% Compression Efficiency**
* **Execution Latency:** ~50.60 milliseconds

> Insert your application screenshot showing the 45.05% compression result here!

## 🧠 Algorithmic Paradigm & Complexity Analysis

Huffman Coding is a deterministic **Greedy Algorithm** that minimizes the weighted path length of a binary tree based on character/byte frequencies.

| Phase / Operation | Theoretical Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| **Frequency Profiling** | $O(N)$ where $N$ is total file bytes | $O(K)$ where $K$ is unique bytes |
| **Priority Queue Sorting** | $O(K \log K)$ via Min-Heap processing | $O(K)$ node generation bounds |
| **Bitstream Stream Extraction** | $O(N)$ encoding layout | $O(N)$ bit allocation structure |

## 🛠️ How to Set Up and Run
1. Ensure you have Python 3.x installed in your environment.
2. Create a Folder named 'src' and save 'app_ui.py' and 'huffman_engine.py' files in it.
3. Create a Folder named 'sample' and save 'demo.txt' in it for testing.
4. After saving files, run and test to check how it's working alright.
