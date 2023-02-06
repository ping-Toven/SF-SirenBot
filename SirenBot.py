# SF SirenBot by Jon_HQ, Toven, KaoSxEclipse, aaPattles, Alexander, & Bopped
import os
import discord
import sqlite3
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(os.getenv("TOKEN"))
