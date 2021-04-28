import discord
import os
import decouple
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import tasks
from pymongo import MongoClient


client = discord.Client()
mClient = MongoClient("mongodb://localhost:27017/")

db = mClient["meeting-hours"]

coll = db["polledData"]
load_dotenv()
TOKEN = os.getenv('TOKEN')


recursionflag=0
@client.event
async def on_ready():
    print('I AM IN THE MATRIX [logged in]')
    #coll.insert_one({"test": ["https://www.google.com", "https://www.twitter.com"]}) {was for test use only!}
@client.event
async def on_message(message):
    global spam_loop
    if message.author == client.user:
        return
    if message.content.startswith('-poll'):
        spam_loop.start(message)
    if message.content.startswith('-unpoll'):
        spam_loop.cancel()
    if message.content.startswith('-help'):
        message.channel.send("-poll => starts recording the minutes of the meeting and searchs for links \n-unpoll => stops collection loop")
        
@tasks.loop()
async def spam_loop(message):
    await message.channel.send("recurse")

client.run(TOKEN)

'''
ok so basically our collection will have documents of the format {user: discord_username, links:[l1,l2,l3]}
 and we will insert that into our collection and that can be accessed seperately by Chai.
'''