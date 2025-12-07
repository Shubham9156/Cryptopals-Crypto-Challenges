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
    return score

def single_byte_xor(cipher: bytes, key: int) -> bytes:
    return bytes([b ^ key for b in cipher])

def break_single_byte_xor(hex_str: str):
    cipher = bytes.fromhex(hex_str)
    best_score = 0
    best_text = None
    best_key = None

    for key in range(256):
        plain = single_byte_xor(cipher, key)
        try:
            decoded = plain.decode('utf-8')
        except:
            continue

        score = score_english(decoded)
        if score > best_score:
            best_score = score
            best_text = decoded
            best_key = key

    return best_key, best_text


if __name__ == "__main__":
    hex_input = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

    key, message = break_single_byte_xor(hex_input)

    print(f"Recovered key: {hex(key)}")
    print("Message:")
    print(message)
