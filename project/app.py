from flask import Flask, Response, jsonify, request
from flask_restful import Api
from blockchain import Blockchain
from uuid import uuid4
import base64

app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

#instantiate the blockchain
blockchain = Blockchain()

api = Api(app)

@app.route("/")
def index():
    return "/api/"

@app.route("/mine", methods=["GET"])
def mine():
    last_block = blockchain.get_last_block
    last_proof = last_block["proof"]
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200

@app.route("/transaction", methods=["POST"])
def new_transaction():
    data = request.get_json(force=True)

    if not data or not "sender" in data or not "recipient" in data or not "amount" in data:
        return 'Missing values', 400

    index = blockchain.new_transaction(data["sender"], data["recipient"], data["amount"])

    response = {
        "message": f'Transaction will be added to Block {index}'
    }

    return jsonify(response), 200

@app.route("/chain", methods=["GET"])
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
