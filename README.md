# Flux Discord Bot

## Intro

The purpose of this project is to create a simple version of IBDD to help others create familiarity with the concept and to be able to test how to would work in practice (and perhaps gain unforeseen insight). For the UI, I decided to go with a discord server and to create a 'Discord bot' that handles all of the human interactions. The reasons I decided to make the project with Discord include:

- Existing Libraries for making discord bots
- Discord already has users
- Discord allows for a wide range of customisation features (roles, channels, emojis)

![alt text](assets/Flux-bot-example.png)

It would be good to share this project so that discord communities can manage their servers by making the "Flux Bot" the owner. This way new discord management decisions can be made collectively via IBDD. For instance, the creation of a new channel may be put to a vote, instead of an owner making all decisions. I imagine that using a flux bot to manage your server it will help create a sense of community ownership.

### Philosophy

This bot will take advantage of the [Vote swapping](docs/VOTE-SWAPPING.md) aspect of [IBDD](docs/ISSUE_BASED_DIRECT_DEMOCRACY.md) and will calculate the values of votes based on a [Simple Blind Ratio](docs/VOTE-SWAPPING.md). Further, Political Capital (PC) will be inflated based on the recommendation that are outlined in [The-Liquidity-Problem](docs/THE-LIQUIDITY-PROBLEM.md)

### The Blockchain

For educational purposes, I decided to include a blockchain to record transactions. The voting data on the blockchain is structured according to:

The structure of the data with the blockchain are described here: [Blockchain Data](docs/BLOCKCHAIN_DATA.md)

## Getting Started

```
python3 -m pip install -U discord.py
git clone https://github.com/KipCrossing/Flux-Discord-Bot
cd Flux-Discord-Bot
python3 main.py
```

See [here](https://discordpy.readthedocs.io/en/latest/) for the discord.py docs.

## TODO

- Save account balance data via SQL
- redo get_bal function
- distribute PC
- calculate outcome
- Add inflation PC to all voters

# Upcoming Features

- Devs to be able to create unique opperations (eg a vote on create channel)
- Votes on federal bills
