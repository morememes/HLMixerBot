#import discord
#from discord.ext import commands
#from discord.ext.commands import Bot

import re
from copy import copy


async def send_msg(channel, msg):
    await channel.send(msg)

class Mix():
    def __init__(self, mixName = None, max_members = 4, mixchannel = None):
        self.mixName = mixName
        self.members = []
        self.members_id = []
        self.count_members = None
        self.max_members = max_members
        self.mixready = False
        self.pickready = False
        self.mixchannel = mixchannel
        self.pick_counter = 0
        self.pick_sequence = "01"

        self.timestartmsg = 'Начало в 20 мск / 19 cest!'

        #self.blue = []
        #self.red = []
        self.teams = [[], []]
        

    async def add_member(self, message):
        if not self.pickready:
            if not message.author.id in self.members_id:
                self.members.append(message.author)
                self.members_id.append(message.author.id)
                await message.channel.send('[**Mix** ({0}/{1})]'.format(len(self.members), self.max_members))
                if len(self.members) == self.max_members:
                    await self.pick_ready()
            else:
                await message.channel.send(message.author.mention + ' , ты уже записан!')

    async def remove_member(self, message):
        if not self.pickready:
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

    async def pick_ready(self):
        self.pickready = True
        self.copy_members = copy(self.members)
        # TODO
        # Переделать систему выборовов капитанов

        self.teams[0].append(self.members.pop(0).name)
        self.teams[1].append(self.members.pop(0).name)
        print(self.members_id)
        await self.print_pick()

        #st = 'Микс собрался! {0} \n'.format(self.timestartmsg) # timestartmsg
        

        """for member in self.members:
            st += '`' + member.name + '`\n'
            await member.send(self.timestartmsg)

        await self.mixchannel.send(st)"""

    async def print_pick(self):
        print(self.teams[0])
        print(self.teams[1])
        blue = "`" + '` + `'.join(self.teams[0]) + "`"
        red = "`" + '` + `'.join(self.teams[1]) + "`"
        unpicked = "Unpicked: \n"
        for member in self.members:
            unpicked += '`' + member.name + '`\n'
        
        st = blue + '\n' + red + '\n' + unpicked

        await self.mixchannel.send(st)

    async def pick_player(self, message):
        # TODO
        # Сделать проверку на pickready == True
        # и mix ready
        if message.author.name == self.teams[ int(self.pick_sequence[self.pick_counter]) ][0]:
            l = message.content.split()
            n_id = re.search('\d+', l[1])
            print(l[1])
            print(n_id)
            if len(l) != 2 or n_id is None or '@' not in l[1]:
                await message.channel.send(message.author.mention + ", этот игрок не участвует")
            else:
                n_id = int(n_id.group(0))
                if n_id in self.members_id:
                    n = self.copy_members[ self.members_id.index( n_id ) ]

                    if n in self.members:
                        ind = self.members.index(n)
                        self.teams[ int(self.pick_sequence[self.pick_counter]) ].append(self.members.pop(ind).name)
                        self.pick_counter += 1
                        await self.print_pick()
                        if self.pick_counter == self.max_members - 3:
                            self.teams[ int(self.pick_sequence[self.pick_counter]) ].append(self.members.pop(0).name)
                            self.pick_counter += 1
                            self.members = copy(self.copy_members)
                            await self.mix_ready()
                    else:
                        await message.channel.send(message.author.mention + ", этот игрок уже в команде")
                else:
                    await message.channel.send(message.author.mention + ", этот игрок не участвует")
        else:
            await message.channel.send(message.author.mention + ", ты не можешь пикать")

    async def mix_ready(self):
        await self.mixchannel.send('Микс собрался! {0} \n'.format(self.timestartmsg)) # timestartmsg



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

    async def pick_player(self, message):
        await self.mix.pick_player(message)



def switch(message):
    mix = None
    if message.content == "!create mix":
        mix = Mix()
    elif message.content == "!add mix":
        mix.add_member(message.author.name)
    elif message.content == "!who":
        message.channel.send(mix.get_members())
