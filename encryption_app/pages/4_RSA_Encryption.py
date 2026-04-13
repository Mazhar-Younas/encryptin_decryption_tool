"""
pages/4_RSA_Encryption.py
RSA (2048-bit, OAEP+SHA-256) – Encrypt & Decrypt
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.ciphers import (
    rsa_encrypt, rsa_decrypt, generate_rsa_keypair
)
from core.ui_utils import (
    page_header, success_box, error_box, info_box, warning_box,
    result_area, file_upload_section, download_button, divider
)

st.set_page_config(page_title="RSA Encryption | CryptoVault", page_icon="🔑", layout="wide")

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
    "RSA Encryption",
    "Asymmetric 2048-bit key pair encryption. Encrypt with public key, decrypt with private key.",
    "🔑"
)

with st.sidebar:
    st.markdown("### 🔑 RSA")
    st.markdown("""
    **How it works:**
    - **Asymmetric**: different keys for encrypt/decrypt
    - Public key → encrypt
    - Private key → decrypt
    - Key size: **2048 bits**
    - Padding: **OAEP + SHA-256**

    **Long text:** Messages longer than ~190 bytes
    are automatically split into chunks.

    **Workflow:**
    1. Click **Generate Key Pair**
    2. Share your **public key** with the sender
    3. Keep your **private key** secret
    4. Decrypt received messages with your private key
    """)
    st.divider()
    st.warning("⚠️ NEVER share your private key. It decrypts all messages encrypted with your public key.")

# ── Session state ──
if "rsa_private_pem" not in st.session_state:
    st.session_state.rsa_private_pem = ""
if "rsa_public_pem" not in st.session_state:
    st.session_state.rsa_public_pem = ""
if "rsa_generating" not in st.session_state:
    st.session_state.rsa_generating = False

# ── Key Pair Generation ──
st.markdown("#### 🔐 RSA Key Pair")
col_gen, col_status = st.columns([1, 3])
with col_gen:
    if st.button("⚙️ Generate 2048-bit Key Pair", use_container_width=True, key="rsa_gen"):
        with st.spinner("Generating 2048-bit RSA key pair…"):
            priv, pub = generate_rsa_keypair()
            st.session_state.rsa_private_pem = priv
            st.session_state.rsa_public_pem = pub
        st.rerun()

if st.session_state.rsa_public_pem:
    with col_status:
        st.markdown("""
        <div style="background:rgba(63,185,80,0.12);border:1px solid #3fb950;border-radius:8px;
                    padding:.6rem 1rem;margin-top:.2rem;color:#3fb950;font-size:0.9rem;">
            ✅ Key pair generated and ready
        </div>
        """, unsafe_allow_html=True)

    key_tab1, key_tab2 = st.tabs(["🔓 Public Key", "🔒 Private Key"])
    with key_tab1:
        st.code(st.session_state.rsa_public_pem, language=None)
        download_button(st.session_state.rsa_public_pem, "rsa_public_key.pem", "⬇️ Download Public Key")
    with key_tab2:
        st.warning("⚠️ Keep this private key secret. Do not share it.")
        st.code(st.session_state.rsa_private_pem, language=None)
        download_button(st.session_state.rsa_private_pem, "rsa_private_key.pem", "⬇️ Download Private Key")
else:
    info_box("Click 'Generate Key Pair' to create your RSA keys, or paste existing keys below.")

divider()

# ── Mode Selection ──
st.markdown("#### 🔧 Mode")
mode = st.radio(
    "Select mode:",
    ["🔒 Encrypt (with Public Key)", "🔓 Decrypt (with Private Key)"],
    horizontal=True,
    key="rsa_mode",
    label_visibility="collapsed"
)

# ── File upload ──
file_upload_section(key="rsa_upload", target_state_key="rsa_input")

# ── Input Text ──
st.markdown("#### 📝 Input Text")
input_text = st.text_area(
    "Input:",
    height=150,
    placeholder="Plaintext to encrypt, or RSA ciphertext to decrypt…",
    key="rsa_input",
    label_visibility="collapsed"
)

# ── Key Input ──
if "Encrypt" in mode:
    st.markdown("#### 🔓 Public Key (PEM)")
    pub_key_input = st.text_area(
        "Public key:",
        value=st.session_state.rsa_public_pem,
        height=160,
        placeholder="-----BEGIN PUBLIC KEY-----\n…\n-----END PUBLIC KEY-----",
        key="rsa_pub_key_input",
        label_visibility="collapsed"
    )
    priv_key_input = ""
else:
    st.markdown("#### 🔒 Private Key (PEM)")
    priv_key_input = st.text_area(
        "Private key:",
        value=st.session_state.rsa_private_pem,
        height=200,
        placeholder="-----BEGIN PRIVATE KEY-----\n…\n-----END PRIVATE KEY-----",
        key="rsa_priv_key_input",
        label_visibility="collapsed",
        help="This is your secret private key. Never paste it in a public channel."
    )
    pub_key_input = ""

divider()

# ── Action Buttons ──
col_enc, col_clr = st.columns([1, 1])
action = None
result = None

with col_enc:
    btn_label = "🔒 Encrypt" if "Encrypt" in mode else "🔓 Decrypt"
    if st.button(btn_label, use_container_width=True, key="rsa_action"):
        action = mode
with col_clr:
    if st.button("🗑️ Clear", use_container_width=True, key="rsa_clr"):
        st.session_state.rsa_input = ""
        st.rerun()

if action:
    try:
        if not input_text.strip():
            error_box("Input text cannot be empty.")
        elif "Encrypt" in action:
            if not pub_key_input.strip():
                error_box("Public key is required for encryption. Generate or paste a PEM public key.")
            else:
                result = rsa_encrypt(input_text, pub_key_input)
                success_box("Encrypted successfully with RSA-2048 (OAEP + SHA-256).")
        else:
            if not priv_key_input.strip():
                error_box("Private key is required for decryption.")
            else:
                result = rsa_decrypt(input_text, priv_key_input)
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
    fname = "rsa_encrypted.txt" if "Encrypt" in mode else "rsa_decrypted.txt"
    download_button(result, filename=fname)

# ── Info ──
divider()
with st.expander("📖 RSA Usage Guide"):
    st.markdown("""
    **Secure communication scenario:**

    | Step | Person A (Sender) | Person B (Receiver) |
    |------|------------------|---------------------|
    | 1 | — | Generate key pair |
    | 2 | Receives B's **public key** | Shares **public key** |
    | 3 | Encrypts message with public key | — |
    | 4 | Sends ciphertext | Decrypts with **private key** |

    **Ciphertext format:** Each 190-byte chunk is base64-encoded and joined with `|` delimiters.

    **Long messages:** Automatically split into chunks — no action needed.

    **Limitations:** RSA is slow for large data. For big files, use RSA to encrypt an AES key,
    then use AES for the actual data (hybrid encryption).
    """)
