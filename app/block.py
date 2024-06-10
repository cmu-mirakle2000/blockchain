import hashlib
import json

class Block:
    def __init__(self, index, timestamp, transactions, proof, previous_hash, merkle_root):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'proof': self.proof,
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root
        }

    @staticmethod
    def hash(block):
        block_string = json.dumps(block.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def merkle_root(transactions):
        if not transactions:
            return None

        def hash_pair(a, b):
            return hashlib.sha256(f'{a}{b}'.encode()).hexdigest()

        tx_hashes = [hashlib.sha256(json.dumps(tx, sort_keys=True).encode()).hexdigest() for tx in transactions]

        while len(tx_hashes) > 1:
            if len(tx_hashes) % 2 != 0:
                tx_hashes.append(tx_hashes[-1])

            tx_hashes = [hash_pair(tx_hashes[i], tx_hashes[i + 1]) for i in range(0, len(tx_hashes), 2)]

        return tx_hashes[0]
