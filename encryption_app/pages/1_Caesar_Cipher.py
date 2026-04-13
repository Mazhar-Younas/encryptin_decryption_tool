"""
pages/1_Caesar_Cipher.py
Caesar Cipher – Encrypt & Decrypt
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.ciphers import caesar_encrypt, caesar_decrypt
from core.ui_utils import (
    page_header, success_box, error_box, info_box,
    result_area, file_upload_section, download_button, divider
)

st.set_page_config(page_title="Caesar Cipher | CryptoVault", page_icon="🏛️", layout="wide")

# Shared dark theme CSS (injected on every page)
st.markdown("""
<style>
html,body,[data-testid="stAppViewContainer"]{background-color:#0d1117!important;color:#e6edf3}
[data-testid="stSidebar"]{background-color:#161b22!important;border-right:1px solid rgba(255,255,255,.08)}
[data-testid="stSidebar"] *{color:#c9d1d9!important}
h1,h2,h3{color:#e6edf3!important}
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stNumberInput>div>div>input{background-color:#161b22!important;border:1px solid rgba(255,255,255,.12)!important;color:#e6edf3!important;border-radius:8px!important}
.stButton>button{background:linear-gradient(135deg,#238636,#2ea043)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-weight:600!important}
.stButton>button:hover{opacity:.85!important}
.stDownloadButton>button{background:linear-gradient(135deg,#1f6feb,#388bfd)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-weight:600!important}
[data-testid="stFileUploader"]{background-color:#161b22!important;border:1px dashed rgba(255,255,255,.2)!important;border-radius:10px!important}
.stCode{background-color:#161b22!important;border-radius:8px!important}
.stTabs [data-baseweb="tab-list"]{background-color:#161b22;border-radius:8px}
.stTabs [data-baseweb="tab"]{color:#8b949e}
.stTabs [aria-selected="true"]{color:#58a6ff!important;border-bottom-color:#58a6ff!important}
[data-testid="metric-container"]{background:#161b22;border-radius:10px;padding:.75rem 1rem}
.streamlit-expanderHeader{background-color:#161b22!important;border-radius:8px!important}
</style>
""", unsafe_allow_html=True)

page_header(
    "Caesar Cipher",
    "Shift each letter by a fixed number (1–25). One of the oldest encryption techniques.",
    "🏛️"
)

# ── Sidebar info ──
with st.sidebar:
    st.markdown("### 🏛️ Caesar Cipher")
    st.markdown("""
    **How it works:**
    Each letter is shifted forward in the alphabet by the shift value.

    - `A` with shift 3 → `D`
    - `Z` with shift 3 → `C` (wraps around)

    **Decryption:** shift backwards by the same amount.

    **Security note:** Only 25 possible keys — easily brute-forced.
    """)
    st.divider()
    st.info("Non-alphabet characters (spaces, digits, punctuation) are preserved unchanged.")

# ── File upload ──
file_upload_section(key="caesar_upload", target_state_key="caesar_input")

# ── Input ──
st.markdown("#### 📝 Input Text")
input_text = st.text_area(
    "Enter text to encrypt or decrypt:",
    height=150,
    placeholder="Type or paste your text here…",
    key="caesar_input",
    label_visibility="collapsed"
)

# ── Key ──
st.markdown("#### 🔑 Shift Key")
col_key, col_info = st.columns([1, 3])
with col_key:
    shift = st.number_input("Shift (1–25):", min_value=1, max_value=25, value=3, step=1, key="caesar_shift")
with col_info:
    st.markdown(f"""
    <div style="background:#161b22;border:1px solid rgba(255,255,255,.08);border-radius:8px;
                padding:.75rem 1rem;margin-top:1.6rem;color:#8b949e;font-size:0.9rem;">
        Shift = <b style='color:#58a6ff'>{shift}</b> &nbsp;|&nbsp;
        A → <b style='color:#3fb950'>{chr(ord('A') + shift - 1) if shift <= 25 else 'A'}</b> &nbsp;|&nbsp;
        Z → <b style='color:#3fb950'>{chr(ord('A') + (25 + shift) % 26)}</b>
    </div>
    """, unsafe_allow_html=True)

divider()

# ── Action Buttons ──
col_enc, col_dec, col_clr = st.columns([1, 1, 1])

result = None
action = None

with col_enc:
    if st.button("🔒 Encrypt", use_container_width=True, key="caesar_enc"):
        action = "encrypt"
with col_dec:
    if st.button("🔓 Decrypt", use_container_width=True, key="caesar_dec"):
        action = "decrypt"
with col_clr:
    if st.button("🗑️ Clear", use_container_width=True, key="caesar_clr"):
        st.session_state.caesar_input = ""
        st.rerun()

# ── Process ──
if action:
    try:
        if not input_text.strip():
            error_box("Input text cannot be empty.")
        else:
            if action == "encrypt":
                result = caesar_encrypt(input_text, shift)
                success_box(f"Encrypted successfully with shift = {shift}")
            else:
                result = caesar_decrypt(input_text, shift)
                success_box(f"Decrypted successfully with shift = {shift}")
    except ValueError as e:
        error_box(str(e))

# ── Output ──
if result is not None:
    divider()
    st.markdown("#### 📤 Output")
    result_area("Result:", result)
    st.markdown("<br>", unsafe_allow_html=True)
    download_button(result, filename="caesar_result.txt")

# ── Brute Force Section ──
divider()
with st.expander("🔍 Brute-Force All 25 Shifts (Analysis)"):
    if input_text.strip():
        st.markdown("All possible decryptions for the input text:")
        for s in range(1, 26):
            try:
                attempt = caesar_decrypt(input_text, s)
                col1, col2 = st.columns([0.15, 0.85])
                col1.markdown(f"**Shift {s:02d}**")
                col2.code(attempt, language=None)
            except Exception:
                pass
    else:
        info_box("Enter some text above to enable brute-force analysis.")
