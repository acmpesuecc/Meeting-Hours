import discord
import os
import os.path
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import tasks
from pymongo import MongoClient
import re
import asyncio
import json

intents = discord.Intents.all()
client = discord.Client(intents=intents)
mClient = MongoClient("mongodb://localhost:27017/")

db = mClient["meeting-hours"]
coll = db["polledData"]
load_dotenv()
TOKEN = os.getenv('TOKEN')

global link_loop
# global poll_flag
# poll_flag=False
# global links
# links={}

def json_dumper(jsonobject,jsonfile):
    f=open(str(jsonfile)+".json","w")
    json.dump(jsonobject,f)
    f.close()



#helper_docs
embed=discord.Embed(title="Helper", url="https://del.dog/cruxagrori.txt", description="This should give you a fair idea as to how to use the bot:", color=discord.Color.red())
embed.add_field(name="-poll", value="Execute this when you want the bot to start monitoring the meeting.", inline=False)
embed.add_field(name="-unpoll", value="Execute this command when you want the bot to stop monitoring your meeting", inline=True)
#-------------------------------------------------------------------------------------------------------------------

@client.event
async def on_ready():
    print('I AM IN THE MATRIX [logged in]')
    #coll.insert_one({"test": ["https://www.google.com", "https://www.twitter.com"]}) {was for test use only!} dbstructure of saving links
@client.event
async def on_message(message):
    if os.path.exists(str(message.guild.id)+".json"):
        pass
    else:
        f=open(str(message.guild.id)+".json","w+")
        w=open("jsontemplate.json","r")
        f.write(w.read())
        f.close()
        w.close()
    # global poll_flag
    f=open(str(message.guild.id)+".json")
    props=json.load(f)
    f.close()

    if message.author == client.user:
        return
    if message.content.startswith('-poll'):
        print(props)
        if props['poll_flag'] == "false":
            link_loop.start()
            await message.channel.send("Starting to monitor current meeting!")
            props['poll_flag']="true"
            json_dumper(props,message.guild.id)
        else:
            await message.channel.send("You have already used the poll command and the bot is monitor the ongoing meeting!")
    if message.content.startswith('-unpoll'):
        if props['poll_flag']=="true":
            await message.channel.send("Unpolled!")
            props['poll_flag']="false"
            json_dumper(props,message.guild.id)
            link_loop.cancel()
        else:
            await message.channel.send("You never polled to begin with!")
        
    if message.content.startswith("-help"):
        await message.channel.send(embed=embed)
        
@tasks.loop()
async def link_loop():
    message = await client.wait_for("message", check=lambda message: message.author != client.user)
    f=open(str(message.guild.id)+".json")
    props=json.load(f)
    f.close()
    if props['poll_flag']=="true":
        msg=str(message.content)
        # global links
        if re.search(r'(http://|https://|ftp://|ftps://|www.)?[\w]+\.[\w]{2,3}(\S*)' ,msg):
            print("Link Found!")
            await message.channel.send("Link Found!Adding to records.")
            print(message.author.name)
            if str(message.author.name) in props["links"].keys():
                pass
            else:
                props["links"][str(message.author.name)]=[]
            for match in re.finditer(r"(http://|https://|ftp://|ftps://|www.)?[\w]+\.[\w]{2,3}(\S*)",msg):
                props["links"][str(message.author.name)].append(match.group())
                json_dumper(props,message.guild)
            print(props["links"])
        
client.run(TOKEN)





'''
ok so basically our collection will have documents of the format {user: discord_username, links:[l1,l2,l3]}
 and we will insert that into our collection and that can be accessed seperately by Chai.
'''