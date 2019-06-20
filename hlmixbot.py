import discord
from discord.ext import commands
from discord.ext.commands import Bot

from libs.core import Mix, Mixer

Bot = commands.Bot(command_prefix = '!')

@Bot.event
async def on_ready():
    print ("pahan upal v yamu")

mix = Mixer()

@Bot.event
async def on_message(message):
    if not message.author.bot:
        if message.content == "!create mix":
            mix.create_mix()
        elif message.content == "!add mix" or message.content == "++":
            mix.add_member(message.author.name)
        elif message.content == "!who":
            await message.channel.send(mix.get_members())

Bot.run("NTkxMjI2OTY3ODYxMzYyNzA3.XQttEA.8vUXFr3H2SDeV3ptDPngXTqPK7Q")




'''
@Bot.command(pass_context = True)
async def pidor(ctx):
    print(ctx)
    await ctx.send('pahan')

@Bot.command(pass_context = True)
async def pahan(ctx):
    await ctx.send("конечно же пидор!")

'''