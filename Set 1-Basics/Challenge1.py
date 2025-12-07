import base64

def hex_to_base64(hex_str: str) -> str:
    # 1. COnverting hex (string) to bytes
    raw_bytes = bytes.fromhex(hex_str)

    # 2. Converting bytes to base64 bytes
    b64_bytes = base64.b64encode(raw_bytes)

    # 3.Converting bytes to string
    return b64_bytes.decode("ascii")


if __name__ == "__main__":
    hex_input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    expected_output = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

    result = hex_to_base64(hex_input)
    print("Result:   ", result)
    print("Expected: ", expected_output)
    print("Match?    ", result == expected_output)
