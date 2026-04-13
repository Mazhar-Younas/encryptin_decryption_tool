# 🔐 CryptoVault — Encryption Suite

A professional **Streamlit** web app supporting five cipher techniques:
Caesar, XOR, AES-256, RSA-2048, and a custom Monoalphabetic cipher.

---

## 📁 Project Structure

```
encryption_app/
├── Home.py                        # Main dashboard (entry point)
├── requirements.txt
├── .streamlit/
│   └── config.toml               # Dark theme config
├── core/
│   ├── __init__.py
│   ├── ciphers.py                # All encryption logic
│   └── ui_utils.py               # Shared Streamlit UI helpers
└── pages/
    ├── 1_Caesar_Cipher.py
    ├── 2_XOR_Cipher.py
    ├── 3_AES_Encryption.py
    ├── 4_RSA_Encryption.py
    └── 5_Monoalphabetic_Cipher.py
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or with a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run Home.py
```

The app opens at **http://localhost:8501** in your browser.

---

## 🔑 Cipher Reference

| Cipher | Key | Mode | Notes |
|--------|-----|------|-------|
| Caesar | Shift 1–25 | Symmetric | Brute-force panel included |
| XOR | Integer 0–255 | Symmetric | Same op encrypts & decrypts |
| AES-256 | 32-byte Base64 | Symmetric CBC | Auto key generation; PKCS7 padding |
| RSA | 2048-bit PEM key pair | Asymmetric | OAEP+SHA-256; chunked for long text |
| Monoalphabetic | Custom letter mapping | Symmetric | Interactive builder; import/export JSON |

---

## 📦 Dependencies

- `streamlit >= 1.32`
- `cryptography >= 42.0` (provides AES, RSA, OAEP, PKCS7)

---

## ✅ Features

- ✅ Dark professional UI
- ✅ File upload (`.txt`) on every cipher page
- ✅ Download result button on every page
- ✅ Robust error handling with user-friendly messages
- ✅ AES auto key generation + copy/download
- ✅ RSA key pair generation + PEM download
- ✅ Monoalphabetic interactive mapping with duplicate prevention
- ✅ Import/export mapping as JSON
- ✅ Random full-alphabet derangement for monoalphabetic
- ✅ Caesar brute-force panel (all 25 shifts)
- ✅ XOR character-level demo
- ✅ Live preview on monoalphabetic page
