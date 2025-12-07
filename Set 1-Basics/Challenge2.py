def fixed_xor(hex1: str, hex2: str) -> str:
    # Converting hex to raw bytes
    b1 = bytes.fromhex(hex1)
    b2 = bytes.fromhex(hex2)

    # XOR must be equal length
    if len(b1) != len(b2):
        raise ValueError("Inputs must be the same length")

    # XORing each pair of bytes
    result = bytes([a ^ b for a, b in zip(b1, b2)])

    # Giving hex str
    return result.hex()


if __name__ == "__main__":
    hex1 = "1c0111001f010100061a024b53535009181c"
    hex2 = "686974207468652062756c6c277320657965"
    expected = "746865206b696420646f6e277420706c6179"

    output = fixed_xor(hex1, hex2)

    print("Result:   ", output)
    print("Expected: ", expected)
    print("Match?    ", output == expected)
