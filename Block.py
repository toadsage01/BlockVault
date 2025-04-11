from hashlib import sha256
# Importing sha256 module for using hashing function
# sha256 module generates a secure, fixed-length for block data
class Block:
    def __init__(self, index, transactions, prev_hash):
        self.index = index
        # index must refer to position in the chain  

        self.transactions = transactions 
        # list of data that are being recorded (or in use)

        self.prev_hash = prev_hash 
        # of previous block

        self.nonce = 0 
        # with this, we will mine


   
   # For verification and linking blocks securely
    def generate_hash(self):
        all_data_combined = str(self.index) + str(self.nonce) + self.prev_hash + str(self.transactions)
        # combines block data into a string

        return sha256(all_data_combined.encode()).hexdigest()
    
    # For adding new transaction to block's transaction record list
    def add_t(self, t):
        self.transactions.append(t)