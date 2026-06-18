"""Simple columnar transposition cipher implementation.

Supports numeric key (e.g., 4312567) or keyword (e.g., SECRET) where column order
is determined by sorting key characters. Non-letter characters are preserved in
place for simplicity.
"""
from typing import List


def _key_to_order(key: str) -> List[int]:
    # If key is numeric, treat each digit as column index order.
    if key.isdigit():
        order = [int(c) for c in key]
        # make them zero-based ranks
        # handle repeated digits by preserving order
        ranks = sorted([(v, i) for i, v in enumerate(order)])
        return [ranks.index((v, i)) for i, v in enumerate(order)]

    # For keyword, order by alphabetical order of characters
    pairs = list(enumerate(key))
    sorted_pairs = sorted(pairs, key=lambda x: (x[1], x[0]))
    order = [0] * len(key)
    for rank, (orig_idx, _) in enumerate(sorted_pairs):
        order[orig_idx] = rank
    return order


def encrypt(plaintext: str, key: str) -> str:
    if not key:
        raise ValueError("Key required for transposition cipher")

    order = _key_to_order(key)
    cols = len(order)
    # remove newlines for block fill
    text = plaintext.replace('\n', ' ')
    # pad to full grid
    rows = (len(text) + cols - 1) // cols
    padded = text.ljust(rows * cols)
    # build grid row-wise
    grid = [list(padded[i * cols:(i + 1) * cols]) for i in range(rows)]
    # read out by columns in order of order ranks
    cipher = []
    for rank in range(cols):
        col_idx = order.index(rank)
        for r in range(rows):
            cipher.append(grid[r][col_idx])
    return ''.join(cipher).rstrip()


def decrypt(ciphertext: str, key: str) -> str:
    if not key:
        raise ValueError("Key required for transposition cipher")
    order = _key_to_order(key)
    cols = len(order)
    rows = (len(ciphertext) + cols - 1) // cols
    # compute how many full columns (some implementations handle short last column)
    # For our simple scheme we assume padded full rectangle during encryption
    full = rows * cols
    padded = ciphertext.ljust(full)
    # build empty grid
    grid = [ [''] * cols for _ in range(rows) ]
    idx = 0
    for rank in range(cols):
        col_idx = order.index(rank)
        for r in range(rows):
            grid[r][col_idx] = padded[idx]
            idx += 1
    # read row-wise
    plain = ''.join(''.join(row) for row in grid)
    return plain.rstrip()


if __name__ == "__main__":
    pt = "THIS IS A SECRET MESSAGE"
    k = "4312"
    ct = encrypt(pt, k)
    print("ct:", ct)
    print("pt:", decrypt(ct, k))
