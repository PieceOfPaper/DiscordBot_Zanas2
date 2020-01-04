import discord
import asyncio
import sys
import datetime
import random
import os

token = 'token'

for argIdx, argVal in enumerate(sys.argv):
    if argVal == '-token':
        token = sys.argv[argIdx + 1]


class GuildData:
    id = 0
    tzinfo = None

    channel_id = 0

    def __init__(self, id):
        self.id = id
        self.tzinfo = datetime.timezone(datetime.timedelta(hours=0))

    


class ZanasClient(discord.Client):

    guildDatas = dict()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_connect(self):
        print(f'on_connect: {self.user.name}({self.user.id})')
    
    async def on_ready(self):
        print(f'on_ready: {self.user.name}({self.user.id})')
        for guild in self.guilds:
            if guild.id not in self.guildDatas:
                self.guildDatas[guild.id] = GuildData(guild.id)
        print(f'guild data count: {len(self.guildDatas)}')


    # async def on_member_join(self, member):
    #     print(f'on_member_join: {member.display_name}({member.id})')

    # async def on_member_remove(self, member):
    #     print(f'on_member_remove: {member.display_name}({member.id})')

    # async def on_member_update(self, before, after):
    #     print(f'on_member_update: {before.display_name}({before.id}) -> {after.display_name}({after.id})')

    # async def on_user_update(self, before, after):
    #     print(f'on_user_update: {before.name}({before.id}) -> {after.name}({after.id})')

    async def on_guild_join(self, guild):
        print(f'on_guild_join: {guild.name}({guild.id})')
        if guild.id not in self.guildDatas:
            self.guildDatas[guild.id] = GuildData(guild.id)

    async def on_guild_remove(self, guild):
        print(f'on_guild_remove: {guild.name}({guild.id})')
        if guild.id in self.guildDatas:
            del self.guildDatas[guild.id]

    # async def on_guild_update(self, guild):
    #     print(f'on_guild_update: {guild.name}({guild.id})')
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        args = message.content.split(' ')
        if len(args) > 0:
            if args[0].startswith('./'):
                if args[0] == './개발자나스':
                    print(f'channel: {message.channel.name}({message.channel.id})')
                    print(f'guild: {message.guild.name}({message.guild.id})')
                    await message.channel.send('print debug.')
                elif args[0] == './채팅자나스':
                    self.guildDatas[message.guild.id].channel_id = message.channel.id
                    await message.channel.send(f'<#{message.channel.id}> 채널에 알림 등록.')
            
    async def my_background_task(self):
        await self.wait_until_ready()
        path = 'C:\\Nexon\\TreeOfSavior\\release\\screenshot\\'
        while not self.is_closed():
            for filename in os.listdir(path):
                if filename.startswith('check_recchat_'):
                    f = open(path + filename, 'r', encoding='UTF8')
                    lines = f.readlines()
                    for line in lines:
                        splited = line.split(' ')
                        text = line.split(splited[2])[1]
                        print(text[:-1])
                        if splited[2] == '[Notice]':
                            for guildKey in self.guildDatas:
                                if self.guildDatas[guildKey].channel_id > 0:
                                    await client.get_channel(self.guildDatas[guildKey].channel_id).send(text[:-1])

                    f.close()
                    os.remove(path + filename)
                elif filename.startswith('recchat_'):
                    os.rename(path + filename, path + 'check_' + filename)
            await asyncio.sleep(1)


client = ZanasClient()
client.run(token)