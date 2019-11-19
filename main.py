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


async def get_issue(issue_id):
    issue_data = issue_id.split('-')
    server = client.get_guild(id=int(issue_data[0]))
    channel = client.get_channel(int(issue_data[1]))
    message = await channel.fetch_message(int(issue_data[2]))
    return(message.content.replace('!IBDD ', '').replace('"', ''))


async def send_pc():
    server_id = 551999201714634752
    voter_id = 449910203220099073
    await block_data(server_id, voter_id, 100)


async def give_balance(receiver_id, amount):
    server_id = 551999201714634752
    server_bal = await get_balance(server_id)
    new_data = 'new_data.txt'
    f = open(new_data, 'a+')
    # [sender_user_id, receiver_id, transver_amount, sender_new_bal]
    f.write('["{}","{}","{}","{}","{}"],'.format(
        server_id, receiver_id, amount, server_bal, amount))
    f.close()


async def get_balance(blockchain_id):
    server = client.get_guild(id=551999201714634752)
    channel = client.get_channel(645889124817043457)
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
                    print(t)
                    print('Current bal: {}'.format(t[3]))
                    current_bal = float(t[3])
                    should_break = True
                elif t[1] == str(blockchain_id):
                    print('id here')
                    current_bal = float(t[4])
                    should_break = True
            if should_break:
                break
        except:
            print('Bad data')
            current_bal = None
    return(current_bal)


async def block_data(sender, receiver, amount):
    s_bal = await get_balance(sender)
    r_bal = await get_balance(receiver)
    sender_bal = s_bal - amount
    receiver_bal = r_bal + amount
    if sender_bal >= 0:
        new_data = 'new_data.txt'
        f = open(new_data, 'a+')
        # [sender_user_id, receiver_id, transver_amount, sender_new_bal]
        f.write('["{}","{}","{}","{}","{}"],'.format(
            sender, receiver, amount, sender_bal, receiver_bal))
        f.close()
        return(True)
    else:
        return(False)


async def update_blockchain():
    await client.wait_until_ready()
    while not client.is_closed():
        new_data = 'new_data.txt'
        if new_data in os.listdir():
            f = open(new_data, 'r')
            data = ''
            for line in f:
                data = line
            f.close()
            blockchain.mine(Block(data))
            os.remove(new_data)
            server = client.get_guild(id=551999201714634752)
            channel = client.get_channel(645889124817043457)
            await channel.send(blockchain.block)
        await asyncio.sleep(5)


@client.event
async def on_ready():
    # game = discord.Game(name='Type: !IBDD')
    # await client.change_presence(status=discord.Status.idle, activity=game)
    print('Bot ready!')
    server_id = '551999201714634752'
    server = client.get_guild(server_id)
    if server:
        print("Yes")
    else:
        print("No")
    user = await client.fetch_user("449910203220099073")

    await user.send("Hello , i'm awake")

    print(user)


# unicode form http://www.fileformat.info/info/unicode/char/274e/index.htm
ibdd_emojis = ['\u2611', '\u274E', '\U0001F48E', '\U0001F4CA']


@client.event
async def on_message(message):
    # print("message.author: " + str(message.author) + "con: "+message.content[:10])
    try:
        if str(message.author) == 'Flux Bot#8753' and message.content[:10] == "**Vote: **":
            for emoji in ibdd_emojis:
                await message.add_reaction(emoji)
        if str(message.author) == 'Flux Bot#8753' and message.content[:8] == "You will":
            # print("YOU WILLL")
            for emoji in ibdd_emojis[:2]:
                await message.add_reaction(emoji)
    except Exception as e:
        print('Fail\n\n{}\n\n'.format(e))

    await client.process_commands(message)

# write message
@client.command(pass_context=True)
async def IBDD(ctx, *args):
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
        issue_id = str(server_id) + '-' + str(channel_id) + '-' + str(message_id)
        await give_balance(issue_id, 0)
        # global new_ibdd
        print(args[0])
        if not issue_id in os.listdir():
            f = open(issue_id, 'w')
            f.write(args[0])
            f.close()
        # new_ibdd = IssueBasedDD(issue_id, str(args[0]))
        if server:
            for member in server.members:
                dont_send = ['Flux Bot#8753', 'Flux Projects#3812', 'XertroV#9931']
                if not str(member) in dont_send:
                    print('name: {}'.format(member))
                    await member.send('**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:negative_squared_cross_mark: NO \n:gem: Convert vote to Political Capital \n:bar_chart:  Trade Political Capital for share in vote\n`{}`'.format(issue_id))
                    # await client.send_message(member, '**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:negative_squared_cross_mark: NO \n:gem: Convert vote to Political Capital \n:bar_chart:  Trade Political Capital for share in vote')
        await ctx.send('**Vote for** *{}* **will end in 5 mins**'.format(args[0]))
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
    block_check = await block_data(user, server_id, use_amount)
    #############
    if block_check:
        await ctx.send("You used {} PC credits\n`{}`".format(use_amount, issue_id))
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
        # await client.say('Messages deleted')


# assign Roles
@client.event
async def on_member_join(member):
    role = doscord.utils.get(member.server.roles, name='Cool People')
    await client.add_roles(member, role)


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
                await user.send('You have voted **YES** {} to the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
                # print(user.id)
                # print(user.name)
                # new_ibdd.vote_yes(user.id)
            elif reaction.emoji == ibdd_emojis[1]:
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await user.send('You have voted **NO** {} to the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
            elif reaction.emoji == ibdd_emojis[2]:
                await message.remove_reaction(ibdd_emojis[3], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await user.send('You have opted to ** Convert vote to Political Capital** {} for the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
            elif reaction.emoji == ibdd_emojis[3]:
                await user.send('You will **Trade Political Capital for share in vote** {} for the issue: \n*"{}"* \nHow would you like to vote?\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
        elif message.content[:8] == "You will":
            issue_id = message.content.split('\n')[-1].replace('`', '')
            issue_message = await get_issue(issue_id)
            if reaction.emoji == ibdd_emojis[1] or reaction.emoji == ibdd_emojis[0]:
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await user.send('How much PC whould you like use to vote {} for the issue \n*"{}"*\nYour current balance is **12.65 PC** \nType: **!use** `[amount]` `[issue id]`'.format(reaction.emoji, issue_message))

    # await client.send_message(channel, '{} has added {} to the the message {}'.format(user.name, reaction.emoji, reaction.message.content))


# Background task


client.loop.create_task(update_blockchain())
client.run(TOKEN)
