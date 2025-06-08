from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import json


# Create users list including the Bank
users = [
    "Amy",
    "Bank",
    "Debangee",
    "James",
    "Kai",
    "Karim",
    "Kennedy",
    "Richa",
    "Yaras"
]


keys_data = {}

for user in users:
    # Generate ECDSA key pair using SECP256K1 (Bitcoin/Ethereum curve)
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    public_key = private_key.public_key()

    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    # Serialize public key
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
