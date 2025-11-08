# 🔐 Secure Note Vault – Professional Edition
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.12%2B-yellow)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![CLI Tool](https://img.shields.io/badge/type-CLI-lightgrey)

> **A CLI-based encrypted note manager** built in Python.  
> Your notes are protected with AES-grade encryption derived from a **master password** — accessible only through your command line.

---

## 🧠 Overview

**Secure Note Vault Pro** is a professional-grade tool that lets you:
- Create a **master password–protected** encrypted note vault  
- Add, list, and read notes securely  
- Store data in AES-encrypted form (using `cryptography.Fernet`)  
- Run directly via command-line (`secure-note`)  
- Perfect for cybersecurity, privacy, or ethical hacking portfolios 💻  

---

## ⚙️ Tech Stack

| Component | Description |
|------------|--------------|
| **Language** | Python 3.12 |
| **Libraries** | `click`, `cryptography` |
| **CLI Framework** | Click (for terminal commands) |
| **Encryption** | AES (via Fernet) |
| **Storage** | Local encrypted JSON file |
| **Platform** | Windows / Linux / macOS |

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/BinaryAmeya/SecureNoteVault.git
cd SecureNoteVault
