"""
pages/6_Playfair_Cipher.py
Playfair Cipher - Encrypt & Decrypt
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.ciphers import (
    generate_playfair_matrix,
    playfair_encrypt,
    playfair_decrypt,
)
from core.ui_utils import (
    page_header, success_box, error_box, info_box,
    result_area, file_upload_section, download_button, divider
)

st.set_page_config(page_title="Playfair Cipher | CryptoVault", page_icon="🗝️", layout="wide")

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
    "Playfair Cipher",
    "Encrypt digraphs using a 5x5 keyword matrix with merged I/J and rectangle-based substitution.",
    "🗝️"
)

with st.sidebar:
    st.markdown("### 🗝️ Playfair Cipher")
    st.markdown("""
    **How it works:**
    A keyword builds a 5x5 matrix of letters. Text is encrypted in pairs.

    **Rules:**
    - `I` and `J` share one cell
    - Repeated letters in a pair get split with `X`
    - Odd-length plaintext gets a trailing `X`
    - Same row -> shift right for encryption, left for decryption
    - Same column -> shift down for encryption, up for decryption
    - Rectangle -> swap columns

    **Input note:** Only alphabet letters and spaces are accepted.
    """)
    st.divider()
    st.info("Spaces are removed before processing, and results are returned in uppercase digraph form.")


def _prepare_preview_text(raw_text: str) -> tuple[str | None, str | None]:
    """Return normalized preview text or an error for display."""
    if not raw_text or not raw_text.strip():
        return None, None

    if any(not (char.isalpha() or char.isspace()) for char in raw_text):
        return None, "Input text must contain only alphabet letters and spaces."

    normalized = ''.join(raw_text.upper().split()).replace('J', 'I')
    if not normalized:
        return None, None
    return normalized, None


file_upload_section(key="playfair_upload", target_state_key="playfair_input")

st.markdown("#### 📝 Input Text")
input_text = st.text_area(
    "Enter text to encrypt or decrypt:",
    height=150,
    placeholder="Type or paste your text here...",
    key="playfair_input",
    label_visibility="collapsed"
)

st.markdown("#### 🔑 Key")
col_key, col_info = st.columns([1.2, 2.8])
with col_key:
    key = st.text_input(
        "Keyword:",
        placeholder="Enter alphabetic keyword",
        key="playfair_key",
        label_visibility="collapsed"
    )
with col_info:
    if key.strip():
        try:
            matrix, _ = generate_playfair_matrix(key)
            matrix_preview = ' | '.join(' '.join(row) for row in matrix)
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid rgba(255,255,255,.08);border-radius:8px;
                        padding:.75rem 1rem;margin-top:0.2rem;color:#8b949e;font-size:0.9rem;">
                Key = <b style='color:#58a6ff'>{''.join(key.upper().split()).replace('J', 'I')}</b> &nbsp;|&nbsp;
                Matrix = <b style='color:#3fb950;font-family:monospace'>{matrix_preview}</b>
            </div>
            """, unsafe_allow_html=True)
        except ValueError as exc:
            error_box(str(exc))
    else:
        info_box("Enter a keyword to generate the Playfair matrix.")

preview_text, preview_error = _prepare_preview_text(input_text)
if preview_error:
    error_box(preview_error)
elif preview_text:
    st.markdown(f"""
    <div style="background:#161b22;border:1px solid rgba(255,255,255,.08);border-radius:8px;
                padding:.75rem 1rem;margin:.75rem 0 0;color:#8b949e;font-size:0.9rem;">
        Prepared text preview = <b style='color:#f97316;font-family:monospace'>{preview_text}</b>
    </div>
    """, unsafe_allow_html=True)

divider()

col_enc, col_dec, col_clr = st.columns([1, 1, 1])
result = None
action = None

with col_enc:
    if st.button("🔒 Encrypt", use_container_width=True, key="playfair_enc"):
        action = "encrypt"
with col_dec:
    if st.button("🔓 Decrypt", use_container_width=True, key="playfair_dec"):
        action = "decrypt"
with col_clr:
    if st.button("🗑️ Clear", use_container_width=True, key="playfair_clr"):
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
    except ValueError as e:
        error_box(str(e))
    except Exception as e:
        error_box(f"Unexpected error: {e}")

if result is not None:
    divider()
    st.markdown("#### 📤 Output")
    result_area("Result:", result)
    st.markdown("<br>", unsafe_allow_html=True)
    download_button(result, filename="playfair_result.txt")

divider()
with st.expander("📖 About Playfair Cipher"):
    st.markdown("""
    **What is it?**
    The Playfair cipher is a classical digraph substitution cipher that encrypts
    pairs of letters instead of single letters.

    **Why it matters:**
    - Hides simple single-letter frequency patterns better than Caesar
    - Still considered educational, not secure for modern use
    - Depends on both the keyword and letter-pair structure

    **Reminder:**
    Decryption now removes common filler `X` characters automatically so the
    result is closer to the original plaintext.
    """)
