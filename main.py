from ibdd import IssueBasedDD
from itertools import cycle
import asyncio
from discord.ext import commands
import discord
import os
from blockchain import Blockchain, Block
import ast

print("Flux Discord Bot")

blockchain = Blockchain()


TOKEN = os.environ['IBDD_DISCORD_BOT_TOKEN']


client = commands.Bot(command_prefix='!')

status = ['Have fun!', 'VOTE FLUX', 'Type: !IBDD']
# unicode form http://www.fileformat.info/info/unicode/char/274e/index.htm
ibdd_emojis = ['\u2611', '\u274E', '\U0001F48E', '\U0001F4CA']
SERVER_ID = 551999201714634752
BLOCKCHAIN_CH_ID = 645889124817043457
COMMANDS_CHANNEL_ID = 551999201714634757
USER_ME_ID = 449910203220099073
FLUX_BOT_ID = 551997414978879499
VOTER = 'Voter'
NOTE_TRANSFER = 'TRANSFER'
NOTE_LOAD = 'LOAD'
NOTE_YES = 'YES'
NOTE_NO = 'NO'
NEW_DATA = 'new_data.txt'
NOTE_CONVERT = 'CONVERT'
issue_in_session = False


async def get_issue(issue_id):
    issue_data = issue_id.split('-')
    server = client.get_guild(id=int(issue_data[0]))
    channel = client.get_channel(int(issue_data[1]))
    message = await channel.fetch_message(int(issue_data[2]))
    return(message.content.replace('!IBDD ', '').replace('"', ''))


async def send_pc(voter_id, amount):
    server_id = SERVER_ID
    await block_data(server_id, voter_id, amount, NOTE_TRANSFER)


async def load_balance(receiver_id, amount):
    server_id = SERVER_ID
    server_bal = await get_balance(server_id)
    f = open(NEW_DATA, 'a+')
    # [sender_user_id, receiver_id, transver_amount, sender_new_bal]
    f.write('["{}","{}","{}","{}","{}","{}"],'.format(
        server_id, receiver_id, amount, server_bal, amount, NOTE_LOAD))
    f.close()


async def get_balance(blockchain_id):
    server = client.get_guild(id=SERVER_ID)
    channel = client.get_channel(BLOCKCHAIN_CH_ID)
    messages = []
    counter = 0
    current_bal = None
    async for message in channel.history(limit=None, oldest_first=False):
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


async def block_data(sender, receiver, amount, note):
    s_bal = await get_balance(sender)
    r_bal = await get_balance(receiver)
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


async def update_blockchain():
    print('Update blockchain')
    await client.wait_until_ready()
    print(client.is_closed())
    while not client.is_closed():
        if NEW_DATA in os.listdir():
            f = open(NEW_DATA, 'r')
            data = ''
            for line in f:
                data = line
            f.close()
            blockchain.mine(Block(data))
            os.remove(NEW_DATA)
            server = client.get_guild(id=SERVER_ID)
            channel = client.get_channel(BLOCKCHAIN_CH_ID)
            await channel.send(blockchain.block)
        await asyncio.sleep(5)


async def non_voters_transver():
    global issue_in_session
    server = client.get_guild(id=SERVER_ID)
    channel = client.get_channel(BLOCKCHAIN_CH_ID)
    messages = []
    counter = 0
    current_bal = None
    print(issue_in_session)
    for member in server.members:
        print(member.id)
        voted = False
        async for message in channel.history(limit=None, oldest_first=False):
            data = message.content.split('\n')[2].replace('Block Data: ', '')[:-1]
            data = '[' + data + ']'
            data = ast.literal_eval(data)
            for t in data:
                if t[0] == str(member.id) and t[1] == issue_in_session:
                    voted = True
        if voted:
            print(member.id, 'voted')
        else:
            await block_data(member.id, issue_in_session, 0, NOTE_CONVERT)


