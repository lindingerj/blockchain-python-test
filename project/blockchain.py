import hashlib
import json
from time import time
from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #create the genesis block
        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.get_last_block)
        }

        self.current_transactions = []

        self.chain.append(block)

        return block

    #creates a new transaction for the new block
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

        last_block = self.get_last_block

        return last_block["index"] + 1     #returns index for new block

    #find a number 'p' such that hash ('old_p' , 'p') containts 4 leading zeroes
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    #validates the proof (four leading zeros)
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    #returns the last block of the chain
    @property
    def get_last_block(self):
        return self.chain[-1]
