import hashlib

# HEXDIGEST & THE AVALANCHE EFFECT ---

print("🏔️ TESTING THE CRYPTOGRAPHIC AVALANCHE EFFECT")
print("-" * 60)

payload_a = "Guangdong AEO Manufacturing Hub" + "15000.0" + "MSKU9918273"
bytes_a = payload_a.encode('utf-8')
hash_a = hashlib.sha256(bytes_a).hexdigest() # Day 23: 64-character alphanumeric signature

payload_b = "Guangdong AEO Manufacturing Hub" + "15000.1" + "MSKU9918273"
bytes_b = payload_b.encode('utf-8')
hash_b = hashlib.sha256(bytes_b).hexdigest()


print(f"Payload A (Original) : {payload_a}")
print(f"🔒 SHA-256 Hash A    : {hash_a}\n")

print(f"Payload B (Tampered) : {payload_b}")
print(f"🔒 SHA-256 Hash B    : {hash_b}")
print("-" * 60)