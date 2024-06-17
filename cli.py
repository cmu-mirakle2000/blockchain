import argparse
import requests
import json
from ecdsa import SigningKey

node_url = "http://127.0.0.1:8000"

local_controller_url = None
nodes = [
    node_url
]
difficulty = 2
node_nickname = ""

# Load keys from JSON file
with open('keys.json', 'r') as f:
    HARDCODED_KEYS = json.load(f)

def set_difficulty(new_difficulty):
    global difficulty
    difficulty = int(new_difficulty)

    configuration = {
        'nodes': nodes,
        'master_controller': local_controller_url,
        'difficulty': difficulty,
        'reset' : 0
    }
    try:
        response = requests.post(f'{node_url}/configure', json=configuration)
        if response.status_code == 201:
            response_data = response.json()
            node_nickname = response_data.get('nickname')
            print(f"Configuration sent to node {node_url}, nickname: {node_nickname}")
        else:
            print(f"Failed to configure node {node_url}: {response.status_code}")
    except Exception as e:
        print(f"Error configuring node {node_url}: {e}")
    print({'status': 'configuration sent to nodes', 'nodes': node_nickname})

def reset():

    configuration = {
        'nodes': nodes,
        'master_controller': local_controller_url,
        'difficulty': difficulty,
        'reset': 1
    }
    try:
        response = requests.post(f'{node_url}/configure', json=configuration)
        if response.status_code == 201:
            response_data = response.json()
            node_nickname = response_data.get('nickname')
            print(f"Reset configuration sent to node {node_url}, nickname: {node_nickname}")
        else:
            print(f"Failed to reset configure node {node_url}: {response.status_code}")
    except Exception as e:
        print(f"Error reset configuring node {node_url}: {e}")
    print({'status': 'reset configuration sent to nodes', 'nodes': node_nickname})

def post_transaction(sender, recipient, amount):
    # Generate signature using sender's private key
    private_key_pem = HARDCODED_KEYS[sender]['private_key']
    private_key = SigningKey.from_pem(private_key_pem)
    transaction_data = f"{sender}{recipient}{amount}".encode()
    signature = private_key.sign(transaction_data).hex()

    url = f"{node_url}/transactions"
    payload = {
        "transaction": {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "signature": signature
        },
        "sender" : node_nickname
    }
    response = requests.post(url, json=payload)
    print(json.dumps(response.json(), indent=4))

def get_users():
    url = f"{node_url}/users"
    response = requests.get(url)
    print(json.dumps(response.json(), indent=4))

def get_chain():
    url = f"{node_url}/chain"
    response = requests.get(url)
    print(json.dumps(response.json(), indent=4))

def get_configuration():
    url = f"{node_url}/configuration"
    response = requests.get(url)
    print(response.json())

def main():
    parser = argparse.ArgumentParser(description="CLI for Master Controller")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for setting difficulty
    set_difficulty_parser = subparsers.add_parser("difficulty")
    set_difficulty_parser.add_argument("difficulty", type=int, help="Difficulty level for mining")

    # Subparser for configuring nodes
    config_parser = subparsers.add_parser("reset")

    # Subparser for posting transaction
    trans_parser = subparsers.add_parser("transaction")
    trans_parser.add_argument("sender", type=str, help="Sender of the transaction")
    trans_parser.add_argument("recipient", type=str, help="Recipient of the transaction")
    trans_parser.add_argument("amount", type=int, help="Amount of the transaction")

    # Subparser for getting users
    users_parser = subparsers.add_parser("users")

    # Subparser for getting blockchain
    chain_parser = subparsers.add_parser("chain")

    args = parser.parse_args()

    if args.command == "difficulty":
        set_difficulty(args.difficulty)
    elif args.command == "reset":
        reset()
    elif args.command == "transaction":
        post_transaction(args.sender, args.recipient, args.amount)
    elif args.command == "users":
        get_users()
    elif args.command == "chain":
        get_chain()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
