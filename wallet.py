import argparse
import requests
import json
from ecdsa import SigningKey
import shlex
import sys

# Enable up-arrow history on Mac/Linux, do nothing on Windows
try:
    import readline
except ImportError:
    pass

# Defaults
DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 8004

node_ip = DEFAULT_IP
node_port = DEFAULT_PORT
node_url = None
local_controller_url = None
nodes = []
difficulty = 2
node_nickname = ""
network_node = True

# Load keys from JSON file
with open('keys.json', 'r') as f:
    HARDCODED_KEYS = json.load(f)

def set_node_url(ip, port):
    global node_url, nodes
    node_url = f"http://{ip}:{port}"
    nodes = [node_url]

def set_difficulty(new_difficulty):
    global difficulty
    if network_node:
        print("Network node")
        return

    difficulty = int(new_difficulty)
    configuration = {
        'nodes': nodes,
        'master_controller': local_controller_url,
        'difficulty': difficulty,
        'reset': 0
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
    if network_node:
        print("Network node")
        return

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
        "source": ""
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

def get_configuration(show=True):
    global node_nickname, network_node
    url = f"{node_url}/configuration"
    response = requests.get(url)
    if response.status_code == 201:
        response_data = response.json()
        node_nickname = response_data.get('nickname')
        network_node = response_data.get('network_node')

    if show:
        print(response.json())

def show_info():
    print(f"Node IP: {node_ip}")
    print(f"Node Port: {node_port}")
    print(f"Node URL: {node_url}")
    print(f"Nickname: {node_nickname}")
    print(f"Network node: {network_node}")

def create_parser():
    parser = argparse.ArgumentParser(description="CLI for Master Controller")
    parser.add_argument("-i", "--ip", type=str, required=True, help="Node IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Node port")
    subparsers = parser.add_subparsers(dest="command")

    set_difficulty_parser = subparsers.add_parser("difficulty", aliases=["d"])
    set_difficulty_parser.add_argument("difficulty", type=int, help="Difficulty level for mining")

    reset_parser = subparsers.add_parser("reset", aliases=["r"])

    trans_parser = subparsers.add_parser("transaction", aliases=["t"])
    trans_parser.add_argument("sender", type=str)
    trans_parser.add_argument("recipient", type=str)
    trans_parser.add_argument("amount", type=int)

    send_parser = subparsers.add_parser("send", aliases=["s"])
    send_parser.add_argument("recipient", type=str)
    send_parser.add_argument("amount", type=int)

    subparsers.add_parser("users", aliases=["u"])
    subparsers.add_parser("get_configuration", aliases=["g"])
    subparsers.add_parser("chain", aliases=["c"])
    subparsers.add_parser("info", help="Show node info")
    subparsers.add_parser("help", aliases=["h"], help="Show this help message and list commands")

    return parser

def run_cli(args=None):
    parser = create_parser()
    args = parser.parse_args(args) if args else parser.parse_args()

    # Set IP and port globally
    global node_ip, node_port
    node_ip = args.ip
    node_port = args.port
    set_node_url(node_ip, node_port)

    if not args.command:
        parser.print_help()
        return
    if args.command in ("help", "h"):
        parser.print_help()
    elif args.command == "info":
        show_info()
    elif args.command in ("difficulty", "d"):
        set_difficulty(args.difficulty)
    elif args.command in ("reset", "r"):
        reset()
    elif args.command in ("transaction", "t"):
        if network_node:
            print("Network node")
        else:
            post_transaction(args.sender, args.recipient, args.amount)
    elif args.command in ("send", "s"):
        post_transaction(node_nickname, args.recipient, args.amount)
    elif args.command in ("get_configuration", "g"):
        get_configuration()
    elif args.command in ("users", "u"):
        get_users()
    elif args.command in ("chain", "c"):
        get_chain()

def interactive_prompt():
    parser = create_parser()
    prompt_base = lambda: f"{node_nickname}@{node_ip}:{node_port}:{'network' if network_node else 'single'}> "
    print("Blockchain CLI (type 'exit' to quit)")
    while True:
        try:
            user_input = input(prompt_base()).strip()
            if user_input.lower() in ("exit", "quit"):
                break
            if not user_input:
                get_configuration(False)
                continue

            get_configuration(False)
            # Add IP and port to args for each command
            run_cli(shlex.split(f"--ip {node_ip} --port {node_port} " + user_input))
        except SystemExit:
            continue
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Parse IP and port at startup
    parser = create_parser()
    startup_args, _ = parser.parse_known_args()
    node_ip = startup_args.ip
    node_port = startup_args.port
    set_node_url(node_ip, node_port)
    run_cli(shlex.split(f"--ip {node_ip} --port {node_port} g"))
    interactive_prompt()
