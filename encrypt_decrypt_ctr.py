from pathlib import Path
import sys
from Crypto.Cipher import AES
from encrypt_decrypt import read_file, write_file


image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}


def aes_encrypt_ctr(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
    return cipher.encrypt(plaintext)


def aes_decrypt_ctr(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
    return cipher.decrypt(ciphertext)


# Example usage
if __name__ == "__main__":
    key_data = "thevarysecretkey".encode()
    # don't use a fixed key and IV in production, generate them securely
    iv = "invector".encode()  # initialization vector for key function
    if len(sys.argv) < 2:
        print("\nBlock encryption demo using AES-CTR with a real key and IV")
        text = "This is a secret message that will be encrypted and decrypted using AES block mode."
        plaintext = text.encode()

        encrypted = aes_encrypt_ctr(plaintext, key_data, iv)
        print(f"\nEncrypted data: {encrypted.hex()}")

        decrypted = aes_decrypt_ctr(encrypted, key_data, iv)
        print(f"\nDecrypted text: {decrypted.decode()}")
    else:
        file_path = sys.argv[1]
        input_data, image_size = read_file(file_path)
        encrypted_data = aes_encrypt_ctr(input_data, key_data, iv)
        encrypted_path = Path(file_path).stem + "_encrypted" + Path(file_path).suffix
        write_file(encrypted_path, encrypted_data, image_size)
        print(f"File '{file_path}' encrypted and saved as '{encrypted_path}'")

        decrypted_data = aes_decrypt_ctr(encrypted_data, key_data, iv)
        decrypted_path = Path(file_path).stem + "_decrypted" + Path(file_path).suffix
        write_file(decrypted_path, decrypted_data, image_size)
        print(f"File '{encrypted_path}' decrypted and saved as '{decrypted_path}'")