async def get_converts():
    global issue_in_session
    server = client.get_guild(id=SERVER_ID)
    channel = client.get_channel(BLOCKCHAIN_CH_ID)
    converts = 0
    convert_ids = []
    async for message in channel.history(limit=None, oldest_first=False):
        data = message.content.split('\n')[2].replace('Block Data: ', '')[:-1]
        data = '[' + data + ']'
        data = ast.literal_eval(data)
        for t in data:
            if t[1] == issue_in_session and t[5] == NOTE_CONVERT:
                converts += 1
                convert_ids.append(t[0])

    return(converts, convert_ids)


async def count_votes():
    await non_voters_transver()
    await asyncio.sleep(10)  # change this for end vote check on BC
    sum_traded_votes, convert_ids = await get_converts()
    server_id = SERVER_ID
    server_bal = await get_balance(server_id)
    vote_price = round(float(server_bal)/float(sum_traded_votes), 2)
    for id in convert_ids:
        await block_data(server_id, id, vote_price, NOTE_TRANSFER)
    print(sum_traded_votes, vote_price)


async def issue_timer():
    global issue_in_session
    server = client.get_guild(id=SERVER_ID)
    channel = client.get_channel(COMMANDS_CHANNEL_ID)
    await asyncio.sleep(60*1)
    await channel.send("1 min remaining")
    await asyncio.sleep(60*1)
    await channel.send("Vote finished")
    await count_votes()
    issue_in_session = False


@client.event
async def on_ready():
    # game = discord.Game(name='Type: !IBDD')
    # await client.change_presence(status=discord.Status.idle, activity=game)

    print('Bot ready!')
    server_id = SERVER_ID
    server = client.get_guild(server_id)
    for member in server.members:
        bal = await get_balance(member.id)
        if not bal:
            await load_balance(member.id, 100)  # Change 100 to calculated mean
        print(member.name, bal)
    if server:
        print("Connected")
    else:
        print("NOT connected")
    user = await client.fetch_user(USER_ME_ID)
    await user.send("Hello , i'm awake")
    print(user)


@client.event
async def on_message(message):
    # print("message.author: " + str(message.author) + "con: "+message.content[:10])
    try:
        if message.author.id == FLUX_BOT_ID and message.content[:10] == "**Vote: **":
            for emoji in ibdd_emojis:
                await message.add_reaction(emoji)
        if message.author.id == FLUX_BOT_ID and message.content[:8] == "You will":
            # print("YOU WILLL")
            for emoji in ibdd_emojis[:2]:
                await message.add_reaction(emoji)
        if message.author.id == FLUX_BOT_ID and message.content[:8] == "Amount t":
            for emoji in ibdd_emojis[:2]:
                await message.add_reaction(emoji)

    except Exception as e:
        print('Fail\n\n{}\n\n'.format(e))

    await client.process_commands(message)

# write message
@client.command(pass_context=True)
async def IBDD(ctx, *args):
    global issue_in_session
    server_id = ctx.message.guild.id
    channel_id = ctx.message.channel.id
    message_id = ctx.message.id
    server = client.get_guild(id=server_id)
    channel = client.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    print(message.content)
    if len(args) == 0:
        await ctx.send('**To create an IBDD issue to be voted on type: ** \n !IBDD "Issue to be voted on"')
    elif len(args) == 1:
        if not issue_in_session:
            issue_id = str(server_id) + '-' + str(channel_id) + '-' + str(message_id)
            await load_balance(issue_id, 0)
            print(args[0])
            issue_in_session = issue_id
            client.loop.create_task(issue_timer())
            for member in server.members:
                dont_send = ['Flux Bot#8753', 'Flux Projects#3812',
                             'XertroV#9931', 'Aus Bills#3405']
                if not str(member) in dont_send:
                    print('name: {}'.format(member))
                    await member.send('**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:negative_squared_cross_mark: NO \n:gem: Convert vote to Political Capital \n:bar_chart:  Trade Political Capital for share in vote\n`{}`'.format(issue_id))
                    # await client.send_message(member, '**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:negative_squared_cross_mark: NO \n:gem: Convert vote to Political Capital \n:bar_chart:  Trade Political Capital for share in vote')
            await ctx.send('**Vote for** *{}*  **will end in 2 mins**'.format(args[0]))
        else:
            await ctx.send("Another vote is in session")
    else:
        await ctx.send('*error*')

