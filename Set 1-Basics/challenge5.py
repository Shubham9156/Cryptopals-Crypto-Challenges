def repeating_key_xor(plaintext: bytes, key: bytes) -> bytes:
    """Encrypt plaintext with repeating-key XOR (Vigenère-style XOR)."""
    ciphertext = bytearray()
    key_len = len(key)

    for i, b in enumerate(plaintext):
        k = key[i % key_len]   # repeat the key
        ciphertext.append(b ^ k)

    return bytes(ciphertext)


if __name__ == "__main__":
    plaintext = (
        b"Burning 'em, if you ain't quick and nimble\n"
        b"I go crazy when I hear a cymbal"
    )
    key = b"ICE"

    expected_hex = (
        "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622"
        "6324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b"
        "20283165286326302e27282f"
    )

    ciphertext = repeating_key_xor(plaintext, key)
    result_hex = ciphertext.hex()

    print("Result hex:   ", result_hex)
    print("Expected hex: ", expected_hex)
    print("Match?        ", result_hex == expected_hex)
