

# from math import gcd

# def RSA(p: int, q: int, message: str):
#     # Calculate n
#     n = p * q

#     # Calculate totient, t
#     t = (p - 1) * (q - 1)

#     # Select public key, e
#     e = 2
#     while gcd(e, t) != 1:
#         e += 1

#     # Select private key, d
#     d = pow(e, -1, t)

#     # Convert the message into numerical values using ASCII
#     numerical_message = [ord(char) for char in message]

#     # Encrypt the message
#     encrypted_numerical_message = [(char ** e) % n for char in numerical_message]

#     # Decrypt the message
#     decrypted_numerical_message = [(char ** d) % n for char in encrypted_numerical_message]

#     # Convert decrypted numerical values back to text
#     decrypted_message = ''.join([chr(char) for char in decrypted_numerical_message])

#     return encrypted_numerical_message, decrypted_message

# # Testcase - 1
# p = 53
# q = 59
# message = "edna"
# encrypted_message, decrypted_message = RSA(p, q, message)
# print("Original message:", message)
# print("Encrypted message:", encrypted_message)
# print("Decrypted message:", decrypted_message)

# # Testcase - 2
# p = 61
# q = 53
# message = "lillyedna@gmail.com"
# encrypted_message, decrypted_message = RSA(p, q, message)
# print("Original message:", message)
# print("Encrypted message:", encrypted_message)
# print("Decrypted message:", decrypted_message)


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def RSA(message):
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Extract public key
    public_key = private_key.public_key()

    # Encrypt the message
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt the message
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()

    return encrypted_message, decrypted_message

# Test
message = "Hello, I am Edna"
encrypted_message, decrypted_message = RSA(message)
print("Original message:", message)
print("Encrypted message:", encrypted_message)
print("Decrypted message:", decrypted_message)
