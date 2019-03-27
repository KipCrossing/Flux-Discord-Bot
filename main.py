print("Flux Discord Bot")
import os
import discord
from discord.ext import commands
import asyncio
from itertools import cycle
from ibdd import IssueBasedDD


TOKEN = os.environ['IBDD_DISCORD_BOT_TOKEN']

client = commands.Bot(command_prefix = '!')

status = ['Have fun!','VOTE FLUX','Type: !IBDD']



async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)
    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game = discord.Game(name=current_status))
        await asyncio.sleep(10)

@client.event
async def on_ready():
    await client.change_presence(game = discord.Game(name='Type: !IBDD'))
    print('Bot ready!')
    server_id = '551999201714634752'
    server = client.get_server(server_id)
    if server:
        print("Yes")
    else:
        print("No")


#unicode form http://www.fileformat.info/info/unicode/char/274e/index.htm
ibdd_emojis = ['\u2611','\u274E','\U0001F48E','\U0001F4CA']

@client.event
async def on_message(message):
    print("message.author: " + str(message.author) + "con: "+message.content[:10])
    if str(message.author) == 'Flux Bot#8753' and message.content[:10] == "**Vote: **":
        for emoji in ibdd_emojis:
            await client.add_reaction(message, emoji)
    if str(message.author) == 'Flux Bot#8753' and message.content[:8] == "You will":
        print("YOU WILLLLLLLLLLLLLL")
        for emoji in ibdd_emojis[:2]:
            await client.add_reaction(message, emoji)


    await client.process_commands(message)

#write message
@client.command(pass_context = True)
async def IBDD(ctx, *args):
    server_id = ctx.message.server.id
    print("Server ID")
    print(server_id)
    print(type(server_id))
    server = client.get_server(id = server_id)
    if len(args) == 0:
        await client.say('**To create an IBDD issue to be voted on type: ** \n !IBDD "Issue to be voted on"')
    elif len(args) == 1:
        global new_ibdd
        new_ibdd = IssueBasedDD(str(args[0]))
        if server:
            for member in server.members:
                if 'Flux Bot#8753' != str(member):
                    print('name: {}'.format(member))
                    await client.send_message(member,'**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:negative_squared_cross_mark: NO \n:gem: Convert vote to Political Capital \n:bar_chart:  Trade Political Capital for share in vote')
        await client.say('**Vote for** *{}* **will end in 5 mins**'.format(args[0]))
    else:
        await client.say('*error*')

#write message
@client.command()
async def use(*args):
    output = ''
    for word in args:
        output += str(word)
        output += ' '
    await client.say("You used {} PC credits".format(output))


#Read and write
@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)


#Delete messages
@client.command(pass_context = True)
async def clear(ctx, amount = 100):
    channel = ctx.message.channel
    messages = []
    counter = 0
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted')


#assign Roles
@client.event
async def on_member_join(member):
    role = doscord.utils.get(member.server.roles, name = 'Cool People')
    await client.add_roles(member,role)



@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    channel = message.channel
    if str(user.name) != 'Flux Bot':
        print(reaction.emoji, user.name)
        if message.content[:10] == "**Vote: **":
            if reaction.emoji == ibdd_emojis[0]:
                await client.send_message(user, 'You have voted **YES** {} to the issue: *{}*'.format( reaction.emoji, reaction.message.content.split('\n')[0][10:]))
                new_ibdd.vote_yes(user)
            elif reaction.emoji == ibdd_emojis[1]:
                await client.send_message(user, 'You have voted **NO** {} to the issue: *{}*'.format( reaction.emoji, reaction.message.content.split('\n')[0][10:]))
            elif reaction.emoji == ibdd_emojis[2]:
                await client.send_message(user, 'You have opted to ** Convert vote to Political Capital** {} for the issue: *{}*'.format( reaction.emoji, reaction.message.content.split('\n')[0][10:]))
            elif reaction.emoji == ibdd_emojis[3]:
                await client.send_message(user, 'You will **Trade Political Capital for share in vote** {} for the issue: *"{}"*. \nHow would you like to vote?'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:]))
        elif message.content[:8] == "You will":
            if reaction.emoji == ibdd_emojis[1] or reaction.emoji == ibdd_emojis[0]:
                await client.send_message(user,"How much PC whould you like to use? \n Your current balance is **12.65 PC** \n Type: **!use** `[amount]`")


    #await client.send_message(channel, '{} has added {} to the the message {}'.format(user.name, reaction.emoji, reaction.message.content))


#Background task



client.loop.create_task(change_status())
client.run(TOKEN)
