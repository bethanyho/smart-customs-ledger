import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_factory_private_key():
    """
    Generates an enterprise-grade 2048-bit RSA Private Key
    and saves it securely as an unencrypted local PEM file.
    """
    print("🔑 Generating secure 2048-bit RSA Private Key...")
    
    # Generate the private key object structure
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Cryptographically solid choice for RSA exponentiation
        key_size=2048
    )
    
    # Serialize the key material into a traditional OpenSSL PEM block format
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()  # Local practice environment setup
    )
    
    # Commit the raw binary bytes safely to your disk storage
    with open("factory_private_key.pem", "wb") as priv_file:
        priv_file.write(pem_private_key)
        
    print("💾 Success: Secret 'factory_private_key.pem' saved locally.")
    return private_key



def derive_customs_public_key(private_key):
    """
    Extracts the public key component from the private key 
    and saves it locally as a public PEM file for customs verification.
    """
    print("\n📜 Deriving Public Verification Key Component...")
    
    # Extract the matching public verification algorithm piece
    public_key = private_key.public_key()
    
    # Serialize public bytes into a standard SubjectPublicKeyInfo format block
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Commit public file key safely to disk for Customs clearance
    with open("customs_public_key.pem", "wb") as pub_file:
        pub_file.write(pem_public_key)
        
    print("💾 Success: Public 'customs_public_key.pem' saved locally.")



if __name__ == "__main__":
    print("====================================================")
    print("          INITIALIZING ASYMMETRIC KEY SYSTEM        ")
    print("====================================================")
    
    # Process generation pipeline sequence
    factory_priv_key = generate_factory_private_key()
    derive_customs_public_key(factory_priv_key)
    
    print("\n🔒 Asymmetric Architecture Established.")
    print("====================================================")