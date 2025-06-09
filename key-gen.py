from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import json
import os
import shutil
from datetime import datetime

# Create users list including the Bank
users = [
    "Amy", "Bank", "Debangee", "James", "Kai",
    "Karim", "Kennedy", "Richa", "Yaras"
]

def backup_keys():
    """Backup existing keys.json with timestamp"""
    if os.path.exists("keys.json"):
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"keys_{timestamp}.json")
        shutil.copy2("keys.json", backup_path)
        print(f"Backup created: {backup_path}")
        return True
    return False

def restore_latest_backup():
    """Restore from most recent backup"""
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        print("No backups directory found")
        return False

    backups = [f for f in os.listdir(backup_dir) if f.startswith("keys_")]
    if not backups:
        print("No backups available")
        return False

    # Get most recent backup
    backups.sort(reverse=True)
    latest_backup = os.path.join(backup_dir, backups[0])
    shutil.copy2(latest_backup, "keys.json")
    print(f"Restored from: {latest_backup}")
    return True

def generate_keys():
    keys_data = {}
    for user in users:
        # Generate ECDSA key pair using SECP256K1
        private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        public_key = private_key.public_key()

        # Serialize keys
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        keys_data[user] = {
            "private_key": private_pem.strip(),
            "public_key": public_pem.strip()
        }

    # Save to keys.json
    with open("keys.json", "w") as f:
        json.dump(keys_data, f, indent=4)
    print("keys.json generated successfully!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Manage ECDSA keys")
    parser.add_argument("--restore", action="store_true", help="Restore keys from latest backup")
    args = parser.parse_args()

    if args.restore:
        restore_latest_backup()
    else:
        backup_keys()  # Always backup before generating new keys
        generate_keys()
