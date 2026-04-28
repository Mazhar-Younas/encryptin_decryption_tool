"""
Caesar Cipher - Encrypt & Decrypt
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.ciphers import caesar_decrypt, caesar_encrypt
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
)

st.set_page_config(page_title="Caesar Cipher | CryptoForge", page_icon="CC", layout="wide")
apply_hacker_theme()

page_header(
    "Caesar Cipher",
    "Shift each letter by a fixed number from 1 to 25 using one of the oldest classical cipher systems.",
    "CC",
)

sidebar_about(
    "Caesar Cipher",
    """
    Each letter is shifted forward in the alphabet by the selected key.<br><br>
    A with shift 3 becomes D, while Z with shift 3 wraps around to C.<br><br>
    Decryption uses the same key in reverse. This technique is useful for learning,
    but it is very easy to brute-force because only 25 possible keys exist.
    """,
)

with st.container():
    st.markdown("#### Quick Notes")
    st.info("Non-alphabet characters like spaces, digits, and punctuation stay unchanged.")
    st.warning("This cipher is educational only and should not be used for real security.")

file_upload_section(key="caesar_upload", target_state_key="caesar_input")

st.markdown("#### Input Text")
input_text = st.text_area(
    "Enter text to encrypt or decrypt:",
    height=150,
    placeholder="Type or paste your text here...",
    key="caesar_input",
    label_visibility="collapsed",
)

st.markdown("#### Shift Key")
col_key, col_info = st.columns([1, 3])
with col_key:
    shift = st.number_input("Shift (1-25):", min_value=1, max_value=25, value=3, step=1, key="caesar_shift")
with col_info:
    st.markdown(
        f"""
        <div style="background:rgba(6,18,32,0.92);border:1px solid rgba(0,255,170,0.10);border-radius:10px;
                    padding:.8rem 1rem;margin-top:1.6rem;color:#b7d7e5;font-size:0.9rem;">
            Shift = <b style='color:#7cf6ff'>{shift}</b> |
            A becomes <b style='color:#00e5a8'>{chr(ord('A') + shift - 1)}</b> |
            Z becomes <b style='color:#00e5a8'>{chr(ord('A') + (25 + shift) % 26)}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

divider()

col_enc, col_dec, col_clr = st.columns(3)
result = None
action = None

with col_enc:
    if st.button("Encrypt", use_container_width=True, key="caesar_enc"):
        action = "encrypt"
with col_dec:
    if st.button("Decrypt", use_container_width=True, key="caesar_dec"):
        action = "decrypt"
with col_clr:
    if st.button("Clear", use_container_width=True, key="caesar_clr"):
        st.session_state.caesar_input = ""
        st.rerun()

if action:
    try:
        if not input_text.strip():
            error_box("Input text cannot be empty.")
        elif action == "encrypt":
            result = caesar_encrypt(input_text, shift)
            success_box(f"Encrypted successfully with shift = {shift}.")
        else:
            result = caesar_decrypt(input_text, shift)
            success_box(f"Decrypted successfully with shift = {shift}.")
    except ValueError as exc:
        error_box(str(exc))

if result is not None:
    divider()
    st.markdown("#### Output")
    result_area("Result:", result)
    st.markdown("<br>", unsafe_allow_html=True)
    download_button(result, filename="caesar_result.txt")

divider()
with st.expander("Brute-Force All 25 Shifts"):
    if input_text.strip():
        st.markdown("All possible decryptions for the current input:")
        for brute_shift in range(1, 26):
            attempt = caesar_decrypt(input_text, brute_shift)
            col1, col2 = st.columns([0.18, 0.82])
            col1.markdown(f"**Shift {brute_shift:02d}**")
            col2.code(attempt, language=None)
    else:
        info_box("Enter some text above to enable brute-force analysis.")
