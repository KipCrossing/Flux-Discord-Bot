import datetime
import hashlib
import os

print(os.listdir())


class Block:
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data

    def hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.blockNo).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\n--------------\n"


class Blockchain:

    diff = 24
    maxNonce = 2**32
    target = 2 ** (256-diff)

    lbf = 'lastblock.txt'

    if lbf in os.listdir():
        f = open('lastblock.txt', 'r')
        lastblock_info = []
        for line in f:
            lastblock_info.append(line)

        block = Block(lastblock_info[2].replace('Block Data: ', '').replace('\n', ''))
        block.hash = lastblock_info[0].replace('Block Hash: ', '').replace('\n', '')
        block.blockNo = int(lastblock_info[1].replace('BlockNo: ', ''))
        f.close()
    else:
        block = Block("Genesis")
        f = open('blockchain.txt', 'a+')
        f.write(str(block))
        f.close()
    dummy = head = block

    def add(self, block):
        try:
            block.previous_hash = self.block.hash()
        except:
            block.previous_hash = self.block.hash
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next
        f = open('blockchain.txt', 'a')
        f.write(str(self.block))
        f.close()
        f = open('lastblock.txt', 'w')
        f.write(str(self.block))
        f.close()

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print(block)
                break
            else:
                block.nonce += 1


blockchain = Blockchain()

# while True:
#     new_data = 'new_data.txt'
#     if new_data in os.listdir():
#         f = open(new_data, 'r')
#         data = ''
#         for line in f:
#             data = line
#         f.close()
#         # os.remove(new_data)
#         print(datetime.datetime.now())
#         blockchain.mine(Block(data))


# while blockchain.head != None:
#     print(blockchain.head)
#     blockchain.head = blockchain.head.next
