from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time

def generate_key_pair():
    key = RSA.generate(2048)  # 2048-bit key for security
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_text(text, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    encrypted_text = cipher.encrypt(text.encode())
    return encrypted_text

def decrypt_text(encrypted_text, private_key):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    decrypted_text = cipher.decrypt(encrypted_text).decode()
    return decrypted_text

if __name__ == "__main__":
    # Generate key pair
    private_key, public_key = generate_key_pair()

    # Take user input for text to encrypt
    original_text = input("Enter the text to encrypt: ")

    # Measure encryption time
    start_time = time.time()

    # Encrypt the text
    encrypted_text = encrypt_text(original_text, public_key)

    # Measure encryption time
    end_time = time.time()
    encryption_time = end_time - start_time

    print(f"Encrypted Text: {encrypted_text.hex()}")
    print(f"Encryption Time: {encryption_time:.6f} seconds")

    # Measure decryption time
    start_time = time.time()

    # Decrypt the text
    decrypted_text = decrypt_text(encrypted_text, private_key)

    # Measure decryption time
    end_time = time.time()
    decryption_time = end_time - start_time

    print(f"Decrypted Text: {decrypted_text}")
    print(f"Decryption Time: {decryption_time:.6f} seconds")

    # Calculate encryption speed (bytes per second)
    encryption_speed = len(original_text) / encryption_time
    print(f"Encryption Speed: {encryption_speed:.2f} bytes/second")
