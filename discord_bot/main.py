from dotenv import load_dotenv
load_dotenv()
import os
import discord
import json

DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')

class FAQCreatorBotClient(discord.Client):
    text_guild_channels = []
    async def on_ready(self):
        print('Logged on as', self.user)
        servers = await self.find_servers()
        print(servers)
        text_channels = await self.find_text_channels()
        print(text_channels)
        messages = await self.fetch_messages()
        print(messages)

    async def find_servers(self):
        await self.wait_until_ready()
        servers = []
        async for guild in client.fetch_guilds(limit=150):
            servers.append(guild)
        
        servers = [{
            "name": s.name,
            "id": s.id                      
        } for s in servers]
        
        with open(f'servers.json', 'w') as f:
            json.dump(servers, f)
        return servers

    async def find_text_channels(self):
        await self.wait_until_ready()
        text_channels = []
        
        for c in self.get_all_channels():
            if type(c) == discord.TextChannel:
                text_channels.append(c)
                
        self.text_guild_channels = text_channels
        channels = [{
            "name": c.name,
            "id": c.id,
            "category_id": c.category.id,
            "category_name": c.category.name,
            "position": c.position ,
            "guild_id": c.guild.id , 
            "guild_name": c.guild.name , 
            "guild_owner": c.guild.owner                       
        } for c in text_channels if c.guild.id == DISCORD_SERVER_ID]

        with open(f'{DISCORD_SERVER_ID}_channels.json', 'w') as f:
            json.dump(channels, f)
        return channels

    async def fetch_messages(self):

        print('fetch_messages()')
        all_messages = []
        
        for c in self.text_guild_channels:
            print(f'{c.name} the current channel')
            try:
                messages = [message async for message in c.history()]
            except:
                print(f'error with channel : {c.name}')
                messages = []
            print(f'Founded {len(messages)} Messages in the current channel')
            all_messages.extend([{ 
                    'id'           : m.id ,
                    'author_id'    : m.author.id ,
                    'content'      : m.content ,
                    'reference_id' : m.reference .message_id if m.reference else None ,
                    'created_at'   : m.created_at.strftime("%m/%d/%YT%H:%M:%S") ,
                    'channel_id'   : m.channel.id ,
                    'channel_name' : m.channel.name ,
                    }                   
                   for m in messages])
            
            print(f'Founded {len(c.threads)} Threads in the current channel')
            threads = [t for t in c.threads]
            for t in threads:
                print( '-> Thread Name : ' , t, ' | Thread id :' , t.id, ' | Parent id :' , t.parent_id, )
                messages = [message async for message in t.history()]
                all_messages.extend([{ 
                    'id'                : m.id ,
                    'author_id'         : m.author.id ,
                    'content'           : m.content ,
                    'reference_id'      : m.reference .message_id if m.reference else None ,
                    'created_at'        : m.created_at.strftime("%m/%d/%YT%H:%M:%S") ,
                    'channel_id'        : m.channelid ,
                    'channel_name'      : m.channel.name ,
                    'channel_parent_id' : m.channel.parent_id ,
                    } 
                   for m in messages])

        with open(f'{DISCORD_SERVER_ID}_all_messages.json', 'w') as f:
            json.dump(all_messages, f)
        return all_messages

#* FETCH SERVER MESSAGES
intents = discord.Intents.default()
intents.message_content = True
client = FAQCreatorBotClient(intents=intents)
dc = client.run(
    os.getenv('BOT_TOKEN')
)