#import discord
#from discord.ext import commands
#from discord.ext.commands import Bot

async def send_msg(channel, msg):
    await channel.send(msg)

class Mix():
    def __init__(self, mixName = None, max_members = 2, mixchannel = None):
        self.mixName = mixName
        self.members = []
        self.members_id = []
        self.count_members = None
        self.max_members = max_members
        self.ready = False
        self.mixchannel = mixchannel

        self.timestartmsg = 'Начало в 20 мск / 19 cest!'

        self.blue = []
        self.read = []
        

    async def add_member(self, message):
        if not self.ready:
            if not message.author.id in self.members_id:
                self.members.append(message.author)
                self.members_id.append(message.author.id)
                await message.channel.send('[**Mix** ({0}/{1})]'.format(len(self.members), self.max_members))
                if len(self.members) == self.max_members:
                    await self.mix_ready()
            else:
                await message.channel.send(message.author.mention + ' , ты уже записан!')

    async def remove_member(self, message):
        if not self.ready:
            if message.author.id in self.members_id:
                ind = self.members_id.index(message.author.id)
                self.members_id.pop(ind)
                self.members.pop(ind)
                await message.channel.send('[**Mix** ({0}/{1})]'.format(len(self.members), self.max_members))
            else:
                await message.channel.send(message.author.mention + ' , ты не записывался на микс!')

    def get_members(self):
        st = '[**Mix** ({0}/{1})] '.format(len(self.members), self.max_members)

        for member in self.members:
            st += '`' + member.name + '`/'
        return st[:-1]

    async def mix_ready(self):
        self.ready = True
        st = 'Микс собрался! {0} \n'.format(self.timestartmsg) # timestartmsg
        for member in self.members:
            st += '`' + member.name + '`\n'
            await member.send(self.timestartmsg)

        await self.mixchannel.send(st)
        # отправка сообщений в пм и в канал миксов



class Mixer():
    def __init__(self, mixchannel = None):
        self.mix = None
        self.mixchannel = mixchannel

    def create_mix(self):
        self.mix = Mix(mixchannel = self.mixchannel)

    async def add_member(self, message):
        if self.mix == None:
            self.create_mix()
        await self.mix.add_member(message)

    async def remove_member(self, message):
        await self.mix.remove_member(message)

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
