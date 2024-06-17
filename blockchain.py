import requests
from time import time
from ecdsa import VerifyingKey
from urllib.parse import urlparse
from block import Block
import json
import threading
import hashlib

# Load keys from JSON file
with open('keys.json', 'r') as f:
    HARDCODED_KEYS = json.load(f)


class Blockchain:
    def __init__(self, nickname, node_address):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.users = self.create_users()
        self.mining_event = threading.Event()
        self.nickname = nickname
        self.node_address = node_address
        self.master_controller = None
        self.difficulty = 2

        # Comment out genesis block creation, will be handled manually
        # self.new_block(previous_hash='1', proof=100)

    def create_users(self):
        users = {user: {'balance': 1000} for user in HARDCODED_KEYS.keys()}
        users["Bank"] = {'balance': 2000000}  # Bank user with maximum currency

        for user, keys in HARDCODED_KEYS.items():
            if user in users:
                users[user]['private_key'] = keys['private_key']
                users[user]['public_key'] = keys['public_key']

        return users

    def new_block(self, nonce, previous_hash=None):
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            nonce=nonce,
            previous_hash=previous_hash or Block.hash(self.chain[-1]),
            merkle_root=Block.merkle_root(self.current_transactions)
        )

        self.current_transactions = []

        self.chain.append(block)

        self.log(f"New Block Forged: {block.to_dict()}")

        # FIXME Remove this later
        # self.broadcast_new_block(block)

        return block

    def new_transaction(self, sender, recipient, amount, signature):
        # Skip verification if it is a reward transaction
        if sender != "Bank":
            if not self.verify_transaction(sender, recipient, amount, signature):
                self.log(f"Transaction from {sender} to {recipient} for {amount} failed: Invalid signature")
                return "Invalid signature"

            if self.users[sender]['balance'] < amount:
                self.log(f"Transaction from {sender} to {recipient} for {amount} failed: Insufficient funds")
                return "Insufficient funds"

        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        }

        self.current_transactions.append(transaction)
        if sender != "Bank":
            self.users[sender]['balance'] -= amount
        self.users[recipient]['balance'] += amount

        self.log(f"Transaction: {sender} sent {amount} to {recipient}")

        # FIXME Remove this later
        # self.broadcast_new_transaction(transaction, signature)

        if len(self.current_transactions) >= 5:
            self.mine()

        return self.last_block.header['index'] + 1

    def mine(self):
        new_header = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'previous_hash': Block.hash(self.chain[-1]),
            'nonce' : 0,
            'merkle_root': Block.merkle_root(self.current_transactions),
        }

        last_block = self.last_block
        last_proof = last_block.header['nonce']
        proof = self.proof_of_work(new_header)
        if proof is None:
            return

        new_block = self.new_block(proof)
        # FIXME Remove this later
        # self.broadcast_new_block(new_block)

        self.new_transaction(
            sender="Bank",
            recipient=self.nickname,
            amount=1,
            signature=b'',
        )

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, header):
        nonce = 0
        self.log("Starting proof of work...")
        while self.valid_proof(header, nonce) is False:
            if self.mining_event.is_set():
                self.log("Mining stopped due to new block received.")
                return None
            nonce += 1

        self.log(f"Proof of work found: {nonce}")
        return nonce

    def valid_proof(self, header, nonce):
        header['nonce'] = nonce
        guess = f'{json.dumps(header)}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        print(guess_hash, self.difficulty)
        return guess_hash[:self.difficulty] == "0" * self.difficulty

    def register_node(self, address):
        parsed_url = urlparse(address)
        if parsed_url.netloc == self.node_address:
            self.log(f"Skipping self registration for {self.node_address}")
            return
        self.nodes.add(parsed_url.netloc)
        self.log(f"Node registered: {parsed_url.netloc}")

    def broadcast_new_block(self, block):
        for node in self.nodes:
            url = f'{node}/blocks/new'
            try:
                response = requests.post(url, json={'block': block.to_dict(), 'sender': self.nickname})
                if response.status_code == 201:
                    self.log(f"Block posted to node {node}")
                else:
                    self.log(f"Failed to post block to node {node}: {response.status_code}")
            except Exception as e:
                self.log(f"Error posting block to node {node}: {e}")

    def broadcast_new_transaction(self, transaction, signature):
        for node in self.nodes:
            url = f'{node}/transactions/new'
            try:
                response = requests.post(url, json={
                    'transaction': {
                        'sender': transaction['sender'],
                        'recipient': transaction['recipient'],
                        'amount': transaction['amount'],
                        'signature': signature.hex()
                    },
                    'sender': self.nickname
                })
                if response.status_code == 201:
                    self.log(f"Transaction posted to node {node}")
                else:
                    self.log(f"Failed to post transaction to node {node}: {response.status_code}")
            except Exception as e:
                self.log(f"Error posting transaction to node {node}: {e}")

    def verify_transaction(self, sender, recipient, amount, signature):
        transaction_data = f"{sender}{recipient}{amount}".encode()
        public_key_pem = self.users[sender]['public_key']
        public_key = VerifyingKey.from_pem(public_key_pem)

        try:
            return public_key.verify(signature, transaction_data)
        except:
            return False

    def add_block(self, block):
        self.mining_event.set()
        self.current_transactions = []
        self.chain.append(block)
        self.log(f"Block added to chain: {block.to_dict()}")
        self.mining_event.clear()

    def configure(self, nodes, master_controller, difficulty, reset=0):
        self.master_controller = master_controller
        self.difficulty = difficulty

        if reset == 1:
            # Reset blockchain
            self.chain = []
            self.current_transactions = []
            self.new_block(previous_hash='1', nonce=100)

        # Register nodes
        self.nodes = set()
        for node in nodes:
            self.register_node(node)

        self.log(f"Blockchain {'reset and ' if reset == 1 else ''}reconfigured with difficulty {difficulty}")
    def reset(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', nonce=100)

    def log(self, message):
        log_message = f"[{self.nickname}] {message}"
        print(log_message)
        if self.master_controller:
            try:
                requests.post(f'{self.master_controller}/log', json={'message': log_message})
            except Exception as e:
                print(f"Failed to send log to master controller: {e}")
