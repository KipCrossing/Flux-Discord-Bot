# Flux Discord Bot

The purpose of this project is to create a simple version of IBDD to help others create familiarity with the concept and to be able to test how to would work in practice (and perhaps gain unforeseen insight). For the UI, I decided to go with a discord server and to create a 'Discord bot' that handles all of the human interactions. The reasons I decided to make the project with Discord include:

- Existing Libraries for making discord bots
- Discord already has users
- Discord allows for a wide range of customisation features (roles, channels, emojis)

This bot will take advantage of the _Vote swapping_ aspect of IBDD and will calculate the values of votes based on a [Simple Blind Ratio](VOTE-SWAPPING.md).

It would be good to share this project so that discord communities can manage their servers by making the "Flux Bot" the owner. This way new discord management decisions can be made collectively via IBDD. For instance, the creation of a new channel may be put to a vote, instead of an owner making all decisions. I imagine that using a flux bot to manage your server it will help create a sense of community ownership.

![alt text](https://github.com/KipCrossing/Flux-Discord-Bot/blob/master/Flux-bot-example.png)

## Getting Started

```
python3 -m pip install -U discord.py
git clone https://github.com/KipCrossing/Flux-Discord-Bot
cd Flux-Discord-Bot
python3 main.py
```

See [here](https://discordpy.readthedocs.io/en/latest/) for the discord.py docs.

## TODO

- Auto transfer/trade non voters
- calculate SBR
- distribute PC
- calculate outcome
- Add inflation PC to all voters

# Upcoming Features

- Devs to be able to create unique opperations (eg a vote on create channel)
- Votes on federal bills
