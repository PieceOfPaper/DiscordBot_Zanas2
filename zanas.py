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


shout_keyworks = ['자나스']
shout_keyworks.append('전설')
shout_keyworks.append('바이보라')
shout_keyworks.append('길드')

# 거래 관련
shout_keyworks.append('석')
shout_keyworks.append('팜')
shout_keyworks.append('삼')
shout_keyworks.append('ㅍ')
shout_keyworks.append('ㅅ')
shout_keyworks.append('실버')
shout_keyworks.append('개당')
shout_keyworks.append('파라')
shout_keyworks.append('팔아')
shout_keyworks.append('팝니')
shout_keyworks.append('파시')
shout_keyworks.append('사요')
shout_keyworks.append('사영')
shout_keyworks.append('사용')
shout_keyworks.append('사욤')
shout_keyworks.append('삽니')
shout_keyworks.append('사봅')
shout_keyworks.append('사봄')
shout_keyworks.append('사시')
shout_keyworks.append('교환')

class GuildData:
    id = 0
    tzinfo = None

    channel_id = 0
    channel_id_guild = 0 #길드컨텐츠용

    def __init__(self, id):
        self.id = id
        self.tzinfo = datetime.timezone(datetime.timedelta(hours=0))

class ZanasClient(discord.Client):

    guildDatas = dict()
    colonyGuilds = dict()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.colonyGuilds['게나르 평원'] = None
        self.colonyGuilds['수로교'] = None
        self.colonyGuilds['아렐르노 남작령'] = None

        self.colonyGuilds['누오로딘 폭포'] = None
        self.colonyGuilds['스벤티마스 유형지'] = None
        self.colonyGuilds['살비야스 숲'] = None

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
                    if len(args) > 1:
                        if args[1] == '채널':
                            self.guildDatas[message.guild.id].channel_id = message.channel.id
                            print(f'guild:{message.guild.id} channel:{message.channel.id}')
                            await message.channel.send(f'<#{message.channel.id}> 채널에 알림 등록.')
                        elif args[1] == '채널길드':
                            self.guildDatas[message.guild.id].channel_id_guild = message.channel.id
                            print(f'guild:{message.guild.id} channel:{message.channel.id}')
                            await message.channel.send(f'<#{message.channel.id}> 채널에 길드 알림 등록.')
                elif args[0] == './채팅시스템':
                    await self.check_systemchat(message.content.replace('./채팅시스템 ',''))
                elif args[0] == './채팅외침':
                    await self.check_shoutchat(message.content.replace('./채팅외침 ',''))

    async def check_systemchat(self, text):
        # print(text)
        result = None
        resulttype = 0
        if 'FieldBossWillAppear' in text:
            resulttype = 1
            bossname = text.replace('System:!@#$FieldBossWillAppear$*$Name$*$','').replace('#@!','')
            result = f':imp: 잠시 후 필드보스가 등장합니다. {bossname.strip()}'
        elif 'NOTICE_READY_FIELDBOSS_WORLD_EVENT' in text:
            resulttype = 1
            result = f':smiling_imp: 월드 보스가 구원자들에 의해 쓰러졌습니다.'
        elif 'NOTICE_START_FIELDBOSS_WORLD_EVENT' in text:
            # resulttype = 1
            # result = f'여신의 가호 이벤트가 시작되었습니다!'
            resulttype = 0
        elif 'FIELDBOSS_WORLD_EVENT_WIN_MSG' in text:
            resulttype = 0
        elif 'ContentRatingMsg' in text:
            resulttype = 0
        elif 'DelibarationMsg1' in text:
            resulttype = 0
        elif 'DelibarationMsg2' in text:
            resulttype = 0
        elif 'SOLO_RAID_NEW_RECORD' in text:
            resulttype = 0
        elif 'Guild_Event_boruta_Awards_WorldMessage_1' in text:
            resulttype = 0
        elif 'Guild_Event_boruta_Awards_WorldMessage_2' in text:
            resulttype = 0
        elif 'Guild_Event_boruta_Awards_WorldMessage_3' in text:
            resulttype = 0
        elif 'Guild_Event_boruta_Awards_WorldMessage_4' in text:
            resulttype = 0
        elif 'NOTICE_END_FIELDBOSS_WORLD_EVENT' in text:
            resulttype = 0
        elif 'Guild_Colony_Live_End_WorldMessage_1' in text:
            resulttype = 0
        elif 'Guild_Colony_Live_End_WorldMessage_2' in text:
            resulttype = 0
        elif 'Guild_Colony_End_WorldMessage_' in text:
            resulttype = 0
        elif 'pvp_mine_before_' in text:
            resulttype = 0
        elif 'pvp_mine_2nd_before_' in text:
            resulttype = 0
        elif 'Guild_Event_boruta_Awards_WorldMessage_Rank_' in text:
            resulttype = 2
            ranking = text.replace('System:!@#$Guild_Event_boruta_Awards_WorldMessage_Rank_','').split('$*$partyName$*$')[0]
            guildnametime = text.replace(f'System:!@#$Guild_Event_boruta_Awards_WorldMessage_Rank_{ranking}$*$partyName$*$','').replace('$*$TimeRankMin$*$','/').replace('$*$TimeRankSec$*$','/').replace('#@!','')
            guildtime_splited = guildnametime.split('/')
            result = f':trophy: 보루타 {ranking}위: {guildtime_splited[0].strip()} ({guildtime_splited[1].strip()}분 {guildtime_splited[2].strip()}초)'
        elif 'Guild_Colony_Occupation_WorldMessage' in text:
            resulttype = 2
            guildnamemap = text.replace('System:!@#$Guild_Colony_Occupation_WorldMessage$*$partyName$*$','').replace('#@!','').split('$*$mapName$*$')
            result = f':triangular_flag_on_post: [{guildnamemap[0].strip()}] 길드가 [{guildnamemap[1].strip()}] 점령에 성공했습니다.\n'
            self.colonyGuilds[guildnamemap[1].replace(' 지역','').strip()] = guildnamemap[0].strip()
            result += '```'
            for colonyKey in self.colonyGuilds:
                result += f'{colonyKey} : {self.colonyGuilds[colonyKey]}\n'
            result += '```'
        elif 'CantConnectChatServer' in text:
            resulttype = 0
            print('클라이언트 재시작 필요.')
        elif text.startswith('System:'):
            resulttype = 0
            result = text
            print(text)
                        
        if resulttype == 1:
            for guildKey in self.guildDatas:
                if self.guildDatas[guildKey].channel_id > 0:
                    await client.get_channel(self.guildDatas[guildKey].channel_id).send(result)
        elif resulttype == 2:
            for guildKey in self.guildDatas:
                if self.guildDatas[guildKey].channel_id_guild > 0:
                    await client.get_channel(self.guildDatas[guildKey].channel_id_guild).send(result)

    async def check_shoutchat(self, text):
        # print(text)
        nickname = text.split(':')[0]
        mention = text.replace(f'{nickname}:','')
        result = None
        resulttype = 0
        for keyword in shout_keyworks:
            if keyword in mention:
                result = f':loudspeaker: **{nickname}** : `{mention}`'
                resulttype = 1
            if result is not None:
                break

        if resulttype == 1:
            for guildKey in self.guildDatas:
                if self.guildDatas[guildKey].channel_id > 0:
                    await client.get_channel(self.guildDatas[guildKey].channel_id).send(result)
        elif resulttype == 2:
            for guildKey in self.guildDatas:
                if self.guildDatas[guildKey].channel_id_guild > 0:
                    await client.get_channel(self.guildDatas[guildKey].channel_id_guild).send(result)


            
    async def my_background_task(self):
        await self.wait_until_ready()
        path = 'C:\\Nexon\\TreeOfSavior\\release\\screenshot\\'
        while not self.is_closed():

            isError = False

            # rename
            filelist = os.listdir(path)
            for filename in filelist:
                if filename.startswith('recchat_'):
                    try:
                        os.rename(path + filename, path + 'check_' + filename)
                    except Exception as e:
                        print(f'rename error - {e}')
                        isError = True
                        break
            await asyncio.sleep(2)

            if isError:
                continue

            # readchat
            filelist = os.listdir(path)
            for filename in filelist:
                if filename.startswith('check_recchat_'):
                    f = open(path + filename, 'r', encoding='UTF8')
                    lines = f.readlines()
                    f.close()
                    try:
                        os.remove(path + filename)
                    except Exception as e:
                        print(f'remove error - {e}')

                    for line in lines:
                        splited = line.split(' ')
                        # print(line[:-1])
                        if len(splited) < 3:
                            continue
                        splited2 = line.split(splited[2])
                        if len(splited2) < 2:
                            continue
                        text = splited2[1][:-1]

                        if 'System' in splited[2]:
                            await self.check_systemchat(text)
                        elif 'Shout' in splited[2]:
                            await self.check_shoutchat(text)

            await asyncio.sleep(2)


client = ZanasClient()
client.run(token)