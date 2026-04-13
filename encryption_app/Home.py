"""
Home.py  –  Main Dashboard
Displays all cipher technique cards in a grid layout.
"""

import streamlit as st

st.set_page_config(
    page_title="CryptoVault – Encryption Suite",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────── Custom CSS ────────────────────────
st.markdown("""
<style>
    /* ── Global ── */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0d1117 !important;
        color: #e6edf3;
    }
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebar"] * { color: #c9d1d9 !important; }

    /* ── Headings ── */
    h1, h2, h3 { color: #e6edf3 !important; }

    /* ── Inputs / Text areas ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background-color: #161b22 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: #e6edf3 !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div > div { background-color: #161b22 !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #238636, #2ea043) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    /* ── Download button ── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1f6feb, #388bfd) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        background-color: #161b22 !important;
        border: 1px dashed rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
    }

    /* ── Code blocks ── */
    .stCode { background-color: #161b22 !important; border-radius: 8px !important; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; }
    .stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom-color: #58a6ff !important; }

    /* ── Metric ── */
    [data-testid="metric-container"] { background: #161b22; border-radius: 10px; padding: 0.75rem 1rem; }

    /* ── Expander ── */
    .streamlit-expanderHeader { background-color: #161b22 !important; border-radius: 8px !important; }

    /* ── Card style for home page ── */
    .cipher-card {
        background: linear-gradient(145deg, #161b22, #1c2128);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
        cursor: pointer;
    }
    .cipher-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    }
    .cipher-card h3 { margin: 0.5rem 0 0.3rem; font-size: 1.15rem; }
    .cipher-card p  { margin: 0; font-size: 0.88rem; color: #8b949e; line-height: 1.5; }
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-classic  { background:#2d333b; color:#8b949e; }
    .badge-modern   { background:#1f3a5f; color:#58a6ff; }
    .badge-asymm    { background:#2d1f3a; color:#bc8cff; }
    .badge-custom   { background:#1f3a2d; color:#3fb950; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────── Hero Header ────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0d1117 0%, #161b22 40%, #1c2128 100%);
    border: 1px solid rgba(88,166,255,0.2);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    text-align: center;
    margin-bottom: 2.5rem;
    box-shadow: 0 4px 40px rgba(88,166,255,0.08);
">
    <div style="font-size:3.5rem; margin-bottom:0.5rem;">🔐</div>
    <h1 style="margin:0; font-size:2.4rem; font-weight:800; color:#e6edf3; letter-spacing:-0.5px;">
        CryptoVault
    </h1>
    <p style="margin:0.6rem 0 0; color:#8b949e; font-size:1.05rem; max-width:520px; margin-left:auto; margin-right:auto;">
        A professional encryption suite supporting five cipher techniques —
        from classical to modern asymmetric cryptography.
    </p>
</div>
""", unsafe_allow_html=True)


# ──────────────────────── Metrics Row ────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Cipher Techniques", "5", help="Caesar, XOR, AES-256, RSA, Monoalphabetic")
m2.metric("AES Key Size", "256-bit", help="Industry-standard symmetric encryption")
m3.metric("RSA Key Size", "2048-bit", help="Secure asymmetric encryption")
m4.metric("File Support", "✅", help="Upload & download .txt files on every page")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🗂️ Choose a Cipher to Begin")
st.markdown("<p style='color:#8b949e; margin-top:-0.5rem;'>Select any technique below — each has its own dedicated page.</p>", unsafe_allow_html=True)

st.divider()

# ──────────────────────── Cipher Cards Grid ────────────────────────
CARDS = [
    {
        "icon": "🏛️",
        "name": "Caesar Cipher",
        "badge": "classic",
        "badge_label": "Classical",
        "desc": (
            "One of the oldest encryption techniques. Shifts each letter in the alphabet "
            "by a fixed number (1–25). Simple, educational, and historically significant."
        ),
        "features": ["Shift key (1–25)", "Case-preserving", "Non-alpha passthrough"],
        "page": "pages/1_Caesar_Cipher.py",
    },
    {
        "icon": "⊕",
        "name": "XOR Cipher",
        "badge": "classic",
        "badge_label": "Classical",
        "desc": (
            "A bitwise XOR operation against a numeric key (0–255). Symmetric by nature: "
            "the same operation encrypts and decrypts. Fast and simple."
        ),
        "features": ["Key range 0–255", "Symmetric operation", "Printable-safe output"],
        "page": "pages/2_XOR_Cipher.py",
    },
    {
        "icon": "🛡️",
        "name": "AES-256 Encryption",
        "badge": "modern",
        "badge_label": "Modern",
        "desc": (
            "Advanced Encryption Standard with a 256-bit key in CBC mode. "
            "Industry-standard symmetric encryption trusted by governments and enterprises worldwide."
        ),
        "features": ["256-bit key", "CBC mode + PKCS7", "Auto key generation"],
        "page": "pages/3_AES_Encryption.py",
    },
    {
        "icon": "🔑",
        "name": "RSA Encryption",
        "badge": "asymm",
        "badge_label": "Asymmetric",
        "desc": (
            "Public-key cryptography with 2048-bit keys. Encrypt with the public key, "
            "decrypt only with the private key. Ideal for secure key exchange."
        ),
        "features": ["2048-bit key pair", "OAEP + SHA-256", "Chunked for long text"],
        "page": "pages/4_RSA_Encryption.py",
    },
    {
        "icon": "🔀",
        "name": "Monoalphabetic Cipher",
        "badge": "custom",
        "badge_label": "Custom",
        "desc": (
            "Define your own substitution alphabet letter-by-letter. "
            "Each plaintext letter maps to a unique ciphertext letter. "
            "Build, preview, and manage your mapping interactively."
        ),
        "features": ["Custom letter mapping", "Duplicate prevention", "Interactive table"],
        "page": "pages/5_Monoalphabetic_Cipher.py",
    },
]

badge_colors = {
    "classic": "#2d333b",
    "modern": "#1f3a5f",
    "asymm": "#2d1f3a",
    "custom": "#1f3a2d",
}
badge_text = {
    "classic": "#8b949e",
    "modern": "#58a6ff",
    "asymm": "#bc8cff",
    "custom": "#3fb950",
}

# Render two columns of cards
col_a, col_b = st.columns(2)
columns = [col_a, col_b]

for idx, card in enumerate(CARDS):
    col = columns[idx % 2]
    with col:
        bc = badge_colors[card["badge"]]
        bt = badge_text[card["badge"]]
        features_html = "".join(
            f'<span style="background:#21262d;color:#8b949e;padding:2px 8px;border-radius:5px;font-size:0.78rem;margin-right:4px;">• {f}</span>'
            for f in card["features"]
        )
        st.markdown(f"""
        <div class="cipher-card">
            <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.6rem;">
                <span style="font-size:1.6rem;">{card['icon']}</span>
                <div>
                    <span style="background:{bc};color:{bt};padding:2px 10px;border-radius:20px;
                          font-size:0.7rem;font-weight:700;letter-spacing:0.5px;text-transform:uppercase;">
                        {card['badge_label']}
                    </span>
                </div>
            </div>
            <h3 style="color:#e6edf3;margin:0 0 0.4rem;">{card['name']}</h3>
            <p style="color:#8b949e;font-size:0.88rem;line-height:1.5;margin-bottom:0.8rem;">{card['desc']}</p>
            <div style="display:flex;flex-wrap:wrap;gap:4px;">{features_html}</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(card["page"], label=f"Open {card['name']} →", use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────── Footer ────────────────────────
st.divider()
st.markdown("""
<p style="text-align:center;color:#484f58;font-size:0.82rem;">
    CryptoVault • Built with Streamlit • AES-256 · RSA-2048 · Caesar · XOR · Monoalphabetic
</p>
""", unsafe_allow_html=True)
