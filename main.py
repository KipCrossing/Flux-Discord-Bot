print("Flux Discord Bot")
import discord
from discord.ext import commands

TOKEN = 'SECRETE!'

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Bot ready!')


@client.event
async def on_message(message):
    print("New message")
    await client.process_commands(message)

@client.command()
async def ping():
    await client.say('Pong!!!')

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)



@client.command()
async def hi():
    await client.say('Hello!')

@client.command(pass_context = True)
async def clear(ctx, amount = 100):
    channel = ctx.message.channel
    messages = []
    counter = 0
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted')

client.run(TOKEN)
