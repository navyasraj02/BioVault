from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
import pickle

"""def encrypt_segment(public_key, segment):
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
    
    return encrypted_segment"""

# Example usage:
# public_key = 
# segment = kp_s[0]  # Example segment from the list
# encrypted_segment = encrypt_segment(public_key, segment)

import pickle
import rsa
import numpy as np
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

pubkeys_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)),"PublicKeys")

"""def encrypt_segment(public_key, segment):
    
    # Serialize the segment data using pickle for RSA compatibility
    # serialized_segment = pickle.dumps(segment)

    # Split the serialized data into chunks within the RSA key size limit
    chunk_size = rsa.common.bit_size(public_key.n) // 8 - 11  # Subtract padding overhead
    chunks = np.array_split(segment, np.ceil(len(segment) / chunk_size))

    # Encrypt each chunk and combine them
    encrypted_chunks = []
    for chunk in chunks:
        encrypted_chunks.append(rsa.encrypt(chunk, public_key))
        
    return np.concatenate(encrypted_chunks)"""



def get_public_keys(server_list):
    public_keys = {}
    for server_no in server_list:
        # Replace this with your actual method to generate file path
        pem_file = os.path.join(pubkeys_folder, f"public_key_{server_no}.pem")
        print(pem_file)
        if not os.path.exists(pem_file):
            print(f"PEM file not found for server {server_no}")
            continue

        with open(pem_file, "rb") as f:
            pem_data = f.read()

        # Replace this with your actual method to extract public key from PEM data
        # This assumes the PEM data contains only the public key
        # public_key = pem_data.split("-----BEGIN PUBLIC KEY-----")[1].split("-----END PUBLIC KEY-----")[0]
        # public_key = public_key.strip()
        # public_key = rsa.PublicKey.load_pkcs1(public_key.encode('utf-8'))
        # public_key = serialization.load_pem_public_key(
        #     pem_data,
        #     backend=default_backend()
        # )

        # public_keys[server_no] = public_key

        try:
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

