"""
Playfair Cipher - Encrypt & Decrypt
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.ciphers import generate_playfair_matrix, playfair_decrypt, playfair_encrypt
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

st.set_page_config(page_title="Playfair Cipher | CryptoForge", page_icon="PF", layout="wide")
apply_hacker_theme()

page_header(
    "Playfair Cipher",
    "Encrypt digraphs using a 5x5 keyword matrix with merged I and J plus rectangle-based substitution rules.",
    "PF",
)

sidebar_about(
    "Playfair Cipher",
    """
    Playfair encrypts pairs of letters instead of single characters.<br><br>
    A keyword builds the 5x5 matrix, I and J share one position, repeated letters are split,
    and odd-length text gets a filler X.<br><br>
    It is a stronger classical cipher than Caesar, but it is still not secure for modern use.
    """,
)

with st.container():
    st.markdown("#### Quick Notes")
    st.info("Only alphabet letters and spaces are accepted as input.")
    st.warning("Spaces are removed before processing and the result is returned in uppercase digraph form.")


def _prepare_preview_text(raw_text: str) -> tuple[str | None, str | None]:
    if not raw_text or not raw_text.strip():
        return None, None
    if any(not (char.isalpha() or char.isspace()) for char in raw_text):
        return None, "Input text must contain only alphabet letters and spaces."
    normalized = "".join(raw_text.upper().split()).replace("J", "I")
    return (normalized, None) if normalized else (None, None)


file_upload_section(key="playfair_upload", target_state_key="playfair_input")

st.markdown("#### Input Text")
input_text = st.text_area(
    "Enter text to encrypt or decrypt:",
    height=150,
    placeholder="Type or paste your text here...",
    key="playfair_input",
    label_visibility="collapsed",
)

st.markdown("#### Key")
col_key, col_info = st.columns([1.2, 2.8])
with col_key:
    key = st.text_input("Keyword:", placeholder="Enter alphabetic keyword", key="playfair_key", label_visibility="collapsed")
with col_info:
    if key.strip():
        try:
            matrix, _ = generate_playfair_matrix(key)
            matrix_preview = " | ".join(" ".join(row) for row in matrix)
            st.markdown(
                f"""
                <div style="background:rgba(6,18,32,0.92);border:1px solid rgba(0,255,170,0.10);border-radius:10px;
                            padding:.8rem 1rem;margin-top:0.2rem;color:#b7d7e5;font-size:0.9rem;">
                    Key = <b style='color:#7cf6ff'>{''.join(key.upper().split()).replace('J', 'I')}</b> |
                    Matrix = <b style='color:#00e5a8;font-family:monospace'>{matrix_preview}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except ValueError as exc:
            error_box(str(exc))
    else:
        info_box("Enter a keyword to generate the Playfair matrix.")

preview_text, preview_error = _prepare_preview_text(input_text)
if preview_error:
    error_box(preview_error)
elif preview_text:
    st.markdown(
        f"""
        <div style="background:rgba(6,18,32,0.92);border:1px solid rgba(0,255,170,0.10);border-radius:10px;
                    padding:.8rem 1rem;margin:.75rem 0 0;color:#b7d7e5;font-size:0.9rem;">
            Prepared text preview = <b style='color:#00e5a8;font-family:monospace'>{preview_text}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

divider()

col_enc, col_dec, col_clr = st.columns(3)
result = None
action = None

with col_enc:
    if st.button("Encrypt", use_container_width=True, key="playfair_enc"):
        action = "encrypt"
with col_dec:
    if st.button("Decrypt", use_container_width=True, key="playfair_dec"):
        action = "decrypt"
with col_clr:
    if st.button("Clear", use_container_width=True, key="playfair_clr"):
        st.session_state.playfair_input = ""
        st.session_state.playfair_key = ""
        st.rerun()

if action:
    try:
        if action == "encrypt":
            result = playfair_encrypt(input_text, key)
            success_box("Encrypted successfully with the Playfair cipher.")
        else:
            result = playfair_decrypt(input_text, key)
            success_box("Decrypted successfully with the Playfair cipher.")
    except ValueError as exc:
        error_box(str(exc))
    except Exception as exc:
        error_box(f"Unexpected error: {exc}")

if result is not None:
    divider()
    st.markdown("#### Output")
    result_area("Result:", result)
    st.markdown("<br>", unsafe_allow_html=True)
    download_button(result, filename="playfair_result.txt")

divider()
with st.expander("Playfair Notes"):
    st.markdown(
        """
        Same-row letters shift right on encryption.
        Same-column letters shift down on encryption.
        Rectangle pairs swap columns.

        During decryption, filler X characters are cleaned up where possible.
        """
    )
