from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import Blockchain


app = Flask(__name__)  # Instantiate the node
node_identifier = str(uuid4()).replace('-', '')  # We need a unique address (identifier) for each node
blockchain = Blockchain()  # Create a blockchain


@app.route('/mine', methods=['GET'])
def mine():
    # First we try to find the next proof
    last_block = blockchain.last_block
    last_proof = last_block["proof"]
    proof = blockchain.proof_of_work(last_proof)

    # Then we collects our reward
    blockchain.new_transaction(
        sender="0",  # 0 points to the node
        recipient=node_identifier,
        amount=1
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        "message": "New block forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"]
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    data = request.get_json()

    required = ["sender", "recipient", "amount"]
    if not all(k in data for k in required):
        return 'Missing properties', 400

    index = blockchain.new_transaction(data["sender"], data["recipient"], data["amount"])
    response = {"message": f"Transaction will be added to block {index}"}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    nodes = request.get_json().get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
