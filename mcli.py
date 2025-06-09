import argparse
import requests
import json
from ecdsa import SigningKey

MASTER_CONTROLLER_URL = "http://127.0.0.1:8001"

# Load keys from JSON file
with open('keys.json', 'r') as f:
    HARDCODED_KEYS = json.load(f)


def post_log(message):
    url = f"{MASTER_CONTROLLER_URL}/log"
    payload = {"message": message}
    response = requests.post(url, json=payload)
    print(response.json())


def add_node(node):
    url = f"{MASTER_CONTROLLER_URL}/add_node"
    payload = {"node": node}
    response = requests.post(url, json=payload)
    print(response.json())


def remove_node(node):
    url = f"{MASTER_CONTROLLER_URL}/remove_node"
    payload = {"node": node}
    response = requests.post(url, json=payload)
    print(response.json())


def set_difficulty(difficulty):
    url = f"{MASTER_CONTROLLER_URL}/set_difficulty"
    payload = {"difficulty": difficulty}
    response = requests.post(url, json=payload)
    print(response.json())


def configure():
    url = f"{MASTER_CONTROLLER_URL}/configure"
    response = requests.post(url)
    print(response.json())

def reset():
    url = f"{MASTER_CONTROLLER_URL}/reset"
    response = requests.post(url)
    print(response.json())


def genesis(nickname):
    url = f"{MASTER_CONTROLLER_URL}/genesis/{nickname}"
    response = requests.post(url)
    print(response.json())


def post_transaction(nickname, sender, recipient, amount):
    # Generate signature using sender's private key
    private_key_pem = HARDCODED_KEYS[sender]['private_key']
    private_key = SigningKey.from_pem(private_key_pem)
    transaction_data = f"{sender}{recipient}{amount}".encode()
    signature = private_key.sign(transaction_data).hex()

    url = f"{MASTER_CONTROLLER_URL}/post_transaction/{nickname}"
    payload = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
        "signature": signature
    }
    response = requests.post(url, json=payload)
    print(response.json())


def get_users(nickname):
    url = f"{MASTER_CONTROLLER_URL}/get_users/{nickname}"
    response = requests.get(url)
    print(json.dumps(response.json(), indent=4))


def get_chain(nickname):
    url = f"{MASTER_CONTROLLER_URL}/get_chain/{nickname}"
    response = requests.get(url)
    print(json.dumps(response.json(), indent=4))


def get_configuration():
    url = f"{MASTER_CONTROLLER_URL}/configuration"
    response = requests.get(url)
    print(response.json())


def main():
    parser = argparse.ArgumentParser(description="CLI for Master Controller")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for adding node (alias: a)
    add_node_parser = subparsers.add_parser("add_node", aliases=["a"])
    add_node_parser.add_argument("node", type=str, help="URL of the node to add")

    # Subparser for removing node (alias: r)
    remove_node_parser = subparsers.add_parser("remove_node", aliases=["r"])
    remove_node_parser.add_argument("node", type=str, help="URL of the node to remove")

    # Subparser for setting difficulty (alias: d)
    set_difficulty_parser = subparsers.add_parser("difficulty", aliases=["d"])
    set_difficulty_parser.add_argument("difficulty", type=int, help="Difficulty level for mining")

    # Subparser for configuring nodes (alias: c)
    config_parser = subparsers.add_parser("configure", aliases=["c"])

    # Subparser for resetting nodes (alias: x)
    reset_parser = subparsers.add_parser("reset", aliases=["x"])

    # Subparser for posting transaction (alias: t)
    trans_parser = subparsers.add_parser("transaction", aliases=["t"])
    trans_parser.add_argument("nickname", type=str, help="Nickname of the node")
    trans_parser.add_argument("sender", type=str, help="Sender of the transaction")
    trans_parser.add_argument("recipient", type=str, help="Recipient of the transaction")
    trans_parser.add_argument("amount", type=int, help="Amount of the transaction")

    # Subparser for create genesis block (alias: g)
    genesis_parser = subparsers.add_parser("genesis", aliases=["g"])
    genesis_parser.add_argument("nickname", type=str, help="Nickname of the node")

    # Subparser for getting users (alias: u)
    users_parser = subparsers.add_parser("users", aliases=["u"])
    users_parser.add_argument("nickname", type=str, help="Nickname of the node")

    # Subparser for getting blockchain (alias: b)
    chain_parser = subparsers.add_parser("chain", aliases=["b"])
    chain_parser.add_argument("nickname", type=str, help="Nickname of the node")

    # Subparser for getting configuration (alias: f)
    config_get_parser = subparsers.add_parser("get_configuration", aliases=["f"])
    args = parser.parse_args()

    if args.command == "add_node":
        add_node(args.node)
    elif args.command == "remove_node":
        remove_node(args.node)
    elif args.command == "difficulty":
        set_difficulty(args.difficulty)
    elif args.command == "configure":
        configure()
    elif args.command == "reset":
        reset()
    elif args.command == "transaction":
        post_transaction(args.nickname, args.sender, args.recipient, args.amount)
    elif args.command == "users":
        get_users(args.nickname)
    elif args.command == "chain":
        get_chain(args.nickname)
    elif args.command == "genesis":
        genesis(args.nickname)
    elif args.command == "get_configuration":
        get_configuration()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
