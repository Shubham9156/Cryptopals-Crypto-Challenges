import string

# Frequency Scoring Table for English Language
FREQ = {
    'a': 8.12, 'b': 1.49, 'c': 2.71, 'd': 4.32, 'e': 12.02, 'f': 2.30,
    'g': 2.03, 'h': 5.92, 'i': 7.31, 'j': 0.10, 'k': 0.69, 'l': 3.98,
    'm': 2.61, 'n': 6.95, 'o': 7.68, 'p': 1.82, 'q': 0.11, 'r': 6.02,
    's': 6.28, 't': 9.10, 'u': 2.88, 'v': 1.11, 'w': 2.09, 'x': 0.17,
    'y': 2.11, 'z': 0.07, ' ': 13.00
}

def score_english(text: str) -> float:
    score = 0.0
    for c in text.lower():
        if c in FREQ:
            score += FREQ[c]
        # Penalty for weird chars
        elif c not in string.printable:
            score -= 5
    return score

def single_byte_xor(cipher: bytes, key: int) -> bytes:
    return bytes([b ^ key for b in cipher])

def break_single_byte_xor(cipher_hex: str):
    cipher = bytes.fromhex(cipher_hex)
    best_score = float("-inf")
    best_text = None
    best_key = None

    for key in range(256):
        decrypted = single_byte_xor(cipher, key)
        try:
            decoded = decrypted.decode("utf-8")
        except UnicodeDecodeError:
            continue

        s = score_english(decoded)
        if s > best_score:
            best_score = s
            best_text = decoded
            best_key = key

    return best_score, best_key, best_text

def detect_single_char_xor(filename: str):
    global_best_score = float("-inf")
    global_best_line = None
    global_best_key = None
    global_best_plain = None
    global_best_line_num = None

    with open(filename, "r") as f:
        for i, line in enumerate(f, start=1):
            hex_str = line.strip()
            if not hex_str:
                continue

            score, key, plain = break_single_byte_xor(hex_str)

            if score > global_best_score:
                global_best_score = score
                global_best_line = hex_str
                global_best_key = key
                global_best_plain = plain
                global_best_line_num = i

    return global_best_line_num, global_best_line, global_best_key, global_best_plain

if __name__ == "__main__":
    line_num, hex_line, key, plaintext = detect_single_char_xor("4.txt")

    print(f"[+] Encrypted line number: {line_num}")
    print(f"[+] Line (hex): {hex_line}")
    print(f"[+] Detected key: {hex(key)} ({repr(chr(key))})")
    print(f"[+] Decrypted plaintext: {plaintext}")
