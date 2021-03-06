import discord
import os
import os.path
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import tasks
from pymongo import MongoClient
import re
import json



def json_dumper(jsonobject,jsonfile):
    f = open(str(jsonfile)+".json","w")
    json.dump(jsonobject,f)
    f.close()

async def linkdetect(message):
    f = open(str(message.guild.id)+".json")
    props = json.load(f)
    f.close()
    if props["poll_flag"] == "true":
        msg = str(message.content)
        if re.search(r'(http://|https://|ftp://|ftps://|www.)?[\w]+\.[\w]{2,3}(\S*)',msg):
            await message.channel.send("Link Found!Adding to records.")
            if str(message.author.name) in props["links"].keys():
                pass
            else:
                props["links"][str(message.author.name)] = []
            for match in re.finditer(r"(http://|https://|ftp://|ftps://|www.)?[\w]+\.[\w]{2,3}(\S*)",msg):
                editablelist = props["links"][str(message.author.name)]
                editablelist.append(match.group())
                props["links"][str(message.author.name)] = editablelist
                json_dumper(props,message.guild.id)