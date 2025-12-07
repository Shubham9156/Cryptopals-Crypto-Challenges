import base64
import string
import sys

# ----------------- Scoring & helpers -----------------

ETAOIN = "etaoinshrdlucmfwypvbgkqjxz"

def score_english(text: str) -> float:
    """
    Higher score = more English-like.
    Reward ETAOIN letters + space, penalize weird / non-printable chars.
    """
    score = 0.0
    for c in text:
        # Penalty  (non printable)
        if c not in string.printable:
            score -= 10
            continue

        cl = c.lower()

        if cl in ETAOIN:
            score += 3
        elif cl == " ":
            score += 4
        elif cl in ".,'!?;-:\n0123456789":
            score += 1
        else:
            # Small penalty 
            score -= 0.5
    return score

def hamming_distance(b1: bytes, b2: bytes) -> int:
    return sum(bin(x ^ y).count("1") for x, y in zip(b1, b2))

def single_byte_xor(cipher: bytes, key: int) -> bytes:
    return bytes([b ^ key for b in cipher])

def break_single_byte_xor_block(block: bytes):
    """Return (key_byte, plaintext_bytes, score)."""
    best_score = float("-inf")
    best_key = 0
    best_plain = block

    for key in range(256):
        pt = single_byte_xor(block, key)
        decoded = pt.decode("latin1")  
        s = score_english(decoded)
        if s > best_score:
            best_score = s
            best_key = key
            best_plain = pt

    return best_key, best_plain, best_score

def guess_key_sizes(cipher: bytes, min_k: int = 2, max_k: int = 40, top_n: int = 3):
    scores = []
    for ks in range(min_k, max_k + 1):
        if 4 * ks > len(cipher):
            continue

        b1 = cipher[0:ks]
        b2 = cipher[ks:2*ks]
        b3 = cipher[2*ks:3*ks]
        b4 = cipher[3*ks:4*ks]

        d1 = hamming_distance(b1, b2) / ks
        d2 = hamming_distance(b2, b3) / ks
        d3 = hamming_distance(b3, b4) / ks

        scores.append(((d1 + d2 + d3) / 3.0, ks))

    scores.sort(key=lambda x: x[0])
    return [ks for _, ks in scores[:top_n]]

def repeating_key_xor(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def break_repeating_key_xor(cipher: bytes):
    candidate_sizes = guess_key_sizes(cipher)
    if not candidate_sizes:
        return None, None

    best_score = float("-inf")
    best_key = None
    best_plain = None

    for ks in candidate_sizes:
        blocks = [cipher[i::ks] for i in range(ks)]

        key_bytes = []
        for block in blocks:
            k, _, _ = break_single_byte_xor_block(block)
            key_bytes.append(k)

        key = bytes(key_bytes)
        plaintext = repeating_key_xor(cipher, key)
        decoded = plaintext.decode("latin1")
        s = score_english(decoded)

        if s > best_score:
            best_score = s
            best_key = key
            best_plain = decoded

    return best_key, best_plain

if __name__ == "__main__":
    try:
        with open("6.txt", "r") as f:
            b64_data = f.read()
    except FileNotFoundError:
        print("[-] Could not find 6.txt in this folder.")
        sys.exit(1)

    cipher = base64.b64decode(b64_data)
    key, plaintext = break_repeating_key_xor(cipher)

    if key is None or plaintext is None:
        print("[-] Failed to recover key / plaintext.")
        sys.exit(1)

    print("[+] Recovered key (bytes):", key)
    print("[+] Recovered key (as text):", key.decode("latin1"))
    print("\n[+] Decrypted plaintext:\n")
    print(plaintext)
