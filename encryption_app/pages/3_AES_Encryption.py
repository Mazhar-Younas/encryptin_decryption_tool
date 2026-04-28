"""
AES-256 (CBC) - Encrypt & Decrypt
"""

import base64
import os
import sys

import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.ciphers import aes_decrypt, aes_encrypt, aes_key_from_b64, aes_key_to_b64, generate_aes_key
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

st.set_page_config(page_title="AES-256 | CryptoForge", page_icon="AES", layout="wide")
apply_hacker_theme()

page_header(
    "AES-256 Encryption",
    "Modern symmetric encryption with a 256-bit key, CBC mode, and PKCS7 padding.",
    "AES",
)

sidebar_about(
    "AES-256 Encryption",
    """
    AES-256 uses the same secret key for encryption and decryption.<br><br>
    This app works with a Base64-encoded 32-byte key and generates a fresh IV for every encryption.<br><br>
    If you lose the key, the ciphertext cannot be recovered, so keep it separate and safe.
    """,
)

with st.container():
    st.markdown("#### Quick Notes")
    st.info("Leave the key empty on encrypt if you want the app to generate one for you.")
    st.warning("Never send the AES key and the encrypted text together in the same channel.")

if "aes_generated_key" not in st.session_state:
    st.session_state.aes_generated_key = ""

file_upload_section(key="aes_upload", target_state_key="aes_input")

st.markdown("#### Input Text")
input_text = st.text_area(
    "Text:",
    height=150,
    placeholder="Plaintext to encrypt, or Base64 ciphertext to decrypt...",
    key="aes_input",
    label_visibility="collapsed",
)

st.markdown("#### AES-256 Key (Base64)")
col_key_input, col_gen_btn = st.columns([3, 1])

with col_key_input:
    aes_key_b64 = st.text_input(
        "AES Key (Base64, 32 bytes):",
        value=st.session_state.aes_generated_key,
        placeholder="Leave blank to auto-generate on encrypt...",
        key="aes_key_b64",
        label_visibility="collapsed",
        type="password",
    )

with col_gen_btn:
    if st.button("Generate Key", use_container_width=True, key="gen_aes_key"):
        st.session_state.aes_generated_key = aes_key_to_b64(generate_aes_key())
        st.rerun()

if aes_key_b64.strip():
    try:
        raw = base64.b64decode(aes_key_b64.strip())
        byte_count = len(raw)
        color = "#00e5a8" if byte_count == 32 else "#fc8181"
        status = "Valid 32-byte key" if byte_count == 32 else f"{byte_count} bytes - must be 32"
        st.markdown(f"<small style='color:{color};'>{status}</small>", unsafe_allow_html=True)
    except Exception:
        st.markdown("<small style='color:#fc8181;'>Not valid Base64</small>", unsafe_allow_html=True)
else:
    info_box("No key entered. A new key will be auto-generated when you click Encrypt.")

if st.session_state.aes_generated_key:
    with st.expander("View / Copy Generated Key"):
        st.code(st.session_state.aes_generated_key, language=None)
        st.caption("Save this key securely. You need it to decrypt your data.")
        download_button(st.session_state.aes_generated_key, filename="aes_key.txt", label="Download Key")

divider()

col_enc, col_dec, col_clr = st.columns(3)
action = None
result = None

with col_enc:
    if st.button("Encrypt", use_container_width=True, key="aes_enc"):
        action = "encrypt"
with col_dec:
    if st.button("Decrypt", use_container_width=True, key="aes_dec"):
        action = "decrypt"
with col_clr:
    if st.button("Clear", use_container_width=True, key="aes_clr"):
        st.session_state.aes_generated_key = ""
        st.session_state.aes_input = ""
        st.rerun()

if action == "encrypt":
    try:
        if not input_text.strip():
            error_box("Input text cannot be empty.")
        else:
            raw_b64 = aes_key_b64.strip() or None
            if raw_b64 is None:
                key_bytes = generate_aes_key()
                st.session_state.aes_generated_key = aes_key_to_b64(key_bytes)
            else:
                key_bytes = aes_key_from_b64(raw_b64)

            result = aes_encrypt(input_text, key_bytes)
            success_box("Encrypted successfully with AES-256-CBC.")
            if raw_b64 is None:
                warning_box("A new key was auto-generated. Open the key section above and save it.")
    except ValueError as exc:
        error_box(str(exc))
    except Exception as exc:
        error_box(f"Unexpected error: {exc}")

elif action == "decrypt":
    try:
        if not input_text.strip():
            error_box("Input text cannot be empty.")
        elif not aes_key_b64.strip():
            error_box("A key is required for decryption.")
        else:
            result = aes_decrypt(input_text, aes_key_from_b64(aes_key_b64.strip()))
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
    download_button(result, filename="aes_result.txt")

divider()
with st.expander("How to Use AES-256 Safely"):
    st.markdown(
        """
        1. Enter plaintext and either paste a key or generate one.
        2. Encrypt and save the ciphertext.
        3. Store the key separately and securely.
        4. To decrypt, paste the exact ciphertext and the exact same Base64 key.
        """
    )
