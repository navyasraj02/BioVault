import secrets

def generate_secure_token(length=16):
    # Generate a secure random string of the specified length
    token = secrets.token_hex(length // 2)  # Each byte is represented by 2 hex characters
    print("User pin number: ",token)
    return token