import discord 
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
load_dotenv()
bot = commands.Bot(command_prefix='.')
# bot.lava_nodes = [
#     {
#         # 'host': 'lava.link',
#         # 'port': 80,
#         # 'rest_url': f'https//{host}:{port}',
#         # 'rest_url': f'http//lava.link:80',
#         # 'password': 'anything',
#         'host': 'lavalink.eu',
#         'port': 2333,
#         'rest_url': f'http//lavalink.eu:2333',
#         'identifier': 'MAIN',
#         'password': 'Raccoon',
#         'region': 'singapore'
#     }
#             ]
@bot.command()
async def Hello(ctx):
    await ctx.reply('Hey')
    
@bot.command("How are you",pass_context=True)  
async def How_are_you(ctx):
    await ctx.reply('Good..What about you?')

@bot.command()
async def Awesome(ctx):
    await ctx.reply('Great...!')
    
    
@bot.event
async def on_ready():
    print("bot is ready")
# bot.load_extension('dismusic')
# bot.load_extension("dch")

bot.run(getenv('Token'))

