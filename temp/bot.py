import discord
from discord.ext import commands
from music import music

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def hello(ctx):
    await ctx.send("Hi")

client.add_cog(music(client))

client.run("OTM3Mjc3NzY1MDk3NTA0ODE4.YfZZ8A.IgZ34jJzv4AOYHZxzbcrlIFaAEc")