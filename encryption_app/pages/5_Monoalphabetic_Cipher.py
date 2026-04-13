"""
pages/5_Monoalphabetic_Cipher.py
Monoalphabetic Substitution Cipher – Interactive mapping builder
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import string
from textwrap import dedent
import streamlit as st
import streamlit.components.v1 as components
from core.ciphers import mono_encrypt, mono_decrypt, validate_mono_mapping
from core.ui_utils import (
    page_header, success_box, error_box, info_box, warning_box,
    result_area, file_upload_section, download_button, divider
)

st.set_page_config(page_title="Monoalphabetic Cipher | CryptoVault", page_icon="🔀", layout="wide")

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
/* Mapping table */
.map-table{width:100%;border-collapse:collapse;font-size:.9rem}
.map-table th{background:#1c2128;color:#8b949e;padding:8px 12px;text-align:left;border-bottom:1px solid rgba(255,255,255,.08);font-weight:600;text-transform:uppercase;letter-spacing:.5px;font-size:.75rem}
.map-table td{padding:8px 12px;border-bottom:1px solid rgba(255,255,255,.05);color:#e6edf3}
.map-table tr:hover td{background:rgba(255,255,255,.03)}
.letter-cell{font-family:monospace;font-size:1.1rem;font-weight:700}
.arrow-cell{color:#8b949e}
.mapped-cell{font-family:monospace;font-size:1.1rem;font-weight:700;color:#3fb950}
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

ALPHABET = list(string.ascii_uppercase)

# ── Session state ──
if "mono_mapping" not in st.session_state:
    st.session_state.mono_mapping = {}  # e.g. {'A': 'X', 'B': 'Q'}

page_header(
    "Monoalphabetic Cipher",
    "Build a custom substitution alphabet letter-by-letter. Each letter maps to a unique letter.",
    "🔀"
)

with st.sidebar:
    st.markdown("### 🔀 Monoalphabetic")
    st.markdown("""
    **How it works:**
    Each plaintext letter is replaced by a fixed ciphertext letter according to your custom mapping.

    **Rules:**
    - Each source letter maps to exactly **one** target
    - Each target letter can only be used **once** (no duplicates)
    - Unmapped letters pass through unchanged

    **Example:**
    ```
    A → X
    B → Q
    C → M
    ```
    `"ABC"` → `"XQM"`

    **Decryption:** Automatically reverses the mapping.
    """)
    st.divider()
    st.info("You don't need to map all 26 letters — unmapped letters appear unchanged in the output.")

# ──────────────────────── MAPPING BUILDER ────────────────────────
st.markdown("### 🛠️ Build Your Mapping")

mapping = st.session_state.mono_mapping
used_sources  = set(k.upper() for k in mapping.keys())
used_targets  = set(v.upper() for v in mapping.values())

available_sources = [l for l in ALPHABET if l not in used_sources]
available_targets = [l for l in ALPHABET if l not in used_targets]

col_add1, col_add2, col_add3, col_add4 = st.columns([1.2, 1.2, 0.8, 0.8])

with col_add1:
    st.markdown("<label style='color:#8b949e;font-size:.85rem;'>SOURCE letter (plaintext)</label>", unsafe_allow_html=True)
    src_letter = st.selectbox(
        "Source:",
        options=available_sources if available_sources else ["(none left)"],
        key="mono_src",
        label_visibility="collapsed"
    )

with col_add2:
    st.markdown("<label style='color:#8b949e;font-size:.85rem;'>TARGET letter (ciphertext)</label>", unsafe_allow_html=True)
    tgt_letter = st.selectbox(
        "Target:",
        options=available_targets if available_targets else ["(none left)"],
        key="mono_tgt",
        label_visibility="collapsed"
    )

with col_add3:
    st.markdown("<label style='color:transparent;font-size:.85rem;'>Add</label>", unsafe_allow_html=True)
    add_clicked = st.button("➕ Add Mapping", use_container_width=True, key="mono_add")

with col_add4:
    st.markdown("<label style='color:transparent;font-size:.85rem;'>Random</label>", unsafe_allow_html=True)
    if st.button("🎲 Random Full Map", use_container_width=True, key="mono_random"):
        import random
        shuffled = ALPHABET.copy()
        random.shuffle(shuffled)
        # Ensure no letter maps to itself (derangement-like)
        for i, letter in enumerate(ALPHABET):
            if shuffled[i] == letter:
                swap_idx = (i + 1) % 26
                shuffled[i], shuffled[swap_idx] = shuffled[swap_idx], shuffled[i]
        st.session_state.mono_mapping = {ALPHABET[i]: shuffled[i] for i in range(26)}
        st.rerun()

# Handle add
if add_clicked:
    src = src_letter.strip().upper() if src_letter != "(none left)" else ""
    tgt = tgt_letter.strip().upper() if tgt_letter != "(none left)" else ""

    if not src or not tgt:
        error_box("No available letters to map. All letters may already be assigned.")
    elif not src.isalpha() or len(src) != 1:
        error_box(f"Invalid source letter: '{src}'. Must be a single alphabet letter.")
    elif not tgt.isalpha() or len(tgt) != 1:
        error_box(f"Invalid target letter: '{tgt}'. Must be a single alphabet letter.")
    elif src in used_sources:
        error_box(f"'{src}' is already mapped. Remove it first to reassign.")
    elif tgt in used_targets:
        error_box(f"'{tgt}' is already used as a target. Each target letter can only appear once.")
    else:
        st.session_state.mono_mapping[src] = tgt
        success_box(f"Added: {src} → {tgt}")
        st.rerun()

divider()

# ──────────────────────── MAPPING TABLE ────────────────────────
st.markdown("### 📋 Current Mapping Table")

col_stats1, col_stats2, col_stats3 = st.columns(3)
col_stats1.metric("Mapped Letters", len(mapping), help="Letters with custom substitution")
col_stats2.metric("Unmapped Letters", 26 - len(mapping), help="These pass through unchanged")
col_stats3.metric("Coverage", f"{len(mapping)/26*100:.0f}%", help="Percentage of alphabet mapped")

st.markdown("<br>", unsafe_allow_html=True)

if mapping:
    # Build HTML table with remove buttons via form trick
    sorted_mapping = dict(sorted(mapping.items()))

    # Render mapping as a styled HTML table
    rows_html = ""
    for src, tgt in sorted_mapping.items():
        rev = {v: k for k, v in mapping.items()}
        rows_html += f"""
        <tr>
            <td class="letter-cell" style="color:#58a6ff;">{src}</td>
            <td class="arrow-cell">→</td>
            <td class="mapped-cell">{tgt}</td>
            <td class="arrow-cell">←</td>
            <td class="letter-cell" style="color:#58a6ff;">{rev.get(tgt, '?')}</td>
        </tr>
        """

    table_html = dedent(f"""
    <style>
    body {{
        margin: 0;
        background: transparent;
        color: #e6edf3;
        font-family: sans-serif;
    }}
    .map-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: .9rem;
    }}
    .map-table th {{
        background: #1c2128;
        color: #8b949e;
        padding: 8px 12px;
        text-align: left;
        border-bottom: 1px solid rgba(255,255,255,.08);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .5px;
        font-size: .75rem;
    }}
    .map-table td {{
        padding: 8px 12px;
        border-bottom: 1px solid rgba(255,255,255,.05);
        color: #e6edf3;
    }}
    .map-table tr:hover td {{
        background: rgba(255,255,255,.03);
    }}
    .letter-cell {{
        font-family: monospace;
        font-size: 1.1rem;
        font-weight: 700;
    }}
    .arrow-cell {{
        color: #8b949e;
    }}
    .mapped-cell {{
        font-family: monospace;
        font-size: 1.1rem;
        font-weight: 700;
        color: #3fb950;
    }}
    </style>
    <table class="map-table">
        <thead>
            <tr>
                <th>Plaintext</th>
                <th></th>
                <th>Ciphertext</th>
                <th></th>
                <th>Decrypt (reverse)</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    """).strip()
    table_height = min(560, max(180, 72 + len(sorted_mapping) * 36))
    components.html(table_html, height=table_height, scrolling=False)

    st.markdown("<br>", unsafe_allow_html=True)

    # Remove individual mapping
    col_rm1, col_rm2, col_rm3 = st.columns([2, 1, 1])
    with col_rm1:
        remove_letter = st.selectbox(
            "Remove a mapping:",
            options=sorted(mapping.keys()),
            key="mono_remove_select",
            label_visibility="visible"
        )
    with col_rm2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Remove", use_container_width=True, key="mono_remove_btn"):
            if remove_letter in st.session_state.mono_mapping:
                del st.session_state.mono_mapping[remove_letter]
                st.rerun()
    with col_rm3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧹 Clear All", use_container_width=True, key="mono_clear_map"):
            st.session_state.mono_mapping = {}
            st.rerun()

    # Export mapping
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📤 Export / Import Mapping"):
        import json
        mapping_json = json.dumps(st.session_state.mono_mapping, indent=2)
        st.code(mapping_json, language="json")
        download_button(mapping_json, "mono_mapping.json", "⬇️ Download Mapping")

        st.markdown("**Import mapping (JSON):**")
        imported = st.text_area("Paste JSON mapping:", height=100, key="mono_import_json", label_visibility="collapsed")
        if st.button("📥 Import", key="mono_import_btn"):
            try:
                parsed = json.loads(imported)
                if not isinstance(parsed, dict):
                    raise ValueError("Must be a JSON object.")
                # Validate
                new_map = {k.upper(): v.upper() for k, v in parsed.items()}
                validate_mono_mapping(new_map)
                st.session_state.mono_mapping = new_map
                success_box("Mapping imported successfully.")
                st.rerun()
            except (json.JSONDecodeError, ValueError) as e:
                error_box(f"Import failed: {e}")
else:
    info_box("No mappings yet. Add letter mappings above, or click 'Random Full Map' to auto-generate.")

divider()

# ──────────────────────── ENCRYPT / DECRYPT ────────────────────────
st.markdown("### 🔐 Encrypt / Decrypt")

if not mapping:
    warning_box("Add at least one letter mapping before encrypting/decrypting.")
else:
    file_upload_section(key="mono_upload", target_state_key="mono_input")

    st.markdown("#### 📝 Input Text")
    input_text = st.text_area(
        "Text:",
        height=150,
        placeholder="Enter text to encrypt or decrypt…",
        key="mono_input",
        label_visibility="collapsed"
    )

    # Live preview
    if input_text.strip() and mapping:
        try:
            preview_enc = mono_encrypt(input_text, mapping)
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid rgba(255,255,255,.08);border-radius:8px;
                        padding:.75rem 1rem;margin:.5rem 0;font-size:.88rem;color:#8b949e;">
                🔍 Live preview (encrypted): 
                <span style="color:#3fb950;font-family:monospace;">{preview_enc[:120]}{'…' if len(preview_enc) > 120 else ''}</span>
            </div>
            """, unsafe_allow_html=True)
        except Exception:
            pass

    divider()

    col_enc, col_dec, col_clr = st.columns(3)
    action = None
    result = None

    with col_enc:
        if st.button("🔒 Encrypt", use_container_width=True, key="mono_enc"):
            action = "encrypt"
    with col_dec:
        if st.button("🔓 Decrypt", use_container_width=True, key="mono_dec"):
            action = "decrypt"
    with col_clr:
        if st.button("🗑️ Clear Text", use_container_width=True, key="mono_clr"):
            st.session_state.mono_input = ""
            st.rerun()

    if action:
        try:
            if not input_text.strip():
                error_box("Input text cannot be empty.")
            else:
                if action == "encrypt":
                    result = mono_encrypt(input_text, mapping)
                    success_box(f"Encrypted using {len(mapping)} mapped substitutions.")
                else:
                    result = mono_decrypt(input_text, mapping)
                    success_box(f"Decrypted using {len(mapping)} reverse substitutions.")
        except ValueError as e:
            error_box(str(e))
        except Exception as e:
            error_box(f"Unexpected error: {e}")

    if result is not None:
        divider()
        st.markdown("#### 📤 Output")
        result_area("Result:", result)
        st.markdown("<br>", unsafe_allow_html=True)
        fname = "mono_encrypted.txt" if action == "encrypt" else "mono_decrypted.txt"
        download_button(result, filename=fname)

# ──────────────────────── INFO ────────────────────────
divider()
with st.expander("📖 About Monoalphabetic Ciphers"):
    st.markdown("""
    **What is it?**
    A monoalphabetic substitution cipher replaces each letter with another fixed letter.
    Unlike Caesar (which uses a formula), you define any arbitrary mapping.

    **Strength:**
    - More combinations than Caesar (26! ≈ 4 × 10²⁶ possible keys)
    - Still vulnerable to **frequency analysis** — common letters (E, T, A) leave statistical patterns

    **Historical use:** Used widely before the 20th century; broken by Al-Kindi (~850 AD)
    using frequency analysis.

    **Best practice for real security:** Use AES-256 or RSA instead.
    """)
