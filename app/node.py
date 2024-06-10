from flask import Flask, jsonify, request
from uuid import uuid4
from blockchain import Blockchain
from block import Block
import argparse

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = None

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
        signature=b'',
    )

    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block.index,
        'transactions': block.transactions,
        'proof': block.proof,
        'previous_hash': block.previous_hash,
        'merkle_root': block.merkle_root,
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['transaction', 'sender']
    if not all(k in values for k in required):
        return 'Missing values', 400

    transaction = values['transaction']
    index = blockchain.new_transaction(
        sender=transaction['sender'],
        recipient=transaction['recipient'],
        amount=transaction['amount'],
        signature=bytes.fromhex(transaction['signature'])
    )

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': [block.to_dict() for block in blockchain.chain],
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/users', methods=['GET'])
def get_users():
    response = {'users': blockchain.users}
    return jsonify(response), 200

@app.route('/configure', methods=['POST'])
def configure():
    values = request.get_json()

    required = ['nodes', 'master_controller', 'difficulty']
    if not all(k in values for k in required):
        return 'Missing values', 400

    nodes = values['nodes']
    master_controller = values['master_controller']
    difficulty = values['difficulty']

    blockchain.configure(nodes, master_controller, difficulty)

    response = {
        'message': 'Configuration updated',
        'total_nodes': list(blockchain.nodes),
        'master_controller': blockchain.master_controller,
        'difficulty': blockchain.difficulty,
        'nickname': blockchain.nickname
    }
    return jsonify(response), 201



@app.route('/genesis', methods=['POST'])
def genesis_block():
    blockchain.genesis()
    response = {'message': 'Genesis block added to the chain'}
    return jsonify(response), 201

@app.route('/blocks/new', methods=['POST'])
def receive_block():
    values = request.get_json()

    required = ['block', 'sender']
    if not all(k in values for k in required):
        return 'Missing values', 400

    block_data = values['block']
    sender = values['sender']

    block = Block(
        index=block_data['index'],
        timestamp=block_data['timestamp'],
        transactions=block_data['transactions'],
        proof=block_data['proof'],
        previous_hash=block_data['previous_hash'],
        merkle_root=block_data['merkle_root']
    )

    blockchain.add_block(block)

    response = {'message': 'Block added to the chain'}
    return jsonify(response), 201

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blockchain Node')
    parser.add_argument('ip', type=str, help='IP address to bind the node')
    parser.add_argument('port', type=int, help='Port to bind the node')
    parser.add_argument('nickname', type=str, help='Nickname of the node')
    parser.add_argument('--type', type=str, default='full', choices=['full', 'lightweight'], help='Type of the node (full or lightweight)')
    args = parser.parse_args()

    blockchain = Blockchain(args.nickname, f"{args.ip}:{args.port}")

    app.run(host=args.ip, port=args.port)

