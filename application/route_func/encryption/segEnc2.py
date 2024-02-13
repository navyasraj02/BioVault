import os
import numpy as np
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

pubkeys_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "PublicKeys")

def encrypt_segment(public_key, segment):
    """Encrypts a single segment of keypoints using RSA.

    Args:
        public_key (cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey): The public key to use for encryption.
        segment (list): A list of keypoints of type <class 'tuple'>.

    Returns:
        bytes: The encrypted segment data.
    """
    # Serialize the segment data using pickle for RSA compatibility
    # serialized_segment = pickle.dumps(segment)

    # Encrypt the segment using the RSA public key
    encrypted_segments = []
    for point in segment:
        encrypted_point = public_key.encrypt(
            point.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        encrypted_segments.append(encrypted_point)
        
    return encrypted_segments

def get_public_keys(server_list):
    public_keys = {}
    for server_no in server_list:
        pem_file = os.path.join(pubkeys_folder, f"public_key_{server_no}.pem")
        print(pem_file)
        if not os.path.exists(pem_file):
            print(f"PEM file not found for server {server_no}")
            continue

        with open(pem_file, "rb") as f:
            pem_data = f.read()

        try:
            # Load the PEM data and extract the public key
            public_key = serialization.load_pem_public_key(
                pem_data,
                backend=default_backend()
            )
            public_keys[server_no] = public_key
        except ValueError as e:
            print(f"Error loading PEM file {pem_file}: {e}")

    return public_keys

# Example usage
server_list = [1, 3, 5]  # Replace with your actual server list
public_keys_dict = get_public_keys(server_list)
print(public_keys_dict)
