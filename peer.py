# import libraries
import json # to handle JSON I/O
from Blockchain import Blockchain
from Block import Block # to create custom 
from flask import Flask, request # to create web server & accept inputs


""" This will intialize 
- flask app,
- the blockchain instance,
- an empty list for connection of peers
"""
# app object
app = Flask(__name__)
# blockchain object
blockchain = Blockchain()
# peers list
peers = []


""" This function will
- accept new document/data transaction
- will validate required features
- will also add it to 'pending transaction pool' post validation
"""
@app.route("/new_transaction", methods=["POST"])
def new_transaction():
    file_data = request.get_json()  # get json response
    required_fields = ["user", "v_file", "file_data", "file_size"]
    for field in required_fields:
        if not file_data.get(field):
            return "Transaction does not have valid fields!", 404
    blockchain.add_pending(file_data)
    return "Success", 201



""" THis will
- return the full blockchain as JSON
- for debugging purpose
"""
@app.route("/chain", methods=["GET"])
def get_chain():
    # consensus()
    chain = []

    for block in blockchain.chain:
        chain.append(block.__dict__)
    # print chain len
    print("Chain Len: {0}".format(len(chain)))
    return json.dumps({"length": len(chain), "chain": chain})



"""
- mine all unconfirmed transaction
- add those into a new block and append to the chain
"""
@app.route("/mine", methods=["GET"])
def mine_uncofirmed_transactions():
    result = blockchain.mine()
    if result:
        return "Block #{0} mined successfully.".format(result)
    else:
        return "No pending transactions to mine."



"""
- displaying list of current pending transaction
"""
@app.route("/pending_tx")
def get_pending_tx():
    return json.dumps(blockchain.pending)


"""
- will accept a block from another peer
- verify using hash and append to chain if it is valid
"""
@app.route("/add_block", methods=["POST"])
def validate_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["transactions"], block_data["prev_hash"])
    hashl = block_data["hash"]
    added = blockchain.add_block(block, hashl)
    if not added:
        return "The Block was thrown away by the node.", 400
    return "The block was added to the blockchain.", 201


# run the app
app.run(port=8800, debug=True)
