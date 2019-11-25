import os
from blockchain import Blockchain, Block
import discord
import asyncio
import ast

NEW_DATA = 'new_data.txt'


class BlockchainManager(object):
    NOTE_LOAD = 'LOAD'
    NEW_DATA = 'new_data.txt'

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

    async def update_block(self, sender, receiver, amount, note):
        s_bal = await self.get_balance(sender)
        r_bal = await self.get_balance(receiver)
        print(s_bal, r_bal, amount)
        try:
            sender_bal = s_bal - amount
            receiver_bal = r_bal + amount
            if sender_bal >= 0:
                f = open(NEW_DATA, 'a+')
                # [sender_user_id, receiver_id, transver_amount, sender_new_bal]
                f.write('["{}","{}","{}","{}","{}","{}"],'.format(
                    sender, receiver, amount, sender_bal, receiver_bal, note))
                f.close()
                return(True)
            else:
                return(False)
        except Exception as e:
            return(False)

    async def load_balance(self, receiver_id, amount):
        server_bal = await self.get_balance(self.server_id)
        f = open(NEW_DATA, 'a+')
        # [sender_user_id, receiver_id, transver_amount, sender_new_bal]
        f.write('["{}","{}","{}","{}","{}","{}"],'.format(
            self.server_id, receiver_id, amount, server_bal, amount, self.NOTE_LOAD))
        f.close()

    async def get_balance(self, blockchain_id):
        await self.client.wait_until_ready()
        server = self.client.get_guild(self.server_id)
        blockchain_channel = self.client.get_channel(self.blockchain_channel_id)
        messages = []
        counter = 0
        current_bal = None
        async for message in blockchain_channel.history(limit=None, oldest_first=False):
            try:
                data = message.content.split('\n')[2].replace('Block Data: ', '')[:-1]
                data = '[' + data + ']'
                data = ast.literal_eval(data)
                should_break = False
                for t in data:
                    if t[0] == str(blockchain_id):
                        # print(t)
                        # print('Current bal: {}'.format(t[3]))
                        current_bal = float(t[3])
                        should_break = True
                    elif t[1] == str(blockchain_id):
                        # print('id here')
                        current_bal = float(t[4])
                        should_break = True
                if should_break:
                    break
            except Exception as e:
                print('Bad data: ', e)
                current_bal = None
        return(current_bal)


class GeneralDemocracy(object):

    def __init__(self, client, server_id, blockchain_channel_id):
        print("Under construction...")
