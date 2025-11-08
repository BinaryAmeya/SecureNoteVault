import os
import json
import base64
from cryptography.fernet import Fernet

VAULT_FILE = "vault.json"
KEY_FILE = "vault.key"


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key


def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()


def init_vault():
    if os.path.exists(VAULT_FILE):
        print("[!] Vault already exists.")
        return
    key = generate_key()
    cipher = Fernet(key)
    notes = {}
    with open(VAULT_FILE, "w") as vault:
        vault.write(json.dumps(notes))
    print("[OK] Secure Note Vault initialized.")


def add_note():
    key = load_key()
    cipher = Fernet(key)
    title = input("Enter note title: ")
    content = input("Enter note content: ")
    enc_content = cipher.encrypt(content.encode()).decode()
    notes = load_notes()
    notes[title] = enc_content
    save_notes(notes)
    print(f"[+] Note '{title}' added securely.")


def load_notes():
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "r") as f:
        return json.load(f)


def save_notes(notes):
    with open(VAULT_FILE, "w") as f:
        json.dump(notes, f, indent=2)


def view_notes():
    key = load_key()
    cipher = Fernet(key)
    notes = load_notes()
    if not notes:
        print("[!] No notes found.")
        return
    print("\n📒 Your Secure Notes:")
    for title, enc_content in notes.items():
        try:
            content = cipher.decrypt(enc_content.encode()).decode()
            print(f"\n{title}:\n{content}")
        except:
            print(f"\n{title}: [Decryption Failed]")


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: secure_note.py [init|add|view]")
        return
    cmd = sys.argv[1].lower()
    if cmd == "init":
        init_vault()
    elif cmd == "add":
        add_note()
    elif cmd == "view":
        view_notes()
    else:
        print("[!] Unknown command.")


if __name__ == "__main__":
    main()
