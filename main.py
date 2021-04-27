import discord
import os
import decouple
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import tasks


client = discord.Client()

load_dotenv()
TOKEN = os.getenv('TOKEN')


recursionflag=0
@client.event
async def on_ready():
    print('I AM IN THE MATRIX [logged in]')

@client.event
async def on_message(message):
    global spam_loop
    if message.author == client.user:
        return
    if message.content.startswith('-poll'):
        spam_loop.start(message)
    if message.content.startswith('-unpoll'):
        spam_loop.cancel()
        
@tasks.loop()
async def spam_loop(message):
    await message.channel.send("recurse")

client.run(TOKEN)