from itertools import cycle
import asyncio
from discord.ext import commands
import discord
import os
from blockchain import Blockchain, Block
import ast
from discordibdd import BlockchainManager, IssueManager

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
NOTE_CONVERT = 'CONVERT'

bm = BlockchainManager(client, SERVER_ID, BLOCKCHAIN_CH_ID)
issue_man = IssueManager(bm, COMMANDS_CHANNEL_ID)


# Discord event Triggers

@client.event
async def on_ready():
    # game = discord.Game(name='Type: !IBDD')
    # await client.change_presence(status=discord.Status.idle, activity=game)
    await client.wait_until_ready()
    print('Bot ready!')
    server_id = SERVER_ID
    server = client.get_guild(server_id)
    if server:
        print("Connected")
    else:
        print("NOT connected")
    user = await client.fetch_user(USER_ME_ID)
    await user.send("Hello , i'm awake")
    print(user)


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
        if not issue_man.issue_in_session:
            issue_id = str(server_id) + '-' + str(channel_id) + '-' + str(message_id)
            await bm.update_block(server_id, issue_id, 0, NOTE_LOAD)
            print(args[0])
            issue_man.issue_in_session = issue_id
            client.loop.create_task(issue_man.issue_timer())
            for member in server.members:
                dont_send = ['Flux Bot#8753', 'Flux Projects#3812',
                             'XertroV#9931', 'Aus Bills#3405', 'deathlist8#3249']
                if not str(member) in dont_send:
                    print('name: {}'.format(member))
                    reply_message = await member.send('**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:negative_squared_cross_mark: NO \n:gem: Convert vote to Political Capital \n:bar_chart:  Trade Political Capital for share in vote\n`{}`'.format(issue_id))
                    for emoji in ibdd_emojis:
                        await reply_message.add_reaction(emoji)
            await ctx.send('**Vote for** *{}*  **will end in 2 mins**'.format(args[0]))
        else:
            await ctx.send("Another vote is in session")
    else:
        await ctx.send('*error*')


@client.command()
async def use(ctx, *args):
    use_amount = float(args[0])
    issue_id = issue_man.issue_in_session
    server_id = 551999201714634752
    issue_message = await issue_man.get_issue(issue_id)
    user = ctx.message.author.id
    print(issue_message)
    bal = await bm.get_balance(user)
    block_check = True
    if float(bal) - use_amount < 0:
        block_check = False
    if block_check:
        reply_message = await ctx.send("Amount to use: \n`{}`\n How do you want to vote\n`{}`".format(use_amount, issue_id))
        for emoji in ibdd_emojis[:2]:
            await reply_message.add_reaction(emoji)
    else:
        await ctx.send("**You do not have enough balance.** Current balance: `{}`".format(current_bal))


@client.command(pass_context=True)
async def mybal(ctx):
    channel = ctx.message.channel
    user = ctx.message.author.id
    bal = await bm.get_balance(user)
    print(user, bal)
    await channel.send('Your bal: `{}`'.format(bal))

# Delete messages
@client.command(pass_context=True)
async def clear(ctx, amount=100):
    if ctx.message.id == USER_ME_ID:
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=100):
            messages.append(message)
        await channel.delete_messages(messages)


@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    channel = message.channel
    if str(user.name) != 'Flux Bot':
        # print(reaction.emoji, user.name)
        if message.content[:10] == "**Vote: **":
            issue_id = message.content.split('\n')[-1].replace('`', '')
            issue_message = await issue_man.get_issue(issue_id)
            if reaction.emoji == ibdd_emojis[0]:
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await bm.update_block(user.id, issue_id, 0, NOTE_YES)
                await user.send('You have voted **YES** {} to the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
            elif reaction.emoji == ibdd_emojis[1]:
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await bm.update_block(user.id, issue_id, 0, NOTE_NO)
                await user.send('You have voted **NO** {} to the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
            elif reaction.emoji == ibdd_emojis[2]:
                await message.remove_reaction(ibdd_emojis[3], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await bm.update_block(user.id, issue_id, 0, NOTE_CONVERT)
                await user.send('You have opted to ** Convert vote to Political Capital** {} for the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
            elif reaction.emoji == ibdd_emojis[3]:
                bal = await bm.get_balance(user.id)
                await user.send('How much PC whould you like use to vote {} for the issue \n*"{}"*\nYour current balance is **{} PC** \nType: **!use** `[amount]`'.format(reaction.emoji, issue_message, bal))
        elif message.content[:8] == "Amount t":
            bal = await bm.get_balance(user.id)
            issue_id = message.content.split('\n')[3].replace('`', '')
            used = float(message.content.split('\n')[1].replace('`', ''))
            new_bal = float(bal) - float(used)
            issue_message = await issue_man.get_issue(issue_id)
            if reaction.emoji == ibdd_emojis[0]:
                await bm.update_block(user.id, SERVER_ID, used, 'Y-'+issue_id)
                the_vote = 'yes'
            elif reaction.emoji == ibdd_emojis[1]:
                await bm.update_block(user.id, SERVER_ID, used, 'N-'+issue_id)
                the_vote = 'no'
            await message.remove_reaction(ibdd_emojis[0], message.author)
            await message.remove_reaction(ibdd_emojis[1], message.author)
            await user.send('You used {} PC to vote {} {} for the issue \n*"{}"*\nYour current balance is **{} PC**'.format(used, the_vote, reaction.emoji, issue_message, new_bal))


client.loop.create_task(bm.update_blockchain())
client.run(TOKEN)
