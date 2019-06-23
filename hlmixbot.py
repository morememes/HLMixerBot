import discord
from discord.ext import commands
from discord.ext.commands import Bot

from libs.core import Mix, Mixer



Bot = commands.Bot(command_prefix = '!')
mixchannel = None


@Bot.event
async def on_ready():
    global mix
    print ("pahan upal v yamu")
    channels = Bot.get_all_channels()
    for channel in channels:
        if channel.name == 'микс':
            mixchannel = channel
            break
    mix = Mixer(mixchannel=mixchannel)



@Bot.event
async def on_message(message):
    global mix
    if not message.author.bot:
        if message.content == "!create mix":
            mix.create_mix()
        elif message.content == "!add mix" or message.content == "++":
            await mix.add_member(message)
        elif message.content == "!rep me" or message.content == "--":
            await mix.remove_member(message)
        elif message.content == "!who":
            await message.channel.send(mix.get_members())
        elif message.content.startswith('!pick'):
            a = message.content.split()
            print(message.author.id)
            print(a)
            await mix.pick_player(message) 

Bot.run("token")




'''
@Bot.command(pass_context = True)
async def pidor(ctx):
    print(ctx)
    await ctx.send('pahan')

@Bot.command(pass_context = True)
async def pahan(ctx):
    await ctx.send("конечно же пидор!")

'''