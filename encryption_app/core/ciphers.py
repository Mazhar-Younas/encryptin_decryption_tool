"""
core/ciphers.py
---------------
All encryption/decryption logic.
Supports: Caesar, XOR, AES-256, RSA, Monoalphabetic Cipher.
"""

import base64
import secrets
import string

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.padding import PKCS7


# ─────────────────────────────────────────────
#  CAESAR CIPHER
# ─────────────────────────────────────────────

def caesar_encrypt(text: str, shift: int) -> str:
    """
    Encrypt text using Caesar Cipher.
    Preserves case; non-alpha characters pass through unchanged.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")
    if not isinstance(shift, int) or not (1 <= shift <= 25):
        raise ValueError("Shift must be an integer between 1 and 25.")
    result = []
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - start + shift) % 26
            result.append(chr(start + shifted))
        else:
            result.append(char)
    return ''.join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    """Decrypt Caesar Cipher by reversing the shift."""
    return caesar_encrypt(text, 26 - (shift % 26))


# ─────────────────────────────────────────────
#  XOR CIPHER
# ─────────────────────────────────────────────

def xor_encrypt_decrypt(text: str, key: int) -> str:
    """
    Encrypt/Decrypt using XOR.
    XOR is symmetric: applying twice restores original.
    Non-printable results fall back to the original character.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")
    if not isinstance(key, int) or not (0 <= key <= 255):
        raise ValueError("XOR key must be an integer between 0 and 255.")
    result = []
    for char in text:
        xored = ord(char) ^ key
        # Keep result printable; fall back to original on non-printable output
        result.append(chr(xored) if 32 <= xored <= 126 else char)
    return ''.join(result)


# ─────────────────────────────────────────────
#  AES-256 (CBC mode, PKCS7 padding)
# ─────────────────────────────────────────────

def generate_aes_key() -> bytes:
    """Generate a cryptographically secure 32-byte AES-256 key."""
    return secrets.token_bytes(32)


def aes_key_to_b64(key: bytes) -> str:
    return base64.b64encode(key).decode('utf-8')


def aes_key_from_b64(b64_str: str) -> bytes:
    """Decode a base64 AES key and validate length."""
    try:
        key = base64.b64decode(b64_str.strip())
    except Exception:
        raise ValueError("AES key is not valid base64.")
    if len(key) != 32:
        raise ValueError(f"AES key must be exactly 32 bytes (256-bit). Got {len(key)} bytes.")
    return key


def aes_encrypt(plaintext: str, key: bytes) -> str:
    """
    Encrypt with AES-256-CBC.
    Returns base64(IV + ciphertext).
    """
    if not plaintext:
        raise ValueError("Input text cannot be empty.")
    if len(key) != 32:
        raise ValueError("AES key must be 32 bytes.")

    plaintext_bytes = plaintext.encode('utf-8')
    iv = secrets.token_bytes(16)

    padder = PKCS7(128).padder()
    padded = padder.update(plaintext_bytes) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    return base64.b64encode(iv + ciphertext).decode('utf-8')


def aes_decrypt(encrypted_b64: str, key: bytes) -> str:
    """
    Decrypt AES-256-CBC ciphertext.
    Expects base64(IV + ciphertext).
    """
    if not encrypted_b64:
        raise ValueError("Input text cannot be empty.")
    if len(key) != 32:
        raise ValueError("AES key must be 32 bytes.")
    try:
        combined = base64.b64decode(encrypted_b64.strip())
    except Exception:
        raise ValueError("Ciphertext is not valid base64. Ensure the input is AES-encrypted text.")

    if len(combined) < 32:
        raise ValueError("Ciphertext is too short. It may be corrupted or not AES-encrypted.")

    iv = combined[:16]
    ciphertext = combined[16:]

    try:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = PKCS7(128).unpadder()
        plaintext_bytes = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext_bytes.decode('utf-8')
    except Exception:
        raise ValueError("Decryption failed. The key may be incorrect or the data may be corrupted.")


# ─────────────────────────────────────────────
#  RSA (2048-bit, OAEP padding)
# ─────────────────────────────────────────────

