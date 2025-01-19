import os
import random

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents(messages=True, guilds=True, members=True) 
intents.message_content = True
bot = commands.Bot(intents=intents,command_prefix='!', help_command=commands.DefaultHelpCommand())



@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    """ members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}') """

# @bot.event
# async def on_member_join(member):
#     await  member.create_dm()
#     await member.dm_channel.send(
#         f'''Hi {member.name}, welcome to the Birth of a city discord server! Check out the 
#         https://discord.com/channels/857435909343805490/1159623640434880613 channel for general server rules and the pinned 
#         messages in https://discord.com/channels/857435909343805490/1160001533258256435. After you have done that we will get 
#         you roles so you can access the rest of the server!'''
#     )