"""
Main dashboard for CryptoForge.
"""

import streamlit as st

from core.ui_utils import apply_hacker_theme

st.set_page_config(
    page_title="CryptoForge | Encryption Suite",
    page_icon="CF",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_hacker_theme()

st.markdown(
    """
    <style>
    .hero-shell {
        background:
            radial-gradient(circle at top right, rgba(124,246,255,0.20), transparent 25%),
            radial-gradient(circle at bottom left, rgba(0,229,168,0.16), transparent 26%),
            linear-gradient(135deg, rgba(5,18,34,0.98) 0%, rgba(4,12,24,0.98) 48%, rgba(2,7,17,1) 100%);
        border: 1px solid rgba(0,255,170,0.15);
        border-radius: 24px;
        padding: 3rem 2.4rem;
        margin-bottom: 2rem;
        box-shadow: 0 18px 45px rgba(0,0,0,0.34);
    }
    .hero-kicker {
        color: #7cf6ff;
        text-transform: uppercase;
        letter-spacing: 0.28rem;
        font-size: 0.8rem;
        margin-bottom: 0.8rem;
    }
    .hero-title {
        margin: 0;
        color: #f4feff;
        font-size: 2.85rem;
        font-weight: 800;
    }
    .hero-tagline {
        color: #00e5a8;
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0.8rem 0 0.3rem;
    }
    .hero-copy {
        color: #b7d7e5;
        font-size: 1rem;
        line-height: 1.7;
        max-width: 760px;
    }
    .category-shell {
        background: linear-gradient(180deg, rgba(7,17,31,0.95), rgba(4,12,22,0.96));
        border: 1px solid rgba(0,255,170,0.12);
        border-radius: 18px;
        padding: 1.3rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 12px 32px rgba(0,0,0,0.24);
    }
    .category-label {
        color: #7cf6ff;
        text-transform: uppercase;
        letter-spacing: 0.18rem;
        font-size: 0.8rem;
        margin-bottom: 0.4rem;
    }
    .category-desc {
        color: #a9c9d8;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    .cipher-card {
        background: linear-gradient(145deg, rgba(8,23,38,0.98), rgba(5,14,24,0.98));
        border: 1px solid rgba(124,246,255,0.12);
        border-radius: 16px;
        padding: 1.1rem;
        min-height: 220px;
        margin-bottom: 0.8rem;
    }
    .cipher-name {
        color: #f4feff;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .cipher-copy {
        color: #b7d7e5;
        line-height: 1.6;
        font-size: 0.92rem;
        min-height: 96px;
    }
    .chip {
        display: inline-block;
        margin: 0.1rem 0.25rem 0.1rem 0;
        padding: 0.22rem 0.55rem;
        border-radius: 999px;
        background: rgba(0,255,170,0.10);
        border: 1px solid rgba(0,255,170,0.10);
        color: #9cefd0;
        font-size: 0.74rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-kicker">Cipher Operations Hub</div>
        <h1 class="hero-title">CryptoForge</h1>
        <p class="hero-tagline">Master the Art of Cryptography</p>
        <p class="hero-copy">
            Explore encryption techniques in organized sections. Open any category below and then jump into
            the technique you want to use, from foundational classroom ciphers to practical modern cryptography.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Cipher Techniques", "6")
m2.metric("Classical", "4")
m3.metric("Symmetric", "1")
m4.metric("Asymmetric", "1")

st.markdown("### Choose a Cipher to Begin")
st.markdown(
    "<p style='color:#a9c9d8; margin-top:-0.4rem;'>Techniques are grouped by category so each section opens with its related tools.</p>",
    unsafe_allow_html=True,
)

SECTIONS = [
    {
        "title": "Classical Ciphers",
        "description": "Historic and educational techniques focused on substitution, shifting, and pair-based encryption.",
        "items": [
            {
                "icon": "CC",
                "name": "Caesar Cipher",
                "desc": "Shift each letter by a fixed key. Great for understanding the basics of alphabet rotation.",
                "features": ["Shift 1-25", "Fast", "Educational"],
                "page": "pages/1_Caesar_Cipher.py",
            },
            {
                "icon": "XO",
                "name": "XOR Cipher",
                "desc": "Apply a numeric key with bitwise XOR. Lightweight and symmetric, useful for simple demonstrations.",
                "features": ["Key 0-255", "Symmetric", "Bitwise"],
                "page": "pages/2_XOR_Cipher.py",
            },
            {
                "icon": "PF",
                "name": "Playfair Cipher",
                "desc": "Encrypt letter pairs with a keyword matrix and rectangle rules for a stronger classical pattern.",
                "features": ["Digraph", "5x5 matrix", "Keyword based"],
                "page": "pages/6_Playfair_Cipher.py",
            },
            {
                "icon": "MC",
                "name": "Monoalphabetic Cipher",
                "desc": "Create your own one-to-one substitution map and test custom alphabet remapping interactively.",
                "features": ["Custom map", "Interactive", "Substitution"],
                "page": "pages/5_Monoalphabetic_Cipher.py",
            },
        ],
    },
    {
        "title": "Symmetric Encryption",
        "description": "Modern shared-key encryption where the same secret is used for both encryption and decryption.",
        "items": [
            {
                "icon": "A256",
                "name": "AES-256 Encryption",
                "desc": "Industry-standard encryption with a 256-bit key for securing text using strong modern cryptography.",
                "features": ["256-bit", "CBC mode", "Secure key"],
                "page": "pages/3_AES_Encryption.py",
            }
        ],
    },
    {
        "title": "Asymmetric Encryption",
        "description": "Public-key cryptography for secure exchange, where encryption and decryption use different keys.",
        "items": [
            {
                "icon": "RSA",
                "name": "RSA Encryption",
                "desc": "Use a public key to encrypt and a private key to decrypt with 2048-bit asymmetric protection.",
                "features": ["2048-bit", "Public/private", "OAEP"],
                "page": "pages/4_RSA_Encryption.py",
            }
        ],
    },
]

for section in SECTIONS:
    with st.expander(f"{section['title']}", expanded=True):
        st.markdown(
            f"""
            <div class="category-shell">
                <div class="category-label">Technique Group</div>
                <h3 style="margin:0 0 0.35rem; color:#f4feff;">{section['title']}</h3>
                <div class="category-desc">{section['description']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        cols = st.columns(2)
        for idx, item in enumerate(section["items"]):
            with cols[idx % 2]:
                features = "".join(f"<span class='chip'>{feature}</span>" for feature in item["features"])
                st.markdown(
                    f"""
                    <div class="cipher-card">
                        <div style="color:#00e5a8; font-size:0.78rem; letter-spacing:0.15rem; text-transform:uppercase;">
                            {item['icon']}
                        </div>
                        <div class="cipher-name">{item['name']}</div>
                        <div class="cipher-copy">{item['desc']}</div>
                        <div>{features}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.page_link(item["page"], label=f"Open {item['name']}", use_container_width=True)

st.divider()
st.markdown(
    """
    <p style="text-align:center;color:#6f97a9;font-size:0.85rem;">
        CryptoForge • Built with Streamlit • Classical + Modern Encryption Workspace
    </p>
    """,
    unsafe_allow_html=True,
)
