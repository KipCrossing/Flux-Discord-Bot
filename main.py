print("Flux Discord Bot")
import discord
from discord.ext import commands
import asyncio
from itertools import cycle


TOKEN = 'SECRETE!'

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


#unicode form http://www.fileformat.info/info/unicode/char/274e/index.htm
ibdd_emojis = ['\u2611','\u274E','\U0001F48E','\U0001F4CA']

@client.event
async def on_message(message):
    print("New message")
    for emoji in ibdd_emojis:
        await client.add_reaction(message, emoji)

    await client.process_commands(message)

#write message
@client.command()
async def IBDD(*args):
    if len(args) == 0:
        await client.say('**To create an IBDD issue to be voted on type: ** \n !IBDD "Issue to be voted on"')
    elif len(args) == 1:
        await client.say('**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:negative_squared_cross_mark: NO \n:gem: Convert vote to Political Capital \n:bar_chart:  Trade Political Capital for share in vote')
    else:
        await client.say('*error*')

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

#Background task



client.loop.create_task(change_status())
client.run(TOKEN)
