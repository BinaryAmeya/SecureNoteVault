import os
import json
import click
import base64
import hashlib
from cryptography.fernet import Fernet


VAULT_FILE = "vault.json"
MASTER_FILE = "master.hash"


def derive_key(password: str) -> bytes:
    """Derive a Fernet key from the master password"""
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)


def get_cipher(password: str):
    """Get Fernet cipher using password-derived key"""
    return Fernet(derive_key(password))


@click.group()
def cli():
    """🔐 Secure Note Vault — Master Password Edition"""
    pass


@cli.command()
def init():
    """Initialize a new secure vault with master password"""
    if os.path.exists(VAULT_FILE):
        click.echo("[!] Vault already exists.")
        return

    master_password = click.prompt("Create master password", hide_input=True, confirmation_prompt=True)
    hashed = hashlib.sha256(master_password.encode()).hexdigest()

    # Save password hash for verification
    with open(MASTER_FILE, "w") as f:
        f.write(hashed)

    # Initialize empty encrypted vault
    cipher = get_cipher(master_password)
    enc_data = cipher.encrypt(json.dumps([]).encode()).decode()
    with open(VAULT_FILE, "w") as f:
        f.write(enc_data)

    click.echo("✅ Vault created and encrypted with master password!")


def verify_master_password():
    """Verify the master password and return cipher"""
    if not os.path.exists(MASTER_FILE):
        raise click.ClickException("Vault not initialized. Run 'secure-note init' first.")

    master_password = click.prompt("Enter master password", hide_input=True)
    with open(MASTER_FILE, "r") as f:
        stored_hash = f.read().strip()

    if hashlib.sha256(master_password.encode()).hexdigest() != stored_hash:
        raise click.ClickException("❌ Incorrect master password.")

    return get_cipher(master_password)


def load_vault(cipher):
    """Decrypt vault data"""
    with open(VAULT_FILE, "r") as f:
        enc_data = f.read()
    dec = cipher.decrypt(enc_data.encode()).decode()
    return json.loads(dec)


def save_vault(cipher, notes):
    """Encrypt and save vault data"""
    enc = cipher.encrypt(json.dumps(notes).encode()).decode()
    with open(VAULT_FILE, "w") as f:
        f.write(enc)


@cli.command()
@click.option("--title", prompt="Note title", help="Title of the note")
@click.option("--body", prompt="Note body", help="Body of the note")
def add(title, body):
    """Add a secure note (requires master password)"""
    cipher = verify_master_password()
    notes = load_vault(cipher)
    notes.append({"title": title, "body": body})
    save_vault(cipher, notes)
    click.echo(f"[+] Note '{title}' added securely.")


@cli.command()
def list():
    """List notes (requires master password)"""
    cipher = verify_master_password()
    notes = load_vault(cipher)
    if not notes:
        click.echo("[!] No notes found.")
        return
    for i, note in enumerate(notes, start=1):
        click.echo(f"{i}. {note['title']}")


@cli.command()
@click.argument("index", type=int)
def read(index):
    """Read a note (requires master password)"""
    cipher = verify_master_password()
    notes = load_vault(cipher)
    try:
        note = notes[index - 1]
        click.echo(f"\n📜 {note['title']}\n{'-'*len(note['title'])}\n{note['body']}")
    except IndexError:
        click.echo("[!] Invalid note index.")


if __name__ == "__main__":
    cli()
