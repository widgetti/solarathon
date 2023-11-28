from dotenv import load_dotenv
load_dotenv()
import os
import discord
import json

DISCORD_SERVER_ID = int(os.getenv('DISCORD_SERVER_ID'))
BOT_TOKEN         = os.getenv('BOT_TOKEN')

class FAQCreatorBotClient(discord.Client):
    text_guild_channels = []
    async def on_ready(self):
        print('Logged on as', self.user)
        servers = await self.find_servers()
        print(servers)
        text_channels = await self.find_text_channels()
        print(text_channels)
        await self.close()

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
            "name"         : c.name ,
            "id"           : c.id ,
            "category_id"  : c.category.id if c.category else None,
            "category_name": c.category.name if c.category else None,
            "position"     : c.position ,
            "guild_id"     : c.guild.id ,
            "guild_name"   : c.guild.name ,
            "guild_owner"  : c.guild.owner                       
        } for c in text_channels if c.guild.id == DISCORD_SERVER_ID]

        with open(f'data/private/{DISCORD_SERVER_ID}_channels.json', 'w') as f:
            json.dump(channels, f)
        return channels


intents = discord.Intents.default()
intents.message_content = True
client = FAQCreatorBotClient(intents=intents)

def run_client():
    dc = client.run(
        BOT_TOKEN
    )
    
# run_client()