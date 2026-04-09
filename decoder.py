"""
decoder.py
----------
Reads the matrix file and reconstructs the original text
by reversing the huffman code lookup.

Usage:
    python decoder.py <matrix_file> <original_text_file>

Example:
    python decoder.py one_page_matrix.txt one_page.txt
"""

import sys
from dictionary import build_dictionary


def decode(matrix_path, source_text_path):
    # Build reverse lookup from the original source text
    _, REVERSE_CODES, _ = build_dictionary(open(source_text_path, encoding='utf-8').read())

    # Load and parse the matrix file
    entries = []
    with open(matrix_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4:
                x, y, z, code = int(parts[0]), int(parts[1]), int(parts[2]), parts[3]
                entries.append((x, y, z, code))

    print(f"[A] Loaded {len(entries)} matrix entries")

    # Filter out page separator rows (code == '0' and x == page number)
    word_entries = [(x, y, z, code) for x, y, z, code in entries if not (y == 0 and z == 0)]

    # Sort into reading order: page (implicit from position), then line (z), then x
    word_entries.sort(key=lambda e: (e[2], e[0]))

    # Decode each huffman code back to a word
    decoded_words = []
    errors = 0
    for x, y, z, code in word_entries:
        if code in REVERSE_CODES:
            decoded_words.append(REVERSE_CODES[code])
        else:
            print(f"  [!] Unknown code: '{code}' at position x={x}, z={z}")
            errors += 1

    print(f"[B] Decoded {len(decoded_words)} words  ({errors} errors)")
    print(f"[C] Reconstructed text (first 100 words):")
    print("    " + ' '.join(decoded_words[:100]))

    return decoded_words


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python decoder.py <matrix_file> <original_text_file>")
        print("Example: python decoder.py one_page_matrix.txt one_page.txt")
        sys.exit(1)

    matrix_path = sys.argv[1]
    source_path = sys.argv[2]
    decode(matrix_path, source_path)
