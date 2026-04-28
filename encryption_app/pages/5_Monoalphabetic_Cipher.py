"""
Monoalphabetic Substitution Cipher - Interactive mapping builder
"""

import json
import os
import random
import string
import sys
from textwrap import dedent

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.ciphers import mono_decrypt, mono_encrypt, validate_mono_mapping
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
    warning_box,
)

st.set_page_config(page_title="Monoalphabetic Cipher | CryptoForge", page_icon="MONO", layout="wide")
apply_hacker_theme()

st.markdown(
    """
    <style>
    .map-table{width:100%;border-collapse:collapse;font-size:.9rem}
    .map-table th{background:#102334;color:#7cb7cf;padding:8px 12px;text-align:left;border-bottom:1px solid rgba(0,255,170,.12);font-weight:600;text-transform:uppercase;letter-spacing:.5px;font-size:.75rem}
    .map-table td{padding:8px 12px;border-bottom:1px solid rgba(255,255,255,.05);color:#e6edf3}
    .map-table tr:hover td{background:rgba(255,255,255,.03)}
    .letter-cell{font-family:monospace;font-size:1.1rem;font-weight:700}
    .arrow-cell{color:#8fb4c7}
    .mapped-cell{font-family:monospace;font-size:1.1rem;font-weight:700;color:#00e5a8}
    </style>
    """,
    unsafe_allow_html=True,
)

ALPHABET = list(string.ascii_uppercase)

if "mono_mapping" not in st.session_state:
    st.session_state.mono_mapping = {}

page_header(
    "Monoalphabetic Cipher",
    "Build a custom substitution alphabet letter-by-letter and encrypt with your own mapping.",
    "MONO",
)

sidebar_about(
    "Monoalphabetic Cipher",
    """
    Each plaintext letter maps to one fixed ciphertext letter based on your custom substitution table.<br><br>
    Every target letter can only be used once, and unmapped letters pass through unchanged.<br><br>
    It is stronger than Caesar for learning purposes, but frequency analysis can still break it.
    """,
)

with st.container():
    st.markdown("#### Quick Notes")
    st.info("You do not need to map all 26 letters. Unmapped letters stay as they are.")
    st.warning("For real protection, use AES-256 or RSA instead of substitution ciphers.")

st.markdown("### Build Your Mapping")

mapping = st.session_state.mono_mapping
used_sources = set(k.upper() for k in mapping.keys())
used_targets = set(v.upper() for v in mapping.values())

available_sources = [letter for letter in ALPHABET if letter not in used_sources]
available_targets = [letter for letter in ALPHABET if letter not in used_targets]

col_add1, col_add2, col_add3, col_add4 = st.columns([1.2, 1.2, 0.8, 0.8])

with col_add1:
    src_letter = st.selectbox(
        "Source letter",
        options=available_sources if available_sources else ["(none left)"],
        key="mono_src",
    )
with col_add2:
    tgt_letter = st.selectbox(
        "Target letter",
        options=available_targets if available_targets else ["(none left)"],
        key="mono_tgt",
    )
with col_add3:
    st.markdown("<br>", unsafe_allow_html=True)
    add_clicked = st.button("Add Mapping", use_container_width=True, key="mono_add")
with col_add4:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Random Full Map", use_container_width=True, key="mono_random"):
        shuffled = ALPHABET.copy()
        random.shuffle(shuffled)
        for idx, letter in enumerate(ALPHABET):
            if shuffled[idx] == letter:
                swap_idx = (idx + 1) % 26
                shuffled[idx], shuffled[swap_idx] = shuffled[swap_idx], shuffled[idx]
        st.session_state.mono_mapping = {ALPHABET[idx]: shuffled[idx] for idx in range(26)}
        st.rerun()

if add_clicked:
    src = src_letter.strip().upper() if src_letter != "(none left)" else ""
    tgt = tgt_letter.strip().upper() if tgt_letter != "(none left)" else ""
    if not src or not tgt:
        error_box("No available letters to map.")
    elif src in used_sources:
        error_box(f"{src} is already mapped.")
    elif tgt in used_targets:
        error_box(f"{tgt} is already used as a target.")
    else:
        st.session_state.mono_mapping[src] = tgt
        success_box(f"Added mapping {src} -> {tgt}.")
        st.rerun()

divider()

st.markdown("### Current Mapping Table")
col_stats1, col_stats2, col_stats3 = st.columns(3)
col_stats1.metric("Mapped Letters", len(mapping))
col_stats2.metric("Unmapped Letters", 26 - len(mapping))
col_stats3.metric("Coverage", f"{len(mapping) / 26 * 100:.0f}%")

st.markdown("<br>", unsafe_allow_html=True)

