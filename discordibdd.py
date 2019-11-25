import os
from blockchain import Blockchain, Block
import discord
import asyncio


NEW_DATA = 'new_data.txt'


class BlockchainManager(object):

    def __init__(self, client, server_id, blockchain_channel_id):
        self.client = client
        self.server_id = server_id
        self.blockchain_channel_id = blockchain_channel_id
        self.blockchain = Blockchain()

    async def update_blockchain(self):
        print('Update blockchain')
        await self.client.wait_until_ready()
        server = self.client.get_guild(self.server_id)
        blockchain_channel = self.client.get_channel(self.blockchain_channel_id)
        print(self.client.is_closed())
        while not self.client.is_closed():
            print('open')
            if NEW_DATA in os.listdir():
                f = open(NEW_DATA, 'r')
                data = ''
                for line in f:
                    data = line
                f.close()
                self.blockchain.mine(Block(data))
                os.remove(NEW_DATA)
                await blockchain_channel.send(self.blockchain.block)
            await asyncio.sleep(5)
