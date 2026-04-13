"""
core/ui_utils.py
----------------
Shared Streamlit UI helpers used across pages.
"""

import streamlit as st


def page_header(title: str, subtitle: str, icon: str = "🔐") -> None:
    """Render a styled page header."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    ">
        <h1 style="margin:0; color:#e0e0e0; font-size:2rem; font-weight:700;">
            {icon} {title}
        </h1>
        <p style="margin:0.5rem 0 0; color:#a0aec0; font-size:1rem;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def success_box(message: str) -> None:
    st.markdown(f"""
    <div style="
        background: rgba(56,161,105,0.15);
        border: 1px solid #38a169;
        border-radius:10px;
        padding:1rem 1.2rem;
        color:#68d391;
        font-size:0.95rem;
        margin-top:0.5rem;
    ">✅ {message}</div>
    """, unsafe_allow_html=True)


def error_box(message: str) -> None:
    st.markdown(f"""
    <div style="
        background: rgba(245,101,101,0.15);
        border: 1px solid #e53e3e;
        border-radius:10px;
        padding:1rem 1.2rem;
        color:#fc8181;
        font-size:0.95rem;
        margin-top:0.5rem;
    ">❌ {message}</div>
    """, unsafe_allow_html=True)


def info_box(message: str) -> None:
    st.markdown(f"""
    <div style="
        background: rgba(66,153,225,0.15);
        border: 1px solid #4299e1;
        border-radius:10px;
        padding:1rem 1.2rem;
        color:#90cdf4;
        font-size:0.95rem;
        margin-top:0.5rem;
    ">ℹ️ {message}</div>
    """, unsafe_allow_html=True)


def warning_box(message: str) -> None:
    st.markdown(f"""
    <div style="
        background: rgba(236,201,75,0.15);
        border: 1px solid #ecc94b;
        border-radius:10px;
        padding:1rem 1.2rem;
        color:#f6e05e;
        font-size:0.95rem;
        margin-top:0.5rem;
    ">⚠️ {message}</div>
    """, unsafe_allow_html=True)


def result_area(label: str, content: str) -> None:
    """Display result in a styled code block."""
    st.markdown(f"**{label}**")
    st.code(content, language=None)


def file_upload_section(key: str = "file_upload", target_state_key: str | None = None) -> str | None:
    """
    Renders a file upload widget.
    Returns file content as string if a file is uploaded, else None.
    If target_state_key is provided, a newly uploaded file also populates
    that session-state field.
    """
    uploaded = st.file_uploader(
        "📁 Upload a text file (optional)",
        type=["txt"],
        key=key,
        help="Upload a .txt file to use its content as input."
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
            st.caption(f"✅ Loaded: `{uploaded.name}` ({len(content)} chars)")
            return content
        except Exception as e:
            error_box(f"Failed to read file: {e}")
    return None


def download_button(content: str, filename: str = "result.txt", label: str = "⬇️ Download Result") -> None:
    """Render a download button for result content."""
    if content:
        st.download_button(
            label=label,
            data=content.encode("utf-8"),
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )


def divider() -> None:
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.08); margin:1.5rem 0;'>", unsafe_allow_html=True)


def section_title(title: str) -> None:
    st.markdown(f"<h3 style='color:#a0aec0; font-size:1rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;'>{title}</h3>", unsafe_allow_html=True)
