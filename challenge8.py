def count_repeated_blocks(ct: bytes, block_size: int = 16) -> int:

    blocks = [
        ct[i:i + block_size]
        for i in range(0, len(ct), block_size)
    ]
    unique_blocks = set(blocks)
    return len(blocks) - len(unique_blocks)  # number of repeats


def detect_aes_ecb(filename: str):
    best_line_num = None
    best_line_hex = None
    best_score = -1

    with open(filename, "r") as f:
        for i, line in enumerate(f, start=1):
            hex_str = line.strip()
            if not hex_str:
                continue

            ct = bytes.fromhex(hex_str)
            score = count_repeated_blocks(ct, block_size=16)

            if score > best_score:
                best_score = score
                best_line_num = i
                best_line_hex = hex_str

    return best_line_num, best_line_hex, best_score


if __name__ == "__main__":
    line_num, line_hex, score = detect_aes_ecb("8.txt")

    print(f"[+] Most likely ECB-encrypted line: {line_num}")
    print(f"[+] Hex ciphertext: {line_hex}")
    print(f"[+] Repeated 16-byte blocks: {score}")
