import argparse
import requests
import json
from ecdsa import SigningKey
import shlex
import sys

# Enable command history on Mac/Linux
try:
    import readline
except ImportError:
    pass  # Skip on Windows

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


def create_parser():
    """Create and return the argparse parser"""
    parser = argparse.ArgumentParser(description="CLI for Master Controller", add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    # Help command
    help_parser = subparsers.add_parser("help", aliases=["h"], help="Show available commands")

    # Add node
    add_parser = subparsers.add_parser("add_node", aliases=["a"])
    add_parser.add_argument("node", help="Node URL to add")

    # Remove node
    remove_parser = subparsers.add_parser("remove_node", aliases=["r"])
    remove_parser.add_argument("node", help="Node URL to remove")

    # Difficulty
    diff_parser = subparsers.add_parser("difficulty", aliases=["d"])
    diff_parser.add_argument("difficulty", type=int, help="Mining difficulty level")

    # Configure
    subparsers.add_parser("configure", aliases=["c"])

    # Reset
    subparsers.add_parser("reset", aliases=["x"])

    # Transaction
    trans_parser = subparsers.add_parser("transaction", aliases=["t"])
    trans_parser.add_argument("nickname", help="Node nickname")
    trans_parser.add_argument("sender", help="Transaction sender")
    trans_parser.add_argument("recipient", type=str, help="Recipient of the transaction")
    trans_parser.add_argument("amount", type=int, help="Transaction amount")

    # Genesis
    genesis_parser = subparsers.add_parser("genesis", aliases=["g"])
    genesis_parser.add_argument("nickname", help="Node nickname")

    # Users
    users_parser = subparsers.add_parser("users", aliases=["u"])
    users_parser.add_argument("nickname", help="Node nickname")

    # Chain
    chain_parser = subparsers.add_parser("chain", aliases=["b"])
    chain_parser.add_argument("nickname", help="Node nickname")

    # Configuration
    subparsers.add_parser("get_configuration", aliases=["f"])

    return parser


def run_command(args):
    """Execute commands based on parsed arguments"""
    if args.command in ("help", "h"):
        create_parser().print_help()
        return

    if args.command in ("add_node", "a"):
        add_node(args.node)
    elif args.command in ("remove_node", "r"):
        remove_node(args.node)
    elif args.command in ("difficulty", "d"):
        set_difficulty(args.difficulty)
    elif args.command in ("configure", "c"):
        configure()
    elif args.command in ("reset", "x"):
        reset()
    elif args.command in ("transaction", "t"):
        post_transaction(args.nickname, args.sender, args.recipient, args.amount)
    elif args.command in ("users", "u"):
        get_users(args.nickname)
    elif args.command in ("chain", "b"):
        get_chain(args.nickname)
    elif args.command in ("genesis", "g"):
        genesis(args.nickname)
    elif args.command in ("get_configuration", "f"):
        get_configuration()


def interactive_prompt():
    """Start interactive command prompt with history"""
    parser = create_parser()
    print("Blockchain Controller CLI - Type 'help' for commands, 'exit' to quit")

    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() in ("exit", "quit"):
                break
            if not user_input:
                continue

            # Parse input
            parsed_args = parser.parse_args(shlex.split(user_input))
            run_command(parsed_args)

        except SystemExit:
            # Handle argparse errors gracefully
            continue
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        args = create_parser().parse_args()
        run_command(args)
    else:
        # Interactive mode
        interactive_prompt()
