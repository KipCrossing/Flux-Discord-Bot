import os
from blockchain import Blockchain, Block
import discord
import asyncio
import ast
import pandas as pd

DATA_DIR = 'data'
NEW_DATA = 'new_data.txt'
ACCOUNT_BALANCES = 'account_balances.csv'


NOTE_CONVERT = 'CONVERT'
NOTE_LOAD = 'LOAD'
NOTE_TRANSFER = 'TRANSFER'
NOTE_END = 'END'
NOTE_START = 'START'
NOTE_NO = 'NO'
NOTE_YES = 'YES'

votes_per_capiter = 100


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
            if NEW_DATA in os.listdir(DATA_DIR):
                f = open(DATA_DIR + '/' + NEW_DATA, 'r')
                data = ''
                for line in f:
                    data = line
                f.close()
                self.blockchain.mine(Block(data))
                os.remove(DATA_DIR + '/' + NEW_DATA)
                await blockchain_channel.send(self.blockchain.block)
            await asyncio.sleep(5)

    async def update_block(self, sender, receiver, amount, note):
        try:
            f = open(DATA_DIR + '/' + NEW_DATA, 'a+')
            f.write('["{}","{}","{}","{}"],'.format(
                sender, receiver, amount, note))
            f.close()
            if note == NOTE_TRANSFER or note[:2] == 'Y-' or note[:2] == 'N-':
                await self.update_balance(sender, -float(amount))
                await self.update_balance(receiver, float(amount))
            elif note == NOTE_TRANSFER:
                await self.update_balance(receiver, votes_per_capiter)
            return(True)
        except Exception as e:
            print("Fail to write to blockchain: \n", e)
            return(False)

    async def update_balance(self, blockchain_id, amount):
        # This is gross but whatever...
        try:
            ab_df = pd.read_csv(DATA_DIR + '/' + ACCOUNT_BALANCES)
            if int(blockchain_id) in list(ab_df['blockchain_id']):
                inx = ab_df.loc[ab_df['blockchain_id'] == int(blockchain_id)].index[0]
                new_bal = float(ab_df['balance'][inx]) + amount
                ab_df.at[inx, 'balance'] = new_bal
                ab_df.to_csv(DATA_DIR + '/' + ACCOUNT_BALANCES, index=False)
            else:
                f = open(DATA_DIR + '/' + ACCOUNT_BALANCES, "a")
                f.write('{},{}\n'.format(blockchain_id, amount))
                f.close()
                ab_df = pd.read_csv(DATA_DIR + '/' + ACCOUNT_BALANCES)
        except Exception as e:
            print(e)
            f = open(DATA_DIR + '/' + ACCOUNT_BALANCES, "w")
            f.write('blockchain_id,balance\n')
            f.write('{},{}\n'.format(blockchain_id, amount))
            f.close()
            ab_df = pd.read_csv(DATA_DIR + '/' + ACCOUNT_BALANCES)
        # print(list(ab_df['blockchain_id']))

    async def get_balance(self, blockchain_id):
        ab_df = pd.read_csv(DATA_DIR + '/' + ACCOUNT_BALANCES)
        if blockchain_id in list(ab_df['blockchain_id']):
            inx = ab_df.loc[ab_df['blockchain_id'] == int(blockchain_id)].index[0]
            print("Index", inx, '=', blockchain_id)
            bal = float(ab_df['balance'][inx])
        else:
            bal = False
        return(bal)


class IssueManager(object):

    def __init__(self, bm, commands_channel_id):
        self.bm = bm
        self.client = bm.client
        self.server_id = bm.server_id
        self.blockchain_channel_id = bm.blockchain_channel_id
        self.commands_channel_id = commands_channel_id
        self.issue_in_session = False
        self.vote_price = 0

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
                data = message.content.split('\n')[2].replace('Block Data: ', '')[: -1]
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
            data = message.content.split('\n')[2].replace('Block Data: ', '')[: -1]
            data = '[' + data + ']'
            data = ast.literal_eval(data)
            for t in data:
                if t[1] == self.issue_in_session and t[3] == NOTE_CONVERT:
                    converts += 1
                    convert_ids.append(t[0])
        return(converts, convert_ids)

    async def get_results(self):
        server = self.client.get_guild(id=self.server_id)
        channel = self.client.get_channel(self.blockchain_channel_id)
        converts = 0
        convert_ids = []
        should_break = False
        yes_count = 0
        no_count = 0
        async for message in channel.history(limit=None, oldest_first=False):
            # if self.issue_in_session, self.server_id, 0, NOTE_START
            data = message.content.split('\n')[2].replace('Block Data: ', '')[: -1]
            data = '[' + data + ']'
            data = ast.literal_eval(data)
            for t in data:
                if t[3] == NOTE_START and t[0] == self.issue_in_session:
                    should_break = True
                elif t[1] == str(self.server_id) and t[3][2:] == self.issue_in_session:
                    print(t[3][:2])
                    if t[3][:2] == 'Y-':
                        print('add small yes')
                        if self.vote_price > 1:
                            yes_count += float(t[2])/self.vote_price
                    elif t[3][:2] == 'N-':
                        print('add small no')
                        if self.vote_price > 1:
                            no_count += float(t[2])/self.vote_price
                elif t[1] == self.issue_in_session and t[3] == NOTE_YES:
                    print('add yes')
                    yes_count += 1
                elif t[1] == self.issue_in_session and t[3] == NOTE_NO:
                    print('add no')
                    no_count += 1
            if should_break:
                print('BREAK<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                break
        text_result = "DRAW"
        if yes_count > no_count:
            text_result = "YES"
        elif yes_count < no_count:
            text_result = "NO"
        return((text_result, yes_count, no_count))

    async def count_votes(self):
        await self.non_voters_transver()
        await asyncio.sleep(10)  # change this for end vote check on BC
        sum_traded_votes, convert_ids = await self.get_converts()
        server_bal = await self.bm.get_balance(self.server_id)
        self.vote_price = float(server_bal)/float(sum_traded_votes)
        for id in convert_ids:
            await self.bm.update_block(self.server_id, id, self.vote_price, NOTE_TRANSFER)
        print(sum_traded_votes, self.vote_price)

    async def issue_timer(self, issue_id):
        self.issue_in_session = issue_id
        await self.bm.update_block(self.issue_in_session, self.server_id, 0, NOTE_START)
        server = self.client.get_guild(id=self.server_id)
        channel = self.client.get_channel(self.commands_channel_id)
        # await asyncio.sleep(60*1)
        await channel.send("**1 min** remaining...")
        await asyncio.sleep(60*1)
        await self.bm.update_block(self.issue_in_session, self.server_id, 0, NOTE_END)
        await channel.send("*Voting Closed, counting votes...")
        await self.count_votes()
        (text_result, yes, no) = await self.get_results()
        self.issue_in_session = False
        await channel.send("Vote finished*\n**RESULT:** {} with {} in favor and {} against".format(text_result, yes, no))
        await channel.send("Use command `!mybal` to check your new balance ")
