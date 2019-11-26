import os
from blockchain import Blockchain, Block
import discord
import asyncio
import ast


NEW_DATA = 'new_data.txt'
NOTE_CONVERT = 'CONVERT'
NOTE_LOAD = 'LOAD'
NOTE_TRANSFER = 'TRANSFER'


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
            self.server_id, receiver_id, amount, server_bal, amount, NOTE_LOAD))
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


class IssueManager(object):

    def __init__(self, bm, commands_channel_id):
        self.bm = bm
        self.client = bm.client
        self.server_id = bm.server_id
        self.blockchain_channel_id = bm.blockchain_channel_id
        self.commands_channel_id = commands_channel_id
        self.issue_in_session = False

    async def get_issue(self, issue_id):
        issue_data = issue_id.split('-')
        server = self.client.get_guild(id=int(issue_data[0]))
        channel = self.client.get_channel(int(issue_data[1]))
        message = await channel.fetch_message(int(issue_data[2]))
        return(message.content.replace('!IBDD ', '').replace('"', ''))

    async def non_voters_transver(self):
        await self.client.wait_until_ready()
        server = self.client.get_guild(id=self.server_id)
        channel = self.client.get_channel(self.blockchain_channel_id)
        counter = 0
        current_bal = None
        print(self.issue_in_session)
        for member in server.members:
            print(member.id)
            voted = False
            async for message in channel.history(limit=None, oldest_first=False):
                data = message.content.split('\n')[2].replace('Block Data: ', '')[:-1]
                data = '[' + data + ']'
                data = ast.literal_eval(data)
                for t in data:
                    if t[0] == str(member.id) and t[1] == self.issue_in_session:
                        voted = True
            if voted:
                print(member.id, 'voted')
            else:
                await self.bm.update_block(member.id, self.issue_in_session, 0, NOTE_CONVERT)

    async def get_converts(self):
        server = self.client.get_guild(id=self.server_id)
        channel = self.client.get_channel(self.blockchain_channel_id)
        converts = 0
        convert_ids = []
        async for message in channel.history(limit=None, oldest_first=False):
            data = message.content.split('\n')[2].replace('Block Data: ', '')[:-1]
            data = '[' + data + ']'
            data = ast.literal_eval(data)
            for t in data:
                if t[1] == self.issue_in_session and t[5] == NOTE_CONVERT:
                    converts += 1
                    convert_ids.append(t[0])
        return(converts, convert_ids)

    async def count_votes(self):
        await self.non_voters_transver()
        await asyncio.sleep(10)  # change this for end vote check on BC
        sum_traded_votes, convert_ids = await self.get_converts()
        server_bal = await self.bm.get_balance(self.server_id)
        vote_price = round(float(server_bal)/float(sum_traded_votes), 2)
        for id in convert_ids:
            await self.bm.update_block(self.server_id, id, vote_price, NOTE_TRANSFER)
        print(sum_traded_votes, vote_price)

    async def issue_timer(self):
        server = self.client.get_guild(id=self.server_id)
        channel = self.client.get_channel(self.commands_channel_id)
        await asyncio.sleep(60*1)
        await channel.send("**1 min** remaining...")
        await asyncio.sleep(60*1)
        await channel.send("*Vote finished*")
        await self.count_votes()
        self.issue_in_session = False
