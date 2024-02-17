import heapq
from collections import defaultdict, Counter
import os
import time

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        internal_node = HuffmanNode(None, left.freq + right.freq)
        internal_node.left = left
        internal_node.right = right

        heapq.heappush(heap, internal_node)

    return heap[0]

def build_huffman_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}

    if node is not None:
        if node.char is not None:
            codes[node.char] = current_code
        build_huffman_codes(node.left, current_code + "0", codes)
        build_huffman_codes(node.right, current_code + "1", codes)

def huffman_encode(text):
    start_time = time.time()

    root = build_huffman_tree(text)
    codes = {}
    build_huffman_codes(root, "", codes)

    encoded_text = "".join(codes[char] for char in text)

    end_time = time.time()
    compression_time = end_time - start_time

    return encoded_text, codes, compression_time

def huffman_decode(encoded_text, codes):
    reversed_codes = {code: char for char, code in codes.items()}
    current_code = ""
    decoded_text = ""

    for bit in encoded_text:
        current_code += bit
        if current_code in reversed_codes:
            decoded_text += reversed_codes[current_code]
            current_code = ""

    return decoded_text

if __name__ == "__main__":
    # Take input text from the user
    text = input("Enter the text to encode: ")

    # Encode the text using Huffman coding
    encoded_text, codes, compression_time = huffman_encode(text)

    print("Huffman Codes:")
    for char, code in codes.items():
        print(f"{char}: {code}")

    print(f"Encoded Text: {encoded_text}")
    print(f"Compression Time: {compression_time:.6f} seconds")

    # Decode the encoded text
    decoded_text = huffman_decode(encoded_text, codes)
    print(f"Decoded Text: {decoded_text}")

    # Calculate compression ratio
    original_bits = len(text) * 8  # 8 bits per character
    encoded_bits = len(encoded_text)
    compression_ratio = original_bits / encoded_bits
    print(f"Compression Ratio: {compression_ratio:.2f}")