# write message
@client.command()
async def use(ctx, *args):

    use_amount = float(args[0])
    issue_id = args[1]
    server_id = 551999201714634752
    issue_message = await get_issue(issue_id)
    user = ctx.message.author.id
    print(issue_message)
    block_check = True  # use check bal here
    #############
    if block_check:
        await ctx.send("Amount to use: \n`{}`\n How do you want to vote\n`{}`".format(use_amount, issue_id))
    else:
        await ctx.send("**You do not have enough balance.** Current balance: `{}`".format(current_bal))


# Read and write
@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)


@client.command(pass_context=True)
async def mybal(ctx):
    channel = ctx.message.channel
    user = ctx.message.author.id
    bal = await get_balance(user)
    print(user, bal)

    await channel.send('Your bal: `{}`'.format(bal))

# Delete messages
@client.command(pass_context=True)
async def clear(ctx, amount=100):
    if str(ctx.message.author) == 'KipDawgz#8789':
        channel = ctx.message.channel
        messages = []
        counter = 0
        async for message in channel.history(limit=100):
            messages.append(message)
        await channel.delete_messages(messages)


# assign Roles
@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=VOTER)
    await member.add_roles(role)


@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    channel = message.channel
    if str(user.name) != 'Flux Bot':
        # print(reaction.emoji, user.name)
        if message.content[:10] == "**Vote: **":

            issue_id = message.content.split('\n')[-1].replace('`', '')
            issue_message = await get_issue(issue_id)
            if reaction.emoji == ibdd_emojis[0]:
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await block_data(user.id, issue_id, 0, NOTE_YES)
                await user.send('You have voted **YES** {} to the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
                # print(user.id)
                # print(user.name)
                # new_ibdd.vote_yes(user.id)
            elif reaction.emoji == ibdd_emojis[1]:
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await block_data(user.id, issue_id, 0, NOTE_NO)
                await user.send('You have voted **NO** {} to the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
            elif reaction.emoji == ibdd_emojis[2]:
                await message.remove_reaction(ibdd_emojis[3], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await block_data(user.id, issue_id, 0, NOTE_CONVERT)
                await user.send('You have opted to ** Convert vote to Political Capital** {} for the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
            elif reaction.emoji == ibdd_emojis[3]:
                bal = await get_balance(user.id)
                await user.send('How much PC whould you like use to vote {} for the issue \n*"{}"*\nYour current balance is **{} PC** \nType: **!use** `[amount]` `[issue id]`'.format(reaction.emoji, issue_message, bal))
                # await user.send('You will **Trade Political Capital for share in vote** {} for the issue: \n*"{}"* \nHow would you like to vote?\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
        elif message.content[:8] == "Amount t":
            bal = await get_balance(user.id)
            issue_id = message.content.split('\n')[3].replace('`', '')
            used = float(message.content.split('\n')[1].replace('`', ''))
            new_bal = float(bal) - float(used)
            issue_message = await get_issue(issue_id)
            if reaction.emoji == ibdd_emojis[0]:
                await block_data(user.id, SERVER_ID, used, 'Y-'+issue_id)
                the_vote = 'yes'
            elif reaction.emoji == ibdd_emojis[1]:
                await block_data(user.id, SERVER_ID, used, 'Y-'+issue_id)
                the_vote = 'no'
            await message.remove_reaction(ibdd_emojis[0], message.author)
            await message.remove_reaction(ibdd_emojis[1], message.author)
            await user.send('You used {} PC to vote {} {} for the issue \n*"{}"*\nYour current balance is **{} PC**'.format(used, the_vote, reaction.emoji, issue_message, new_bal))

    # await client.send_message(channel, '{} has added {} to the the message {}'.format(user.name, reaction.emoji, reaction.message.content))


# Background task


client.loop.create_task(update_blockchain())
client.run(TOKEN)
