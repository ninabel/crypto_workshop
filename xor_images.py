from encrypt_decrypt import xor_encrypt_decrypt_block, read_file, write_file
from sys import argv
from pathlib import Path

if __name__ == "__main__":
    # xor two images
    if len(argv) != 3:
        print("Usage: python xor_images.py <image1.png> <image2.png>")
        exit(1)

    image1_path = Path(argv[1])
    image2_path = Path(argv[2])

    if not image1_path.exists() or not image2_path.exists():
        print("Error: One or both images do not exist.")
        exit(1)

    image1_data, image1_size = read_file(image1_path)
    image2_data, image2_size = read_file(image2_path)

    if image1_size != image2_size:
        print("Error: Images must be of the same size.")
        exit(1)

    # Perform XOR operation
    xor_result = xor_encrypt_decrypt_block(image1_data, image2_data)

    # Write the result to a new file
    write_file(Path("xor_result.png"), xor_result, image1_size)
    print("XOR operation completed. Result saved as 'xor_result.png'.")
