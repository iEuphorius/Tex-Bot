import os
import random

import discord
from discord.ext import commands
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

# dice roll command
@bot.command()
async def roll(ctx, *, text: str):
    count, _, text = text.partition('d')  # eg "12d34+56" -> "12", "d", "34+56"
    size, _, offset = text.partition('+')  # eg "34+56" -> "34", "+", "56"
    if offset == "":
        offset = 0
    try:
        count = int(count)
        size = int(size)
        offset = int(offset)
    except ValueError:
        raise commands.BadArgument('bad formatting of dice value')
    return await _roll(ctx, count, size, offset)

async def _roll(ctx, count, size, offset):
    rolls = [random.randint(offset+1, offset+size) for i in range(count)]  # eg for 20 with offset 3, generate values 4 to 23
    embed = discord.Embed(title=f'Dice for {count}d{size}+{offset}')
    embed.description = '\n'.join((f'dice #{i+1}: **{roll}**' for i, roll in enumerate(rolls)))
    embed.add_field(name='sum', value=f'total = {sum(rolls)}')
    await ctx.send(embed=embed)
    
    
    
    
bot.run(TOKEN)