"""
XOR Cipher - Encrypt & Decrypt
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.ciphers import xor_encrypt_decrypt
from core.ui_utils import (
    apply_hacker_theme,
    divider,
    download_button,
    error_box,
    file_upload_section,
    page_header,
    result_area,
    sidebar_about,
    success_box,
)

st.set_page_config(page_title="XOR Cipher | CryptoForge", page_icon="XO", layout="wide")
apply_hacker_theme()

page_header(
    "XOR Cipher",
    "Apply a numeric key from 0 to 255 with bitwise XOR. The same operation encrypts and decrypts.",
    "XO",
)

sidebar_about(
    "XOR Cipher",
    """
    XOR combines each character with a numeric key using a bitwise operation.<br><br>
    Because XOR is symmetric, running the same key on encrypted text restores the original text.<br><br>
    It is useful for demos and simple obfuscation, but it is not secure enough for real-world protection.
    """,
)

with st.container():
    st.markdown("#### Quick Notes")
    st.info("Key 0 makes no change, so it behaves like a pass-through.")
    st.warning("Use AES-256 instead when you need real modern encryption.")

file_upload_section(key="xor_upload", target_state_key="xor_input")

st.markdown("#### Input Text")
input_text = st.text_area(
    "Text input:",
    height=150,
    placeholder="Type or paste your text here...",
    key="xor_input",
    label_visibility="collapsed",
)

st.markdown("#### XOR Key")
col_key, col_vis = st.columns([1, 3])
with col_key:
    key = st.number_input("Key (0-255):", min_value=0, max_value=255, value=42, step=1, key="xor_key")
with col_vis:
    st.markdown(
        f"""
        <div style="background:rgba(6,18,32,0.92);border:1px solid rgba(0,255,170,0.10);border-radius:10px;
                    padding:.8rem 1rem;margin-top:1.6rem;color:#b7d7e5;font-size:0.9rem;">
            Key = <b style='color:#7cf6ff'>{key}</b> |
            Hex = <b style='color:#7cf6ff'>0x{key:02X}</b> |
            Binary = <b style='color:#00e5a8'>{format(key, '08b')}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

divider()

col_enc, col_dec, col_clr = st.columns(3)
action = None
result = None

with col_enc:
    if st.button("Encrypt", use_container_width=True, key="xor_enc"):
        action = "encrypt"
with col_dec:
    if st.button("Decrypt", use_container_width=True, key="xor_dec"):
        action = "decrypt"
with col_clr:
    if st.button("Clear", use_container_width=True, key="xor_clr"):
        st.session_state.xor_input = ""
        st.rerun()

if action:
    try:
        if not input_text.strip():
            error_box("Input text cannot be empty.")
        else:
            result = xor_encrypt_decrypt(input_text, key)
            label = "Encrypted" if action == "encrypt" else "Decrypted"
            success_box(f"{label} successfully with XOR key = {key}.")
    except ValueError as exc:
        error_box(str(exc))

if result is not None:
    divider()
    st.markdown("#### Output")
    result_area("Result:", result)
    st.markdown("<br>", unsafe_allow_html=True)
    download_button(result, filename="xor_result.txt")

divider()
with st.expander("Character-level XOR Demo"):
    demo_input = st.text_input("Demo character:", value="A", max_chars=1, key="xor_demo_char")
    demo_key = st.number_input("Demo key:", min_value=0, max_value=255, value=key, key="xor_demo_key")
    if demo_input and len(demo_input) == 1:
        orig_code = ord(demo_input)
        xored_code = orig_code ^ demo_key
        printable = chr(xored_code) if 32 <= xored_code <= 126 else f"<non-printable {xored_code}>"
        reversed_code = xored_code ^ demo_key
        st.markdown(
            f"""
            | Step | Value |
            |------|-------|
            | Input char | `{demo_input}` (ASCII {orig_code}, binary `{format(orig_code, '08b')}`) |
            | XOR key | `{demo_key}` (binary `{format(demo_key, '08b')}`) |
            | Result code | `{xored_code}` (binary `{format(xored_code, '08b')}`) |
            | Result char | `{printable}` |
            | Re-XOR'd | ASCII {reversed_code} = `{chr(reversed_code)}` |
            """
        )
