"""
RSA (2048-bit, OAEP+SHA-256) - Encrypt & Decrypt
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.ciphers import generate_rsa_keypair, rsa_decrypt, rsa_encrypt
from core.ui_utils import (
    apply_hacker_theme,
    divider,
    download_button,
    error_box,
    file_upload_section,
    info_box,
    page_header,
    result_area,
    sidebar_about,
    success_box,
    warning_box,
)

st.set_page_config(page_title="RSA Encryption | CryptoForge", page_icon="RSA", layout="wide")
apply_hacker_theme()

page_header(
    "RSA Encryption",
    "Asymmetric encryption with a public key for encryption and a private key for decryption.",
    "RSA",
)

sidebar_about(
    "RSA Encryption",
    """
    RSA uses two different keys: a public key for encryption and a private key for decryption.<br><br>
    This makes it ideal for secure exchange, because you can share the public key openly while keeping
    the private key secret.<br><br>
    The app uses 2048-bit keys with OAEP and SHA-256 padding.
    """,
)

with st.container():
    st.markdown("#### Quick Notes")
    st.info("Generate a key pair first, then share only the public key with others.")
    st.warning("Never share your private key. It can decrypt every message for that pair.")

if "rsa_private_pem" not in st.session_state:
    st.session_state.rsa_private_pem = ""
if "rsa_public_pem" not in st.session_state:
    st.session_state.rsa_public_pem = ""

st.markdown("#### RSA Key Pair")
col_gen, col_status = st.columns([1, 3])
with col_gen:
    if st.button("Generate 2048-bit Key Pair", use_container_width=True, key="rsa_gen"):
        with st.spinner("Generating 2048-bit RSA key pair..."):
            priv, pub = generate_rsa_keypair()
            st.session_state.rsa_private_pem = priv
            st.session_state.rsa_public_pem = pub
        st.rerun()

with col_status:
    if st.session_state.rsa_public_pem:
        success_box("Key pair generated and ready.")
    else:
        info_box("Click Generate Key Pair to create your RSA keys, or paste existing keys below.")

if st.session_state.rsa_public_pem:
    key_tab1, key_tab2 = st.tabs(["Public Key", "Private Key"])
    with key_tab1:
        st.code(st.session_state.rsa_public_pem, language=None)
        download_button(st.session_state.rsa_public_pem, "rsa_public_key.pem", "Download Public Key")
    with key_tab2:
        st.code(st.session_state.rsa_private_pem, language=None)
        download_button(st.session_state.rsa_private_pem, "rsa_private_key.pem", "Download Private Key")

divider()

st.markdown("#### Mode")
mode = st.radio(
    "Select mode:",
    ["Encrypt (with Public Key)", "Decrypt (with Private Key)"],
    horizontal=True,
    key="rsa_mode",
    label_visibility="collapsed",
)

file_upload_section(key="rsa_upload", target_state_key="rsa_input")

st.markdown("#### Input Text")
input_text = st.text_area(
    "Input:",
    height=150,
    placeholder="Plaintext to encrypt, or RSA ciphertext to decrypt...",
    key="rsa_input",
    label_visibility="collapsed",
)

if "Encrypt" in mode:
    st.markdown("#### Public Key (PEM)")
    pub_key_input = st.text_area(
        "Public key:",
        value=st.session_state.rsa_public_pem,
        height=160,
        placeholder="-----BEGIN PUBLIC KEY-----",
        key="rsa_pub_key_input",
        label_visibility="collapsed",
    )
    priv_key_input = ""
else:
    st.markdown("#### Private Key (PEM)")
    priv_key_input = st.text_area(
        "Private key:",
        value=st.session_state.rsa_private_pem,
        height=200,
        placeholder="-----BEGIN PRIVATE KEY-----",
        key="rsa_priv_key_input",
        label_visibility="collapsed",
    )
    pub_key_input = ""

divider()

col_action, col_clr = st.columns(2)
action = None
result = None

with col_action:
    if st.button("Run RSA", use_container_width=True, key="rsa_action"):
        action = mode
with col_clr:
    if st.button("Clear", use_container_width=True, key="rsa_clr"):
        st.session_state.rsa_input = ""
        st.rerun()

if action:
    try:
        if not input_text.strip():
            error_box("Input text cannot be empty.")
        elif "Encrypt" in action:
            if not pub_key_input.strip():
                error_box("Public key is required for encryption.")
            else:
                result = rsa_encrypt(input_text, pub_key_input)
                success_box("Encrypted successfully with RSA-2048.")
        else:
            if not priv_key_input.strip():
                error_box("Private key is required for decryption.")
            else:
                result = rsa_decrypt(input_text, priv_key_input)
                success_box("Decrypted successfully.")
    except ValueError as exc:
        error_box(str(exc))
    except Exception as exc:
        error_box(f"Unexpected error: {exc}")

if result is not None:
    divider()
    st.markdown("#### Output")
    result_area("Result:", result)
    st.markdown("<br>", unsafe_allow_html=True)
    filename = "rsa_encrypted.txt" if "Encrypt" in mode else "rsa_decrypted.txt"
    download_button(result, filename=filename)

divider()
with st.expander("RSA Usage Guide"):
    st.markdown(
        """
        1. Generate a key pair.
        2. Share the public key with the sender.
        3. Encrypt with the public key.
        4. Decrypt with the matching private key.

        RSA is best for secure key exchange and short messages, not very large payloads.
        """
    )
