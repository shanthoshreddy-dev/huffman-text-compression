"""
analyse.py
----------
Runs test cases on sample text files and shows full size breakdown
comparing original ASCII storage vs matrix (Huffman) storage.

Usage:
    python analyse.py
"""

import os
import sys
from encoder import encode, matrix_size_bits, clean
from layout import TOTAL_BOXES, BITS_X, BITS_Z, BOX_W


def analyse(path):
    if not os.path.exists(path):
        print(f"[!] File not found: {path}")
        return

    raw_bytes = os.path.getsize(path)
    raw_bits  = raw_bytes * 8
    words     = clean(open(path, encoding='utf-8').read())

    matrix, pages, CODES, REVERSE, stats = encode(path)

    word_rows    = [r for r in matrix if not (r[2] == 0 and r[1] == 0)]
    matrix_bits, fixed = matrix_size_bits(matrix)

    avg_code = sum(len(r[3]) for r in word_rows) / max(len(word_rows), 1)
    savings  = raw_bits - matrix_bits

    print(f'\n{"="*56}')
    print(f'  {path}')
    print(f'{"="*56}')
    print(f'  Total words           : {len(words)}')
    print(f'  Encoded words         : {len(word_rows)}  ({len(word_rows)/max(len(words),1)*100:.1f}%)')
    print(f'  Pages used            : {pages}  ({TOTAL_BOXES} lines/page)')
    print(f'  Page separator rows   : {pages}  (format: [page_num, 0, 0, 0])')

    print(f'\n  ORIGINAL (plain ASCII):')
    print(f'    Size                : {raw_bits} bits  ({raw_bytes} bytes)')
    print(f'    Cost per word       : ~{raw_bits // max(len(words),1)} bits avg  (8 bits per char)')

    print(f'\n  MATRIX STORAGE:')
    print(f'    x  (0-{BOX_W})     : {BITS_X} bits')
    print(f'    y  (always 0)       : 0 bits  (omitted)')
    print(f'    z  (0-{TOTAL_BOXES})         : {BITS_Z} bits')
    print(f'    code (huffman)      : avg {avg_code:.1f} bits')
    print(f'    Cost per word       : {fixed}+{avg_code:.1f} = {fixed+avg_code:.1f} bits avg')
    print(f'    Total matrix size   : {matrix_bits} bits  ({matrix_bits//8} bytes)')

    print(f'\n  RESULT:')
    print(f'    Space saved         : {savings} bits  ({savings//8} bytes)')
    print(f'    Saved %             : {savings/raw_bits*100:.1f}%')
    print(f'    Compression ratio   : {matrix_bits/raw_bits*100:.1f}%')

    print(f'\n  SAMPLE ROWS (first page separator + first 5 words):')
    print(f'    {"type":<12} {"x":>5} {"y":>3} {"z":>3}  {"code":<10} note')
    print(f'    {"-"*54}')
    shown = 0
    for row in matrix[:8]:
        x, y, z, code = row
        if y == 0 and z == 0:
            print(f'    {"PAGE SEP":<12} {x:>5} {y:>3} {z:>3}  {"0":<10} page {x} starts here')
        else:
            word = REVERSE.get(code, '???')
            print(f'    {"word":<12} {x:>5} {y:>3} {z:>3}  {code:<10} "{word}"')
            shown += 1
            if shown == 5:
                break


if __name__ == '__main__':
    files = sys.argv[1:] if len(sys.argv) > 1 else ['one_page.txt', 'five_pages.txt', 'twenty_pages.txt']
    for f in files:
        analyse(f)
