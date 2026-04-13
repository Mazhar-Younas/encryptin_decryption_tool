"""
pages/2_XOR_Cipher.py
XOR Cipher – Encrypt & Decrypt
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.ciphers import xor_encrypt_decrypt
from core.ui_utils import (
    page_header, success_box, error_box, info_box,
    result_area, file_upload_section, download_button, divider
)

st.set_page_config(page_title="XOR Cipher | CryptoVault", page_icon="⊕", layout="wide")

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
    "XOR Cipher",
    "Bitwise XOR with a numeric key (0–255). Symmetric: the same key encrypts and decrypts.",
    "⊕"
)

with st.sidebar:
    st.markdown("### ⊕ XOR Cipher")
    st.markdown("""
    **How it works:**
    Each character's ASCII code is XOR'd with the key value.

    - `char XOR key = encrypted`
    - `encrypted XOR key = char` (symmetric)

    **Key range:** 0–255 (single byte)

    **Note:** Non-printable results (outside ASCII 32–126)
    fall back to the original character to preserve readability.

    **Security note:** Trivially broken with known plaintext.
    Use AES-256 for real security.
    """)
    st.divider()
    st.info("Key 0 is a no-op (everything XOR 0 = itself). Avoid using 0.")

# ── File upload ──
file_upload_section(key="xor_upload", target_state_key="xor_input")

# ── Input ──
st.markdown("#### 📝 Input Text")
input_text = st.text_area(
    "Text input:",
    height=150,
    placeholder="Type or paste your text here…",
    key="xor_input",
    label_visibility="collapsed"
)

# ── Key ──
st.markdown("#### 🔑 XOR Key")
col_key, col_vis = st.columns([1, 3])
with col_key:
    key = st.number_input("Key (0–255):", min_value=0, max_value=255, value=42, step=1, key="xor_key")
with col_vis:
    binary_repr = format(key, '08b')
    st.markdown(f"""
    <div style="background:#161b22;border:1px solid rgba(255,255,255,.08);border-radius:8px;
                padding:.75rem 1rem;margin-top:1.6rem;color:#8b949e;font-size:0.9rem;">
        Key = <b style='color:#58a6ff'>{key}</b> &nbsp;|&nbsp;
        Hex = <b style='color:#f97316'>0x{key:02X}</b> &nbsp;|&nbsp;
        Binary = <b style='color:#a78bfa'>{binary_repr}</b>
    </div>
    """, unsafe_allow_html=True)

if key == 0:
    st.warning("⚠️ Key 0 is a no-op — output will be identical to input.")

divider()

# ── Action Buttons ──
col_enc, col_dec, col_clr = st.columns(3)
action = None

with col_enc:
    if st.button("🔒 Encrypt", use_container_width=True, key="xor_enc"):
        action = "encrypt"
with col_dec:
    if st.button("🔓 Decrypt", use_container_width=True, key="xor_dec"):
        action = "decrypt"
with col_clr:
    if st.button("🗑️ Clear", use_container_width=True, key="xor_clr"):
        st.session_state.xor_input = ""
        st.rerun()

result = None

if action:
    try:
        if not input_text.strip():
            error_box("Input text cannot be empty.")
        else:
            # XOR is symmetric: same function for encrypt and decrypt
            result = xor_encrypt_decrypt(input_text, key)
            op = "Encrypted" if action == "encrypt" else "Decrypted"
            success_box(f"{op} successfully with XOR key = {key} (0x{key:02X})")
    except ValueError as e:
        error_box(str(e))

# ── Output ──
if result is not None:
    divider()
    st.markdown("#### 📤 Output")
    result_area("Result:", result)
    st.markdown("<br>", unsafe_allow_html=True)
    download_button(result, filename="xor_result.txt")

# ── Character-level demo ──
divider()
with st.expander("🔬 Character-level XOR Demo"):
    demo_input = st.text_input("Demo character:", value="A", max_chars=1, key="xor_demo_char")
    demo_key = st.number_input("Demo key:", min_value=0, max_value=255, value=key, key="xor_demo_key")
    if demo_input and len(demo_input) == 1:
        orig_code = ord(demo_input)
        xored_code = orig_code ^ demo_key
        printable = chr(xored_code) if 32 <= xored_code <= 126 else f"<non-printable {xored_code}>"
        reversed_code = xored_code ^ demo_key
        st.markdown(f"""
        | Step | Value |
        |------|-------|
        | Input char | `{demo_input}` (ASCII {orig_code}, binary `{format(orig_code,'08b')}`) |
        | XOR key | `{demo_key}` (binary `{format(demo_key,'08b')}`) |
        | Result code | `{xored_code}` (binary `{format(xored_code,'08b')}`) |
        | Result char | `{printable}` |
        | Re-XOR'd (decrypt) | ASCII {reversed_code} = `{chr(reversed_code)}` ✅ |
        """)
