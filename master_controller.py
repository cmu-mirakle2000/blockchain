from flask import Flask, request, jsonify
from datetime import datetime
import argparse
import requests

app = Flask(__name__)
master_controller_url = None
nodes = []
difficulty = None
node_nicknames = {}

@app.route('/genesis/<nickname>', methods=['POST'])
def genesis(nickname):
    node_url = node_nicknames.get(nickname)
    if not node_url:
        return 'Invalid node nickname', 400

    try:
        response = requests.post(f'http://{node_url}/genesis', json={})
        if response.status_code == 201:
            return jsonify(response.json()), 201
        else:
            return jsonify({'status': 'Failed to request genesis', 'error': response.status_code}), 400
    except Exception as e:
        return jsonify({'status': 'Failed to request genesis', 'error': str(e)}), 400


@app.route('/log', methods=['POST'])
def receive_log():
    values = request.get_json()

    required = ['message']
    if not all(k in values for k in required):
        return 'Missing values', 400

    message = values['message']
    current_time = datetime.now().strftime('%H:%M:%S')
    print(f"[{current_time}] {message}")

    return jsonify({'status': 'received'}), 201

@app.route('/add_node', methods=['POST'])
def add_node():
    values = request.get_json()

    required = ['node']
    if not all(k in values for k in required):
        return 'Missing values', 400

    node = values['node']
    nodes.append(node)
    return jsonify({'status': 'node added', 'nodes': nodes}), 201

@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    values = request.get_json()

    required = ['difficulty']
    if not all(k in values for k in required):
        return 'Missing values', 400

    global difficulty
    difficulty = values['difficulty']
    return jsonify({'status': 'difficulty set', 'difficulty': difficulty}), 201

@app.route('/configure', methods=['POST'])
def configure():
    if not nodes or difficulty is None:
        return 'Configuration incomplete', 400

    global node_nicknames

    configuration = {
        'nodes': nodes,
        'master_controller': master_controller_url,
        'difficulty': difficulty
    }

    for node in nodes:
        try:
            response = requests.post(f'http://{node}/configure', json=configuration)
            if response.status_code == 201:
                response_data = response.json()
                node_nickname = response_data.get('nickname')
                node_nicknames[node_nickname] = node
                print(f"Configuration sent to node {node}, nickname: {node_nickname}")
            else:
                print(f"Failed to configure node {node}: {response.status_code}")
        except Exception as e:
            print(f"Error configuring node {node}: {e}")

    return jsonify({'status': 'configuration sent to nodes', 'nodes': node_nicknames}), 201

@app.route('/post_transaction/<nickname>', methods=['POST'])
def post_transaction(nickname):
    values = request.get_json()

    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(k in values for k in required):
        return 'Missing values', 400

    node_url = node_nicknames.get(nickname)
    if not node_url:
        return 'Invalid node nickname', 400

    transaction = {
        'sender': values['sender'],
        'recipient': values['recipient'],
        'amount': values['amount'],
        'signature': values['signature']
    }

    try:
        response = requests.post(f'http://{node_url}/transactions/new', json={'transaction': transaction, 'sender': 'MasterController'})
        if response.status_code == 201:
            return jsonify({'status': 'Transaction posted'}), 201
        else:
            return jsonify({'status': 'Failed to post transaction', 'error': response.status_code}), 400
    except Exception as e:
        return jsonify({'status': 'Failed to post transaction', 'error': str(e)}), 400

@app.route('/get_users/<nickname>', methods=['GET'])
def get_users(nickname):
    node_url = node_nicknames.get(nickname)
    if not node_url:
        return 'Invalid node nickname', 400

    try:
        response = requests.get(f'http://{node_url}/users')
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'status': 'Failed to get users', 'error': response.status_code}), 400
    except Exception as e:
        return jsonify({'status': 'Failed to get users', 'error': str(e)}), 400

@app.route('/get_chain/<nickname>', methods=['GET'])
def get_chain(nickname):
    node_url = node_nicknames.get(nickname)
    if not node_url:
        return 'Invalid node nickname', 400

    try:
        response = requests.get(f'http://{node_url}/chain')
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'status': 'Failed to get chain', 'error': response.status_code}), 400
    except Exception as e:
        return jsonify({'status': 'Failed to get chain', 'error': str(e)}), 400

@app.route('/configuration', methods=['GET'])
def get_configuration():
    global nodes, difficulty, node_nicknames
    return jsonify({
        'master_controller_url': master_controller_url,
        'nodes': nodes,
        'difficulty': difficulty,
        'node_nicknames': node_nicknames
    }), 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Master Controller for Blockchain Nodes')
    parser.add_argument('ip', type=str, help='IP address to bind the master controller')
    parser.add_argument('port', type=int, help='Port to bind the master controller')
    args = parser.parse_args()

    master_controller_url = f"http://{args.ip}:{args.port}"

    app.run(host=args.ip, port=args.port)
