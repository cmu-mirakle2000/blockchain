from flask import Flask, jsonify, request
from uuid import uuid4
from blockchain import Blockchain
from block import Block
import argparse

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = None
node_type = "single"


@app.route('/configure', methods=['POST'])
def configure():
    values = request.get_json()

    required = ['nodes', 'master_controller', 'difficulty', 'reset']
    if not all(k in values for k in required):
        return 'Missing values', 400

    nodes = values['nodes']
    master_controller = values['master_controller']
    difficulty = values['difficulty']
    reset = values['reset']

    blockchain.configure(nodes, master_controller, difficulty, reset)

    response = {
        'message': 'Configuration updated',
        'total_nodes': list(blockchain.nodes),
        'master_controller': blockchain.master_controller,
        'difficulty': blockchain.difficulty,
        'nickname': blockchain.nickname
    }
    return jsonify(response), 201



@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block.nonce
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
        signature=b'',
        broadcast=True
    )

    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block.index,
        'transactions': block.transactions,
        'proof': block.nonce,
        'previous_hash': block.previous_hash,
        'merkle_root': block.merkle_root,
    }
    return jsonify(response), 200

@app.route('/transactions', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['transaction', 'sender']
    if not all(k in values for k in required):
        return 'Missing values', 400

    sender = values['sender']
    transaction = values['transaction']
    valid_transaction, validation_message = blockchain.new_transaction(
        sender=transaction['sender'],
        recipient=transaction['recipient'],
        amount=transaction['amount'],
        signature=bytes.fromhex(transaction['signature']),
        # broadcast=True if sender == 'MasterController' else False
        broadcast=True if network_node and sender=="" else False
    )

    if not valid_transaction:
        return jsonify(f'Invalid transaction: {validation_message}'), 400

    response = {'message': f'Transaction will be added to next Block'}
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


@app.route('/genesis', methods=['POST'])
def genesis_block():
    if not network_node:
        response = {'message': 'Not a network node'}
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
        index=block_data['header']['index'],
        timestamp=block_data['header']['timestamp'],
        nonce=block_data['header']['nonce'],
        previous_hash=block_data['header']['previous_hash'],
        merkle_root=block_data['header']['merkle_root'],
        transactions=block_data['transactions']
    )

    # TODO
    # Confirm the Merkle Root is valid for the transactions
    # Match the previous_hash with the actual block in YOUR blockchain
    # Confirm that proof of work hash is valid for new block header with the given nonce

    blockchain.add_block(block)

    response = {'message': 'Block added to the chain'}
    return jsonify(response), 201

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blockchain Node')
    parser.add_argument('type', type=str, help='single or network')
    parser.add_argument('nickname', type=str, help='Nickname of the node')

    parser.add_argument('-i', '--ip', type=str, help='IP address to bind the node', default="127.0.0.1")
    parser.add_argument('-p', '--port', type=int, help='Port to bind the node', default=8000)
    args = parser.parse_args()

    network_node = True if args.type == 'network' else False if args.type == 'single' else None
    if network_node is None:
        raise ValueError('Node must be single or network')
    node_ip = args.ip
    bind_ip = args.ip if args.type == 'single' else "0.0.0.0"
    node_port = args.port

    blockchain = Blockchain(args.nickname, f"{node_ip}:{node_port}", network_node)
    if not network_node:
        blockchain.reset()
    app.run(host=bind_ip, port=node_port)

