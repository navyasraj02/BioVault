from hashlib import sha256

def rc4(key, data):
    """
    Implements the RC4 stream cipher.

    Args:
        key: The key for encryption.
        data: The data to be encrypted.

    Returns:
        The encrypted data.
    """
    S = list(range(256))
    j = 0
    out = []

    # KSA (Key Scheduling Algorithm)
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA (Pseudo-Random Generation Algorithm)
    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])

    return bytes(out)

def hash_string(string):
    """
    Hashes a given string using the SHA-256 algorithm after applying additional transformations with RC4.

    Args:
        string: The string to be hashed.

    Returns:
        The SHA-256 hash of the transformed string as a hexadecimal string.
    """
    # RC4 key (you can change this key)
    rc4_key = b'SecretKeyMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1kpdOa5X4ncb4UUrYZAxu3wmwB/RLJGb0/Q5rWXjn24Z7ycTXzmpi8kk4f/M5+9gc1U'
    #int_value = int(string)
    # Apply RC4 encryption to the string
    encrypted_string = rc4(rc4_key, string.encode()).hex()

    # Hash the encrypted string using SHA-256
    return sha256(encrypted_string.encode()).hexdigest()


