print("Flux Discord Bot")
import discord
from discord.ext import commands

TOKEN = 'SECRETE!'

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    await client.change_presence(game = discord.Game(name='type !IBDD'))
    print('Bot ready!')


@client.event
async def on_message(message):
    print("New message")
    await client.process_commands(message)

#write message
@client.command()
async def IBDD(*args):
    if len(args) == 0:
        await client.say('**To create an IBDD issue to be voted on type: ** \n !IBDD "Issue to be voted on"')
    elif len(args) == 1:
        await client.say('**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:x: NO \n:gem: Convert vote to Political Capital')
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





client.run(TOKEN)