if mapping:
    sorted_mapping = dict(sorted(mapping.items()))
    reverse_mapping = {value: key for key, value in mapping.items()}
    rows_html = ""
    for src, tgt in sorted_mapping.items():
        rows_html += f"""
        <tr>
            <td class="letter-cell" style="color:#7cf6ff;">{src}</td>
            <td class="arrow-cell">-></td>
            <td class="mapped-cell">{tgt}</td>
            <td class="arrow-cell"><-</td>
            <td class="letter-cell" style="color:#7cf6ff;">{reverse_mapping.get(tgt, '?')}</td>
        </tr>
        """

    table_html = dedent(
        f"""
        <style>
        body {{ margin: 0; background: transparent; color: #e6edf3; font-family: sans-serif; }}
        .map-table {{ width: 100%; border-collapse: collapse; font-size: .9rem; }}
        .map-table th {{ background: #102334; color: #7cb7cf; padding: 8px 12px; text-align: left; border-bottom: 1px solid rgba(0,255,170,.12); font-weight: 600; text-transform: uppercase; letter-spacing: .5px; font-size: .75rem; }}
        .map-table td {{ padding: 8px 12px; border-bottom: 1px solid rgba(255,255,255,.05); color: #e6edf3; }}
        .mapped-cell {{ font-family: monospace; font-size: 1.1rem; font-weight: 700; color: #00e5a8; }}
        .letter-cell {{ font-family: monospace; font-size: 1.1rem; font-weight: 700; }}
        .arrow-cell {{ color: #8fb4c7; }}
        </style>
        <table class="map-table">
            <thead>
                <tr>
                    <th>Plaintext</th>
                    <th></th>
                    <th>Ciphertext</th>
                    <th></th>
                    <th>Decrypt</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        """
    ).strip()
    table_height = min(560, max(180, 72 + len(sorted_mapping) * 36))
    components.html(table_html, height=table_height, scrolling=False)

    st.markdown("<br>", unsafe_allow_html=True)
    col_rm1, col_rm2, col_rm3 = st.columns([2, 1, 1])
    with col_rm1:
        remove_letter = st.selectbox("Remove a mapping", options=sorted(mapping.keys()), key="mono_remove_select")
    with col_rm2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Remove", use_container_width=True, key="mono_remove_btn"):
            del st.session_state.mono_mapping[remove_letter]
            st.rerun()
    with col_rm3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear All", use_container_width=True, key="mono_clear_map"):
            st.session_state.mono_mapping = {}
            st.rerun()

    with st.expander("Export / Import Mapping"):
        mapping_json = json.dumps(st.session_state.mono_mapping, indent=2)
        st.code(mapping_json, language="json")
        download_button(mapping_json, "mono_mapping.json", "Download Mapping")
        imported = st.text_area("Paste JSON mapping:", height=100, key="mono_import_json")
        if st.button("Import", key="mono_import_btn"):
            try:
                parsed = json.loads(imported)
                if not isinstance(parsed, dict):
                    raise ValueError("Mapping must be a JSON object.")
                new_map = {k.upper(): v.upper() for k, v in parsed.items()}
                validate_mono_mapping(new_map)
                st.session_state.mono_mapping = new_map
                success_box("Mapping imported successfully.")
                st.rerun()
            except (json.JSONDecodeError, ValueError) as exc:
                error_box(f"Import failed: {exc}")
else:
    info_box("No mappings yet. Add mappings above or generate a random full map.")

divider()

st.markdown("### Encrypt / Decrypt")
if not mapping:
    warning_box("Add at least one letter mapping before encrypting or decrypting.")
else:
    file_upload_section(key="mono_upload", target_state_key="mono_input")
    input_text = st.text_area(
        "Text:",
        height=150,
        placeholder="Enter text to encrypt or decrypt...",
        key="mono_input",
        label_visibility="collapsed",
    )

    if input_text.strip():
        preview_enc = mono_encrypt(input_text, mapping)
        st.markdown(
            f"""
            <div style="background:rgba(6,18,32,0.92);border:1px solid rgba(0,255,170,0.10);border-radius:10px;
                        padding:.8rem 1rem;margin:.5rem 0;font-size:.9rem;color:#b7d7e5;">
                Live preview:
                <span style="color:#00e5a8;font-family:monospace;">{preview_enc[:120]}{'...' if len(preview_enc) > 120 else ''}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    divider()

    col_enc, col_dec, col_clr = st.columns(3)
    action = None
    result = None
    with col_enc:
        if st.button("Encrypt", use_container_width=True, key="mono_enc"):
            action = "encrypt"
    with col_dec:
        if st.button("Decrypt", use_container_width=True, key="mono_dec"):
            action = "decrypt"
    with col_clr:
        if st.button("Clear Text", use_container_width=True, key="mono_clr"):
            st.session_state.mono_input = ""
            st.rerun()

    if action:
        try:
            if not input_text.strip():
                error_box("Input text cannot be empty.")
            elif action == "encrypt":
                result = mono_encrypt(input_text, mapping)
                success_box(f"Encrypted using {len(mapping)} mapped substitutions.")
            else:
                result = mono_decrypt(input_text, mapping)
                success_box(f"Decrypted using {len(mapping)} reverse substitutions.")
        except ValueError as exc:
            error_box(str(exc))
        except Exception as exc:
            error_box(f"Unexpected error: {exc}")

    if result is not None:
        divider()
        st.markdown("#### Output")
        result_area("Result:", result)
        st.markdown("<br>", unsafe_allow_html=True)
        filename = "mono_encrypted.txt" if action == "encrypt" else "mono_decrypted.txt"
        download_button(result, filename=filename)
