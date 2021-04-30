import discord
import os
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import tasks
from pymongo import MongoClient
# import linkwaiter


client = discord.Client()
mClient = MongoClient("mongodb://localhost:27017/")

db = mClient["meeting-hours"]

coll = db["polledData"]
load_dotenv()
TOKEN = os.getenv('TOKEN')

global link_loop


#helper_docs
embed=discord.Embed(title="Helper", url="https://del.dog/cruxagrori.txt", description="This should give you a fair idea as to how to use the bot:", color=discord.Color.red())
embed.add_field(name="-poll", value="Execute this when you want the bot to start monitoring the meeting.", inline=False)
embed.add_filed(name="-unpoll", vaule="Execute this command when you want the bot to stop monitoring your meeting", inline=True)

@client.event
async def on_ready():
    print('I AM IN THE MATRIX [logged in]')
    #coll.insert_one({"test": ["https://www.google.com", "https://www.twitter.com"]}) {was for test use only!} dbstructure of saving links
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('-poll'):
        link_loop.start()
    if message.content.startswith('-unpoll'):
        link_loop.cancel()
    if message.content.startswith("-help"):
        await message.channel.send(embed=embed)
        
@tasks.loop()
async def link_loop():
    message = await client.wait_for("message", check=lambda message: message.author == message.author)
    await message.channel.send(message.content)
    # print(message)
    # if linker.linkfn(coll,message) :
        
client.run(TOKEN)

'''
ok so basically our collection will have documents of the format {user: discord_username, links:[l1,l2,l3]}
 and we will insert that into our collection and that can be accessed seperately by Chai.
'''