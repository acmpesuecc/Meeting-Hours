import discord
import os
import decouple
from dotenv import load_dotenv
from discord.utils import get

intents = discord.Intents.all()
client = discord.Client(intents=intents)

load_dotenv()
TOKEN = os.getenv('TOKEN')

@client.event
async def on_ready():
    print('I AM IN THE MATRIX [logged in]')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

client.run(TOKEN)