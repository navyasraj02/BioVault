from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
import pickle

def encrypt_segment(public_key, segment):
    # Serialize the public key
    serialized_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Load the serialized public key
    loaded_public_key = serialization.load_pem_public_key(
        serialized_public_key,
        backend=default_backend()
    )
    
    # Pickle and serialize the segment
    serialized_segment = pickle.dumps(segment)
    
    # Encrypt the serialized segment using RSA
    encrypted_segment = loaded_public_key.encrypt(
        serialized_segment,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return encrypted_segment

# Example usage:
# public_key = 
# segment = kp_s[0]  # Example segment from the list
# encrypted_segment = encrypt_segment(public_key, segment)
