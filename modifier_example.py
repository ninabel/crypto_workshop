from Crypto.Cipher import AES
from Crypto.Util import Counter

from encrypt_decrypt import xor_encrypt_decrypt_block

import secrets

# --- 1. Setup and Encryption ---
key = secrets.token_bytes(32)  # AES-256
nonce = secrets.token_bytes(8)  # Standard 64-bit nonce for CTR
ctr = Counter.new(64, prefix=nonce)
cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

plaintext = b"I love you"
ciphertext = cipher.encrypt(plaintext)


# --- 2. Calculate the "modifier" A ---
# We want: plaintext ^ A = target
# So: A = plaintext ^ target
target = b"I hate you"
A = xor_encrypt_decrypt_block(plaintext, target)

# --- 3. XOR A with ciphertext ---
# This flips the bits in the ciphertext to match the target plaintext
modified_ciphertext = xor_encrypt_decrypt_block(ciphertext, A)

# --- 4. Decipher the result ---
# We must reset the counter to the same starting state to decrypt
ctr_reset = Counter.new(64, prefix=nonce)
decrypt_cipher = AES.new(key, AES.MODE_CTR, counter=ctr_reset)

decrypted_msg = decrypt_cipher.decrypt(modified_ciphertext)

# Output Results
print(f"Original Plaintext:  {plaintext.decode()}")
print(f"Target Plaintext:    {target.decode()}")
print("---")
print(f"Decrypted Result:    {decrypted_msg.decode()}")


# plaintext2 = b"I hate you"
# ciphertext2 = cipher.encrypt(plaintext2)
# modified_ciphertext2 = xor_encrypt_decrypt_block(ciphertext2, A)
# decrypted_msg2 = decrypt_cipher.decrypt(modified_ciphertext2)
# print("\n---\n")
# print(f"Original Plaintext2: {plaintext2.decode()}")
# print(f"Decrypted Result2:   {decrypted_msg2.decode()}")
