from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

KEY = b'1234567890123456'  # ⚠️ Replace with secure key management in real apps
BLOCK_SIZE = 16

def encrypt_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    # 🔐 Proper PKCS7 padding
    padded_data = pad(data, BLOCK_SIZE)

    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = iv + cipher.encrypt(padded_data)

    enc_path = filepath + '.enc'
    with open(enc_path, 'wb') as f:
        f.write(encrypted)
    
    print(f"[+] Encrypted file saved as: {enc_path}")
    return enc_path

def decrypt_file(enc_path):
    with open(enc_path, 'rb') as f:
        encrypted = f.read()

    iv = encrypted[:BLOCK_SIZE]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted[BLOCK_SIZE:])

    try:
        # 🧹 Safe unpadding
        unpadded_data = unpad(decrypted_data, BLOCK_SIZE)
    except ValueError as e:
        print("[!] Padding error:", e)
        return None

    dec_path = enc_path.replace('.enc', '.dec')
    with open(dec_path, 'wb') as f:
        f.write(unpadded_data)
    
    print(f"[+] Decrypted file saved as: {dec_path}")
    return dec_path