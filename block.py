import hashlib
import json


class Block:
    def __init__(self, index, timestamp, transactions, nonce, previous_hash, merkle_root, header=None):
        if header:
            self.header = {
                'index': header.get('index'),
                'timestamp': header.get('timestamp'),
                'nonce': header.get('nonce'),
                'previous_hash': header.get('previous_hash'),
                'merkle_root': header.get('merkle_root')
            }
        else:
            self.header = {
                'index': index,
                'timestamp': timestamp,
                'nonce': nonce,
                'previous_hash': previous_hash,
                'merkle_root': merkle_root
            }
        self.transactions = transactions

    def to_dict(self):
        return {
            'header': {
                'index': self.header['index'],
                'timestamp': self.header['timestamp'],
                'nonce': self.header['nonce'],
                'previous_hash': self.header['previous_hash'],
                'merkle_root': self.header['merkle_root']
            },
            'transactions': self.transactions,
        }

    def header_to_dict(self):
        return {
            'header': {
                'index': self.header['index'],
                'timestamp': self.header['timestamp'],
                'nonce': self.header['nonce'],
                'previous_hash': self.header['previous_hash'],
                'merkle_root': self.header['merkle_root']
            },
            'transactions': self.transactions,
        }

    @staticmethod
    def hash(block):
        """Serialize block header for hashing, handling both Block objects and dicts"""
        if isinstance(block, dict):
            # Extract header from dictionary format
            header = block.get('header', {})
        elif isinstance(block, Block):
            # Get header from Block object
            header = block.header_to_dict()
        else:
            raise ValueError("Unsupported block type")

        # Serialize header for hashing
        return json.dumps(header, sort_keys=True).encode()

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
