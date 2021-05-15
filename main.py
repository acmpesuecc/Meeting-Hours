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
import linkfinder

intents = discord.Intents.all()
client = discord.Client(intents=intents)
mClient = MongoClient("mongodb://localhost:27017/")

db = mClient["meeting-hours"]
coll = db["polledData"]
load_dotenv()
TOKEN = os.getenv('TOKEN')

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
    f=open(str(message.guild.id)+".json")
    props=json.load(f)
    f.close()

    if message.author == client.user:
        return
    await linkfinder.linkdetect(message)
    if message.content.startswith('-poll'):
        print(props)
        print(message.guild.id)
        if props['poll_flag'] == "false":
            await message.channel.send("Starting to monitor current meeting!")
            props['poll_flag']="true"
            props['links']={}
            json_dumper(props,message.guild.id)
        else:
            await message.channel.send("You have already used the poll command and the bot is monitor the ongoing meeting!")
    if message.content.startswith('-unpoll'):
        if props['poll_flag']=="true":
            await message.channel.send("Unpolled!")
            props['poll_flag']="false"
            json_dumper(props,message.guild.id)
        else:
            await message.channel.send("You never polled to begin with!")
        
    if message.content.startswith("-help"):
        await message.channel.send(embed=embed)
        
client.run(TOKEN)