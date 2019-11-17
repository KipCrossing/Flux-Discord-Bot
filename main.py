from ibdd import IssueBasedDD
from itertools import cycle
import asyncio
from discord.ext import commands
import discord
import os
print("Flux Discord Bot")


TOKEN = os.environ['IBDD_DISCORD_BOT_TOKEN']

client = commands.Bot(command_prefix='!')

status = ['Have fun!', 'VOTE FLUX', 'Type: !IBDD']


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)
    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(10)


@client.event
async def on_ready():
    game = discord.Game(name='Type: !IBDD')

    await client.change_presence(status=discord.Status.idle, activity=game)
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
    print("message.author: " + str(message.author) + "con: "+message.content[:10])
    if str(message.author) == 'Flux Bot#8753' and message.content[:10] == "**Vote: **":
        for emoji in ibdd_emojis:
            await message.add_reaction(emoji)
    if str(message.author) == 'Flux Bot#8753' and message.content[:8] == "You will":
        print("YOU WILLL")
        for emoji in ibdd_emojis[:2]:
            await message.add_reaction(emoji)

    await client.process_commands(message)

# write message
@client.command(pass_context=True)
async def IBDD(ctx, *args):
    server_id = ctx.message.guild.id
    print("Server ID")
    print(server_id)
    print(type(server_id))
    server = client.get_guild(id=server_id)
    if len(args) == 0:
        await ctx.send('**To create an IBDD issue to be voted on type: ** \n !IBDD "Issue to be voted on"')
    elif len(args) == 1:
        global new_ibdd
        print(args[0])
        new_ibdd = IssueBasedDD(str(args[0]))
        if server:
            for member in server.members:
                if 'Flux Bot#8753' != str(member) and 'Flux Projects#3812' != str(member):
                    print('name: {}'.format(member))
                    await member.send('**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:negative_squared_cross_mark: NO \n:gem: Convert vote to Political Capital \n:bar_chart:  Trade Political Capital for share in vote')
                    # await client.send_message(member, '**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:negative_squared_cross_mark: NO \n:gem: Convert vote to Political Capital \n:bar_chart:  Trade Political Capital for share in vote')
        await ctx.send('**Vote for** *{}* **will end in 5 mins**'.format(args[0]))
    else:
        await ctx.send('*error*')

# write message
@client.command()
async def use(ctx, *args):
    output = ''
    for word in args:
        output += str(word)
        output += ' '
    await ctx.send("You used {} PC credits".format(output))


# Read and write
@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)


# Delete messages
@client.command(pass_context=True)
async def clear(ctx, amount=100):
    if str(ctx.message.author) == 'KipDawgz#8789':
        channel = ctx.message.channel
        messages = []
        counter = 0
        async for message in client.logs_from(channel, limit=int(amount)):
            messages.append(message)
        await client.delete_messages(messages)
        await client.say('Messages deleted')


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
        print(reaction.emoji, user.name)
        if message.content[:10] == "**Vote: **":
            if reaction.emoji == ibdd_emojis[0]:
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await user.send('You have voted **YES** {} to the issue: *{}*'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:]))
                print(user.id)
                print(user.name)
                new_ibdd.vote_yes(user.id)
            elif reaction.emoji == ibdd_emojis[1]:
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await user.send('You have voted **NO** {} to the issue: *{}*'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:]))
            elif reaction.emoji == ibdd_emojis[2]:
                await message.remove_reaction(ibdd_emojis[3], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await user.send('You have opted to ** Convert vote to Political Capital** {} for the issue: *{}*'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:]))
            elif reaction.emoji == ibdd_emojis[3]:
                await user.send('You will **Trade Political Capital for share in vote** {} for the issue: *"{}"*. \nHow would you like to vote?'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:]))
        elif message.content[:8] == "You will":
            if reaction.emoji == ibdd_emojis[1] or reaction.emoji == ibdd_emojis[0]:
                await user.send("How much PC whould you like to use? \n Your current balance is **12.65 PC** \n Type: **!use** `[amount]`")

    # await client.send_message(channel, '{} has added {} to the the message {}'.format(user.name, reaction.emoji, reaction.message.content))


# Background task


client.loop.create_task(change_status())
client.run(TOKEN)
