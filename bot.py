import os
import random
import sqlite3

import discord
from discord.ext import commands
from dotenv import load_dotenv

import characterDatabase

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents(messages=True, guilds=True, members=True) 
intents.message_content = True
bot = commands.Bot(intents=intents,command_prefix='!', help_command=commands.DefaultHelpCommand())

conn = sqlite3.connect("characters.db")
cursor = conn.cursor()

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    
# END SERVER INIT

# dice roll command
@bot.command()
async def roll(ctx, *, text: str):
    count, _, text = text.partition('d')  # eg "12d34+56" -> "12", "d", "34+56"
    if "-" in text:
        size, _, offset = text.partition('-')  # eg "34+56" -> "34", "+", "56"
        offset = int(offset)
        offset = offset-(2 * offset)        
    else:
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
    rolls = [random.randint(1, size) for i in range(count)]  # eg for 20 with offset 3, generate values 4 to 23
    if offset > 0:
        embed = discord.Embed(title=f'Dice for {count}d{size}+{offset}')
    elif offset < 0:
        embed = discord.Embed(title=f'Dice for {count}d{size}{offset}')
    else:
        embed = discord.Embed(title=f'Dice for {count}d{size}')
    
    embed.description = '\n'.join((f'dice #{i+1}: **{roll}**' for i, roll in enumerate(rolls)))
    embed.add_field(name = 'sum', value=f'total = {sum(rolls)+offset}')
    await ctx.send(embed = embed)
    
@bot.command()    
async def attributes(ctx):
    embed = discord.Embed(title=f'Rolling attributes!')
    for i in range(6):
        rolls = [random.randint(1,6) for i in range(3)]        
        embed.add_field(name = 'Attribute', value={sum(rolls)}, inline=False)
    await ctx.send(embed = embed)
    
@bot.command()    
async def Tex(ctx):
    print("use '!roll 1d4+1' to make a roll")
    print("use '!attributes to roll your starting attributes")
    


@bot.command()
async def newCharacter(ctx, name: str, char_class: str, level: int, credits: int, hp: int):
    user_id = ctx.author.id

    character = characterDatabase.Character(user_id, name, char_class, level, credits, hp)

    success = characterDatabase.create_character(character)

    if not success:
        await ctx.send("You already have a character!")
        return

    await ctx.send(
        f"Character created!\n"
        f"Name: {name}\n"
        f"Class: {char_class}\n"
        f"HP: {character.hp}\n"
        f"Credits: {character.credits}"
    )
    

@bot.command()
async def character(ctx):
    data = characterDatabase.get_character(ctx.author.id)

    if not data:
        await ctx.send("You don't have a character yet. Use !create")
        return

    await ctx.send(
        f"**{data['name']}**\n"
        f"Class: {data['class']}\n"
        f"Level: {data['level']}\n"
        f"Credits: {data['credits']}\n"
        f"HP: {data['hp']}/{data['maxHP']}"
    )

@bot.command()
async def delete(ctx):
    user_id = ctx.author.id

    await ctx.send("Are you sure? Type `yes` to confirm.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)

    if msg.content.lower() != "yes":
        await ctx.send("Cancelled.")
        return

    success = characterDatabase.delete_character(user_id)

    if success:
        await ctx.send("Character deleted.")
    else:
        await ctx.send("No character found.")

# command to view character
# !viewchar @Taylor
@bot.command()
@commands.has_permissions(administrator=True)
async def viewchar(ctx, member: discord.Member):
    data = characterDatabase.get_character_by_user_id(member.id)

    if not data:
        await ctx.send("That user has no character.")
        return

    await ctx.send(
        f"**Character Sheet**\n"
        f"Name: {data[1]}\n"
        f"Class: {data[2]}\n"
        f"Level: {data[3]}\n"
        f"Credits: {data[4]}\n"
        f"HP: {data[5]}/{data[6]}"
    )

# command to edit characters
# !editchar @Taylor level 5
# !editchar @Taylor credits 2000
# !editchar @Taylor hp 80

@bot.command()
@commands.has_permissions(administrator=True)
async def editchar(ctx, member: discord.Member, field: str, value):
    success = characterDatabase.update_character_field(member.id, field, value)

    if not success:
        ALLOWED_FIELDS = ["name", "char_class", "level", "credits", "hp", "maxHP"]
        await ctx.send(f"Invalid field. Valid fields: {', '.join(ALLOWED_FIELDS)}")
        return

    await ctx.send(
        f"Updated {field} for {member.display_name} to {value}"
    )


bot.run(TOKEN)