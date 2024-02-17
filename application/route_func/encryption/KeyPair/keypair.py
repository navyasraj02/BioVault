from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_and_write_rsa_key_pair_to_file(index):
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Get the public key
    public_key = private_key.public_key()

    # Serialize private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key to PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Write private and public keys to a single file
    with open(f"key_pair_{index}.pem", "wb") as key_pair_file:
        key_pair_file.write(private_pem)
        key_pair_file.write(public_pem)

# Generate and write 10 RSA key pairs
for i in range(1, 11):
    generate_and_write_rsa_key_pair_to_file(i)