def generate_rsa_keypair() -> tuple[str, str]:
    """
    Generate a 2048-bit RSA key pair.
    Returns (private_key_pem, public_key_pem) as strings.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    return private_pem, public_pem


def rsa_encrypt(plaintext: str, public_key_pem: str) -> str:
    """
    Encrypt text with an RSA public key (OAEP + SHA-256).
    Returns base64-encoded ciphertext.
    RSA-2048 can encrypt up to ~214 bytes per chunk; larger messages are chunked.
    """
    if not plaintext:
        raise ValueError("Input text cannot be empty.")
    if not public_key_pem.strip():
        raise ValueError("Public key cannot be empty.")

    try:
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8'),
            backend=default_backend()
        )
    except Exception:
        raise ValueError("Invalid RSA public key. Ensure it is in PEM format.")

    plaintext_bytes = plaintext.encode('utf-8')
    # RSA-2048 with OAEP-SHA256: max chunk = 256 - 66 = 190 bytes
    chunk_size = 190
    chunks = [plaintext_bytes[i:i + chunk_size] for i in range(0, len(plaintext_bytes), chunk_size)]

    encrypted_chunks = []
    for chunk in chunks:
        encrypted = public_key.encrypt(
            chunk,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        encrypted_chunks.append(base64.b64encode(encrypted).decode('utf-8'))

    # Join chunks with '|' delimiter
    return '|'.join(encrypted_chunks)


def rsa_decrypt(ciphertext: str, private_key_pem: str) -> str:
    """
    Decrypt RSA ciphertext with a private key.
    Expects '|'-delimited base64 chunks.
    """
    if not ciphertext:
        raise ValueError("Input text cannot be empty.")
    if not private_key_pem.strip():
        raise ValueError("Private key cannot be empty.")

    try:
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
    except Exception:
        raise ValueError("Invalid RSA private key. Ensure it is in PEM format.")

    try:
        chunks = ciphertext.strip().split('|')
        decrypted_chunks = []
        for chunk in chunks:
            encrypted_bytes = base64.b64decode(chunk)
            decrypted = private_key.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            decrypted_chunks.append(decrypted)
        return b''.join(decrypted_chunks).decode('utf-8')
    except Exception:
        raise ValueError("RSA decryption failed. The private key may be wrong or ciphertext corrupted.")


# ─────────────────────────────────────────────
#  MONOALPHABETIC CIPHER
# ─────────────────────────────────────────────

ALPHABET = string.ascii_uppercase


def validate_mono_mapping(mapping: dict[str, str]) -> None:
    """
    Validate a monoalphabetic mapping dictionary.
    Raises ValueError on:
    - Non-alphabet keys or values
    - Duplicate values (two keys mapping to the same letter)
    """
    if not mapping:
        raise ValueError("Mapping is empty. Add at least one letter mapping.")

    seen_values = set()
    for key, value in mapping.items():
        if not key.isalpha() or len(key) != 1:
            raise ValueError(f"Invalid mapping key: '{key}'. Keys must be single alphabet letters.")
        if not value.isalpha() or len(value) != 1:
            raise ValueError(f"Invalid mapping value: '{value}'. Values must be single alphabet letters.")
        val_upper = value.upper()
        if val_upper in seen_values:
            raise ValueError(f"Duplicate mapping target: '{value}'. Each letter can only be a target once.")
        seen_values.add(val_upper)


def mono_encrypt(text: str, mapping: dict[str, str]) -> str:
    """
    Encrypt text using a monoalphabetic substitution mapping.
    mapping = {'A': 'X', 'B': 'Q', ...} (uppercase keys expected)
    Non-mapped letters pass through unchanged.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")
    validate_mono_mapping(mapping)

    upper_mapping = {k.upper(): v.upper() for k, v in mapping.items()}
    result = []
    for char in text:
        if char.upper() in upper_mapping:
            sub = upper_mapping[char.upper()]
            result.append(sub if char.isupper() else sub.lower())
        else:
            result.append(char)
    return ''.join(result)


def mono_decrypt(text: str, mapping: dict[str, str]) -> str:
    """
    Decrypt by reversing the monoalphabetic mapping.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")
    validate_mono_mapping(mapping)

    # Build reverse mapping
    reverse_mapping = {v.upper(): k.upper() for k, v in mapping.items()}
    result = []
    for char in text:
        if char.upper() in reverse_mapping:
            sub = reverse_mapping[char.upper()]
            result.append(sub if char.isupper() else sub.lower())
        else:
            result.append(char)
    return ''.join(result)
