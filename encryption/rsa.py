

from math import gcd

def RSA(p: int, q: int, message: str):
    # Calculate n
    n = p * q

    # Calculate totient, t
    t = (p - 1) * (q - 1)

    # Select public key, e
    e = 2
    while gcd(e, t) != 1:
        e += 1

    # Select private key, d
    d = pow(e, -1, t)

    # Convert the message into numerical values using ASCII
    numerical_message = [ord(char) for char in message]

    # Encrypt the message
    encrypted_numerical_message = [(char ** e) % n for char in numerical_message]

    # Decrypt the message
    decrypted_numerical_message = [(char ** d) % n for char in encrypted_numerical_message]

    # Convert decrypted numerical values back to text
    decrypted_message = ''.join([chr(char) for char in decrypted_numerical_message])

    return encrypted_numerical_message, decrypted_message

# Testcase - 1
p = 53
q = 59
message = "edna"
encrypted_message, decrypted_message = RSA(p, q, message)
print("Original message:", message)
print("Encrypted message:", encrypted_message)
print("Decrypted message:", decrypted_message)

# Testcase - 2
p = 61
q = 53
message = "lillyedna@gmail.com"
encrypted_message, decrypted_message = RSA(p, q, message)
print("Original message:", message)
print("Encrypted message:", encrypted_message)
print("Decrypted message:", decrypted_message)
