from ecdsa import SigningKey, SECP256k1, ECDH

# 1. Alice generates her key pair
alice_private_key = SigningKey.generate(curve=SECP256k1)
alice_public_key = alice_private_key.get_verifying_key()

# 2. Bob generates his key pair
bob_private_key = SigningKey.generate(curve=SECP256k1)
bob_public_key = bob_private_key.get_verifying_key()

# --- Simulating the exchange of Public Keys ---

# 3. Alice computes the shared secret using Bob's Public Key
alice_ecdh = ECDH(curve=SECP256k1)
alice_ecdh.load_private_key(alice_private_key)
alice_ecdh.load_received_public_key(bob_public_key)
alice_shared_secret = alice_ecdh.generate_sharedsecret_bytes()

# 4. Bob computes the shared secret using Alice's Public Key
bob_ecdh = ECDH(curve=SECP256k1)
bob_ecdh.load_private_key(bob_private_key)
bob_ecdh.load_received_public_key(alice_public_key)
bob_shared_secret = bob_ecdh.generate_sharedsecret_bytes()

# Verification
print(f"Alice's Secret (hex): {alice_shared_secret.hex()}")
print(f"Bob's Secret (hex):   {bob_shared_secret.hex()}")
print(f"Secrets Match: {alice_shared_secret == bob_shared_secret}")
