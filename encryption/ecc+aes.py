import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import time


def generate_key_pair():
    private_key = ec.generate_private_key(
        ec.SECP256R1(),  # You can choose other curves if needed
        default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def derive_shared_key(private_key, peer_public_key):
    shared_key = private_key.exchange(
        ec.ECDH(),
        peer_public_key
    )
    return shared_key


def encrypt(shared_key, plaintext):
    start_time = time.time()

    # Use a key derivation function (KDF) to derive a symmetric key
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # Length of the derived key for AES-256
        salt=None,
        info=b'',
        backend=default_backend()
    ).derive(shared_key)

    # Generate a random IV
    iv = os.urandom(16)

    # Use the derived key and IV for encryption
    cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Apply padding to the plaintext
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext.encode('utf-8')) + padder.finalize()

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Return the IV along with the ciphertext and encryption time
    return iv + ciphertext, elapsed_time


def decrypt(shared_key, ciphertext):
    start_time = time.time()

    # Extract the IV from the ciphertext
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    # Use a key derivation function (KDF) to derive a symmetric key
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # Length of the derived key for AES-256
        salt=None,
        info=b'',
        backend=default_backend()
    ).derive(shared_key)

    # Use the derived key and IV for decryption
    cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the decrypted text
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(decrypted_text) + unpadder.finalize()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Return the plaintext and decryption time
    return plaintext.decode('utf-8'), elapsed_time


# Example usage:
private_key_Alice, public_key_Alice = generate_key_pair()
private_key_Bob, public_key_Bob = generate_key_pair()

# Alice sends her public key to Bob
shared_key_Bob = derive_shared_key(private_key_Bob, public_key_Alice)

# Bob sends his public key to Alice
shared_key_Alice = derive_shared_key(private_key_Alice, public_key_Bob)

while True:
    print("\n1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        plaintext = input("Enter the text to encrypt: ")
        ciphertext, encryption_time = encrypt(shared_key_Alice, plaintext)
        print(f"Ciphertext: {ciphertext.hex()}")
        print(f"Encryption Time: {encryption_time} seconds")

    elif choice == '2':
        ciphertext_hex = input("Enter the ciphertext in hex format: ")
        ciphertext = bytes.fromhex(ciphertext_hex)
        decrypted_text, decryption_time = decrypt(shared_key_Bob, ciphertext)
        print(f"Decrypted Text: {decrypted_text}")
        print(f"Decryption Time: {decryption_time} seconds")

    elif choice == '3':
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
