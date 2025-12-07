import base64
from Crypto.Cipher import AES 

def decrypt_aes_ecb(ciphertext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


if __name__ == "__main__":
    with open("7.txt", "r") as f:
        b64_data = f.read()

    b64_data = "".join(b64_data.split()) 
    ciphertext = base64.b64decode(b64_data)

    key = b"YELLOW SUBMARINE"  

    plaintext = decrypt_aes_ecb(ciphertext, key)

    print(plaintext.decode("utf-8", errors="replace"))
