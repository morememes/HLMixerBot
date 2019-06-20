#import discord
#from discord.ext import commands
#from discord.ext.commands import Bot

class Mix():
    def __init__(self):
        self.members = []
        self.count_members = None
        self.max_members = 18

    def add_member(self, nick):
        self.members.append(nick)

    def remove_member(self, nick):
        pass

    def get_members(self):
        st = 'Mix({0}/{1}) '.format(len(self.members), self.max_members)
        for member in self.members:
            st += '`' + member + '`/'
        return st[:-1]

class Mixer():
    def __init__(self):
        self.mix = None

    def create_mix(self):
        self.mix = Mix()

    def add_member(self, nick):
        self.mix.add_member(nick)

    def remove_member(self, nick):
        pass

    def get_members(self):
        return self.mix.get_members()



def switch(message):
    mix = None
    if message.content == "!create mix":
        mix = Mix()
    elif message.content == "!add mix":
        mix.add_member(message.author.name)
    elif message.content == "!who":
        message.channel.send(mix.get_members())
