"""
Shared Streamlit UI helpers used across pages.
"""

import streamlit as st


def apply_hacker_theme() -> None:
    """Apply a shared cyber-themed look across the app."""
    st.markdown(
        """
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top left, rgba(0, 255, 170, 0.12), transparent 28%),
                radial-gradient(circle at top right, rgba(0, 153, 255, 0.12), transparent 24%),
                linear-gradient(135deg, #030711 0%, #07111f 45%, #02050c 100%) !important;
            color: #e6f7ff;
        }
        [data-testid="stHeader"] {
            background: rgba(2, 5, 12, 0.65) !important;
        }
        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(3, 12, 24, 0.96) 0%, rgba(6, 18, 32, 0.98) 100%) !important;
            border-right: 1px solid rgba(0, 255, 170, 0.14);
        }
        [data-testid="stSidebar"] * { color: #cbe7f5 !important; }
        [data-testid="stAppViewContainer"] > .main::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(0, 255, 170, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 170, 0.05) 1px, transparent 1px);
            background-size: 42px 42px;
            opacity: 0.26;
            mix-blend-mode: screen;
        }
        h1, h2, h3, h4 { color: #f4feff !important; }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div,
        div[data-baseweb="select"] > div {
            background: rgba(6, 18, 32, 0.95) !important;
            border: 1px solid rgba(0, 255, 170, 0.14) !important;
            color: #e6f7ff !important;
            border-radius: 10px !important;
        }
        .stRadio label, .stCheckbox label, .stMarkdown, .stCaption, small {
            color: #b7d7e5 !important;
        }
        .stButton > button {
            background: linear-gradient(135deg, #00c27a, #00e5a8) !important;
            color: #02110b !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            box-shadow: 0 8px 24px rgba(0, 229, 168, 0.18) !important;
        }
        .stButton > button:hover { filter: brightness(1.05); }
        .stDownloadButton > button {
            background: linear-gradient(135deg, #00a3ff, #7cf6ff) !important;
            color: #02111b !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
        }
        [data-testid="stFileUploader"] {
            background: rgba(6, 18, 32, 0.92) !important;
            border: 1px dashed rgba(0, 255, 170, 0.28) !important;
            border-radius: 12px !important;
        }
        .stCode, code {
            background: rgba(7, 17, 31, 0.92) !important;
            border-radius: 10px !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(6, 18, 32, 0.9);
            border-radius: 10px;
        }
        .stTabs [data-baseweb="tab"] { color: #7cb7cf; }
        .stTabs [aria-selected="true"] {
            color: #7cf6ff !important;
            border-bottom-color: #00e5a8 !important;
        }
        [data-testid="metric-container"] {
            background: linear-gradient(180deg, rgba(7, 17, 31, 0.95), rgba(4, 12, 22, 0.95));
            border: 1px solid rgba(0, 255, 170, 0.12);
            border-radius: 14px;
            padding: 0.85rem 1rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.22);
        }
        .streamlit-expanderHeader {
            background: rgba(6, 18, 32, 0.88) !important;
            border: 1px solid rgba(0, 255, 170, 0.08) !important;
            border-radius: 10px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str, icon: str = "LOCK") -> None:
    """Render a shared page header."""
    st.markdown(
        f"""
        <div style="
            background:
                radial-gradient(circle at top right, rgba(124,246,255,0.22), transparent 28%),
                linear-gradient(135deg, rgba(5,18,34,0.96) 0%, rgba(4,12,24,0.98) 55%, rgba(2,7,17,1) 100%);
            padding: 2rem 2.5rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            border: 1px solid rgba(0,255,170,0.16);
            box-shadow: 0 14px 38px rgba(0,0,0,0.35);
        ">
            <div style="font-size:0.8rem; letter-spacing:0.24rem; text-transform:uppercase; color:#7cf6ff; margin-bottom:0.7rem;">
                CryptoForge Control Node
            </div>
            <h1 style="margin:0; color:#f4feff; font-size:2rem; font-weight:700;">
                {icon} {title}
            </h1>
            <p style="margin:0.5rem 0 0; color:#b7d7e5; font-size:1rem;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def success_box(message: str) -> None:
    st.markdown(
        f"""
        <div style="
            background: rgba(56, 161, 105, 0.15);
            border: 1px solid #38a169;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            color: #68d391;
            font-size: 0.95rem;
            margin-top: 0.5rem;
        ">SUCCESS {message}</div>
        """,
        unsafe_allow_html=True,
    )


def error_box(message: str) -> None:
    st.markdown(
        f"""
        <div style="
            background: rgba(245, 101, 101, 0.15);
            border: 1px solid #e53e3e;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            color: #fc8181;
            font-size: 0.95rem;
            margin-top: 0.5rem;
        ">ERROR {message}</div>
        """,
        unsafe_allow_html=True,
    )


def info_box(message: str) -> None:
    st.markdown(
        f"""
        <div style="
            background: rgba(66, 153, 225, 0.15);
            border: 1px solid #4299e1;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            color: #90cdf4;
            font-size: 0.95rem;
            margin-top: 0.5rem;
        ">INFO {message}</div>
        """,
        unsafe_allow_html=True,
    )


def warning_box(message: str) -> None:
    st.markdown(
        f"""
        <div style="
            background: rgba(236, 201, 75, 0.15);
            border: 1px solid #ecc94b;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            color: #f6e05e;
            font-size: 0.95rem;
            margin-top: 0.5rem;
        ">WARNING {message}</div>
        """,
        unsafe_allow_html=True,
    )


def result_area(label: str, content: str) -> None:
    """Display result in a styled code block."""
    st.markdown(f"**{label}**")
    st.code(content, language=None)


def file_upload_section(key: str = "file_upload", target_state_key: str | None = None) -> str | None:
    """Render a file upload widget and optionally sync its content to session state."""
    uploaded = st.file_uploader(
        "Upload a text file (optional)",
        type=["txt"],
        key=key,
        help="Upload a .txt file to use its content as input.",
    )
    if uploaded is not None:
        try:
            raw_bytes = uploaded.getvalue()
            content = raw_bytes.decode("utf-8")
            upload_signature = (uploaded.name, len(raw_bytes))
            signature_key = f"{key}__last_signature"
            if target_state_key and st.session_state.get(signature_key) != upload_signature:
                st.session_state[target_state_key] = content
                st.session_state[signature_key] = upload_signature
            st.caption(f"Loaded: `{uploaded.name}` ({len(content)} chars)")
            return content
        except Exception as exc:
            error_box(f"Failed to read file: {exc}")
    return None


def download_button(content: str, filename: str = "result.txt", label: str = "Download Result") -> None:
    """Render a download button for result content."""
    if content:
        st.download_button(
            label=label,
            data=content.encode("utf-8"),
            file_name=filename,
            mime="text/plain",
            use_container_width=True,
        )


def divider() -> None:
    st.markdown(
        "<hr style='border:1px solid rgba(0,255,170,0.10); margin:1.5rem 0;'>",
        unsafe_allow_html=True,
    )


def section_title(title: str) -> None:
    st.markdown(
        f"<h3 style='color:#7cf6ff; font-size:1rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;'>{title}</h3>",
        unsafe_allow_html=True,
    )


def about_section(title: str, body: str) -> None:
    """Render an in-page about panel."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(180deg, rgba(7,17,31,0.95), rgba(4,12,22,0.96));
            border: 1px solid rgba(0,255,170,0.12);
            border-radius: 16px;
            padding: 1.25rem 1.4rem;
            margin: 0.5rem 0 1rem;
            box-shadow: 0 10px 24px rgba(0,0,0,0.22);
        ">
            <div style="color:#7cf6ff; font-size:0.82rem; letter-spacing:0.18rem; text-transform:uppercase; margin-bottom:0.55rem;">
                About
            </div>
            <h3 style="margin:0 0 0.7rem; color:#f4feff;">{title}</h3>
            <div style="color:#cbe7f5; line-height:1.65; font-size:0.95rem;">
                {body}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_about(title: str, body: str) -> None:
    """Render the about block inside the left sidebar."""
    cleaned_parts = [part.strip() for part in body.replace("<br><br>", "\n\n").split("\n\n") if part.strip()]
    body_html = "".join(
        f"<p style='margin:0 0 0.8rem; color:#cbe7f5; line-height:1.6; font-size:0.88rem;'>{part}</p>"
        for part in cleaned_parts
    )
    with st.sidebar:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(180deg, rgba(7,17,31,0.96), rgba(4,12,22,0.98));
                border: 1px solid rgba(0,255,170,0.12);
                border-radius: 14px;
                padding: 1rem 1rem 0.95rem;
                margin-top: 1rem;
                box-shadow: 0 10px 24px rgba(0,0,0,0.20);
            ">
                <div style="color:#7cf6ff; font-size:0.74rem; letter-spacing:0.16rem; text-transform:uppercase; margin-bottom:0.45rem;">
                    About
                </div>
                <div style="color:#f4feff; font-size:1rem; font-weight:700; margin-bottom:0.55rem;">
                    {title}
                </div>
                {body_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
