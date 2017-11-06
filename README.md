# Blockchain implemented with Python
A proof-of-concept blockchain which is accessible over http implemented with Python

## Getting Started
Implemented this to understand blockchain and proof of work better.

To use the blockchain you have these http access points:
/chain - returns the complete blockchain
/transaction - only POST Request is allowed - adds a new transaction
/mine - starts with proof of work

### Installing
You need a running python environment with Flask and flask_restful, then just run app.py.

### Example

#### New transaction
Add a new transaction with any http client (e.g. postman) posting to the URI /transaction:

POST request data (in json):

{
	"sender": "any address",
	"recipient": "any address",
	"amount": 5
}

Of course you can add any informtion you want to the transaction.
