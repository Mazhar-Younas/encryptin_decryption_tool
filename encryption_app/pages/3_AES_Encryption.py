"""
pages/3_AES_Encryption.py
AES-256 (CBC) – Encrypt & Decrypt
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import base64
import streamlit as st
from core.ciphers import (
    aes_encrypt, aes_decrypt,
    generate_aes_key, aes_key_to_b64, aes_key_from_b64
)
from core.ui_utils import (
    page_header, success_box, error_box, info_box, warning_box,
    result_area, file_upload_section, download_button, divider
)

st.set_page_config(page_title="AES-256 | CryptoVault", page_icon="🛡️", layout="wide")

DARK_CSS = """
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
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

page_header(
    "AES-256 Encryption",
    "Advanced Encryption Standard – 256-bit key, CBC mode, PKCS7 padding.",
    "🛡️"
)

with st.sidebar:
    st.markdown("### 🛡️ AES-256")
    st.markdown("""
    **How it works:**
    - Symmetric cipher (same key encrypts & decrypts)
    - Key size: **256 bits (32 bytes)**
    - Mode: **CBC** (Cipher Block Chaining)
    - Padding: **PKCS7**
    - IV: randomly generated per encryption

    **Key format:** Base64-encoded 32-byte string.

    **Auto-generate:** Leave the key field blank and click
    Encrypt — a secure key is generated for you.

    **CRITICAL:** Save your key! Without it, decryption
    is impossible.
    """)
    st.divider()
    st.warning("⚠️ Never share your AES key alongside ciphertext in the same channel.")

# ── Session state for generated key ──
if "aes_generated_key" not in st.session_state:
    st.session_state.aes_generated_key = ""

# ── File upload ──
file_upload_section(key="aes_upload", target_state_key="aes_input")

# ── Input ──
st.markdown("#### 📝 Input Text")
input_text = st.text_area(
    "Text:",
    height=150,
    placeholder="Plaintext to encrypt, or base64 ciphertext to decrypt…",
    key="aes_input",
    label_visibility="collapsed"
)

# ── Key Section ──
st.markdown("#### 🔑 AES-256 Key (Base64)")
col_key_input, col_gen_btn = st.columns([3, 1])

with col_key_input:
    # Show generated key if available, otherwise allow editing
    key_val = st.session_state.aes_generated_key
    aes_key_b64 = st.text_input(
        "AES Key (Base64, 32 bytes):",
        value=key_val,
        placeholder="Leave blank to auto-generate on encrypt…",
        key="aes_key_b64",
        label_visibility="collapsed",
        type="password"
    )

with col_gen_btn:
    if st.button("⚙️ Generate Key", use_container_width=True, key="gen_aes_key"):
        new_key = generate_aes_key()
        st.session_state.aes_generated_key = aes_key_to_b64(new_key)
        st.rerun()

# Show key length indicator
if aes_key_b64.strip():
    try:
        raw = base64.b64decode(aes_key_b64.strip())
        byte_count = len(raw)
        color = "#3fb950" if byte_count == 32 else "#f85149"
        status = "✅ Valid 32-byte key" if byte_count == 32 else f"❌ {byte_count} bytes — must be 32"
        st.markdown(f"<small style='color:{color};'>{status}</small>", unsafe_allow_html=True)
    except Exception:
        st.markdown("<small style='color:#f85149;'>❌ Not valid Base64</small>", unsafe_allow_html=True)
else:
    info_box("No key entered — a new key will be auto-generated when you click Encrypt.")

# ── Show generated key (copyable) ──
if st.session_state.aes_generated_key:
    with st.expander("👁️ View / Copy Generated Key"):
        st.code(st.session_state.aes_generated_key, language=None)
        st.caption("⚠️ Save this key securely. You need it to decrypt your data.")
        download_button(
            st.session_state.aes_generated_key,
            filename="aes_key.txt",
            label="⬇️ Download Key"
        )

divider()

# ── Action Buttons ──
col_enc, col_dec, col_clr = st.columns(3)
action = None
result = None
used_key_b64 = ""

with col_enc:
    if st.button("🔒 Encrypt", use_container_width=True, key="aes_enc"):
        action = "encrypt"
with col_dec:
    if st.button("🔓 Decrypt", use_container_width=True, key="aes_dec"):
        action = "decrypt"
with col_clr:
    if st.button("🗑️ Clear", use_container_width=True, key="aes_clr"):
        st.session_state.aes_generated_key = ""
        st.session_state.aes_input = ""
        st.rerun()

if action == "encrypt":
    try:
        if not input_text.strip():
            error_box("Input text cannot be empty.")
        else:
            raw_b64 = aes_key_b64.strip() if aes_key_b64.strip() else None
            if raw_b64 is None:
                # Auto-generate key
                key_bytes = generate_aes_key()
                used_key_b64 = aes_key_to_b64(key_bytes)
                st.session_state.aes_generated_key = used_key_b64
            else:
                key_bytes = aes_key_from_b64(raw_b64)
                used_key_b64 = raw_b64

            result = aes_encrypt(input_text, key_bytes)
            success_box("Encrypted successfully with AES-256-CBC.")
            if raw_b64 is None:
                warning_box("A new key was auto-generated. See 'View / Copy Generated Key' above.")
    except ValueError as e:
        error_box(str(e))
    except Exception as e:
        error_box(f"Unexpected error: {e}")

elif action == "decrypt":
    try:
        if not input_text.strip():
            error_box("Input text cannot be empty.")
        elif not aes_key_b64.strip():
            error_box("A key is required for decryption. Enter the Base64 key used during encryption.")
        else:
            key_bytes = aes_key_from_b64(aes_key_b64.strip())
            result = aes_decrypt(input_text, key_bytes)
            success_box("Decrypted successfully.")
    except ValueError as e:
        error_box(str(e))
    except Exception as e:
        error_box(f"Unexpected error: {e}")

# ── Output ──
if result is not None:
    divider()
    st.markdown("#### 📤 Output")
    result_area("Result:", result)
    st.markdown("<br>", unsafe_allow_html=True)
    download_button(result, filename="aes_result.txt")

# ── How-to Info ──
divider()
with st.expander("📖 How to Use AES-256 Safely"):
    st.markdown("""
    **Encryption workflow:**
    1. Enter your plaintext in the input box.
    2. Click **Generate Key** for a secure random key — *or* paste an existing Base64 key.
    3. Click **Encrypt**. The output is Base64-encoded ciphertext (IV + encrypted data).
    4. **Download and save both the ciphertext and the key separately.**

    **Decryption workflow:**
    1. Paste the Base64 ciphertext in the input box.
    2. Enter the exact Base64 key used during encryption.
    3. Click **Decrypt**.

    **Common errors:**
    - *"Key must be 32 bytes"* → Your Base64 key decoded to the wrong length.
    - *"Decryption failed"* → Wrong key, or the ciphertext was modified/corrupted.
    - *"Not valid Base64"* → The ciphertext or key contains invalid characters.
    """)
