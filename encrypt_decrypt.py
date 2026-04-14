# XOR encryption and decryption function
from pathlib import Path
import sys
from PIL import Image
import secrets

image_extensions = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}


def xor_encrypt_decrypt_block(input_bytes: bytes, key_bytes: bytes) -> bytes:
    # XOR each byte of the input with the corresponding byte of the key
    # assume key length is greater than ot equal to input length
    if len(key_bytes) < len(input_bytes):
        raise ValueError("Key length must be greater than or equal to input length")
    output_bytes = []
    for i, byte in enumerate(input_bytes):
        output_byte = byte ^ key_bytes[i]
        output_bytes.append(output_byte)
    return bytes(output_bytes)


def encrypt_decrypt(input_bytes: bytes, key_bytes: bytes, blocksize: int) -> bytes:
    # Split the input into blocks and apply XOR encryption/decryption to each block
    if len(key_bytes) < blocksize:
        raise ValueError("Key length must be greater than or equal to block size")
    blocks = [
        input_bytes[i : i + blocksize] for i in range(0, len(input_bytes), blocksize)
    ]
    return b"".join(
        xor_encrypt_decrypt_block(block, key_bytes)  # key_function(key_bytes, i))
        for i, block in enumerate(blocks)
    )


def read_file(file_path: str) -> bytes:
    format = Path(file_path).suffix[1:]  # Get the file extension without the dot
    if format.lower() in image_extensions:
        image = Image.open(file_path, formats=[format.upper()]).convert("RGB")
        # Encrypt image bytes
        return image.tobytes(), image.size
    with open(file_path, "rb") as f:
        return f.read(), None


def write_file(file_path: str, data: bytes, image_size=None) -> None:
    format = Path(file_path).suffix[1:]  # Get the file extension without the dot
    if format.lower() in image_extensions and image_size is not None:
        # Create new image with encrypted data
        encrypted_image = Image.frombytes("RGB", image_size, data)
        # Save encrypted image
        encrypted_image.save(file_path, format=format.upper())
    else:
        with open(file_path, "wb") as f:
            f.write(data)


# Example usage
if __name__ == "__main__":
    key = "thevarysecretkey"
    key_data = key.encode()
    # create random key data
    blocksize = 161  # for example, 16 bytes
    key_data = secrets.token_bytes(blocksize)
    iv = secrets.token_bytes(blocksize)  # initialization vector for key function
    # blocksize = len(key_data)
    if len(sys.argv) < 2:
        print("Simple XOR Encryption/Decryption")
        print(f"Using key: {key} (block size: {blocksize} bytes)")
        text = "This is a secret message that will be encrypted and decrypted using XOR operation."
        # Encrypt the data
        encrypted = encrypt_decrypt(text.encode(), key_data, blocksize)
        print(f"Original data: {text}")
        print(f"Encrypted data: {encrypted}")
        # Decrypt the data
        decrypted = encrypt_decrypt(encrypted, key_data, blocksize)
        print(f"Decrypted data: {decrypted.decode()}")
    else:
        file_path = sys.argv[1]
        input_data, image_size = read_file(file_path)
        write_file(
            Path(file_path).stem + "_original" + Path(file_path).suffix,
            input_data,
            image_size,
        )
        encrypted_data = encrypt_decrypt(input_data, key_data, blocksize)
        encrypted_path = Path(file_path).stem + "_encrypted" + Path(file_path).suffix
        write_file(encrypted_path, encrypted_data, image_size)
        print(f"File '{file_path}' encrypted and saved as '{encrypted_path}'")
        decrypted_data = encrypt_decrypt(encrypted_data, key_data, blocksize)
        decrypted_path = Path(file_path).stem + "_decrypted" + Path(file_path).suffix
        write_file(decrypted_path, decrypted_data, image_size)
        print(f"File '{encrypted_path}' decrypted and saved as '{decrypted_path}'")
