from typing import Any
from discord.flags import Intents
# from dotenv import load_dotenv
# load_dotenv()
import os
import discord
import json
from pathlib import Path

DISCORD_SERVER_ID = int(os.getenv('DISCORD_SERVER_ID'))
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
BOT_TOKEN         = os.getenv('BOT_TOKEN')

tmp_data_path = Path('data')
tmp_data_path.mkdir(parents=True, exist_ok=True)

class FAQCreatorBotClient(discord.Client):
    
    def __init__(self, *, intents: Intents, channel_filter_list : list[int] , **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self.channel_filter_list = channel_filter_list
    
    text_selected_channels = []
    async def on_ready(self):
        print('Logged on as', self.user)
        text_channels = await self.find_text_channels()
        print(text_channels)
        messages = await self.fetch_messages()
        print(messages)
        await self.close()
        print('process complete')


    async def find_text_channels(self):
        await self.wait_until_ready()
        text_channels = []
        
        for c in self.get_all_channels():
            if type(c) == discord.TextChannel:
                text_channels.append(c)
                
        
        channels = [c for c in text_channels if c.guild.id == DISCORD_SERVER_ID and c.id in self.channel_filter_list]
        self.text_selected_channels = channels

    async def fetch_messages(self):

        print('fetch_messages()')
        all_messages = []
        
        for c in self.text_selected_channels:
            print(f'{c.name} the current channel')
            try:
                #TODO uncomment for PROD
                # messages = [message async for message in c.history(limit = 100_000)] 
                messages = [message async for message in c.history(limit = 300)]
            except:
                print(f'error with channel : {c.name}')
                messages = []
            
            print(f'Founded {len(messages)} Messages in the current channel')
            all_messages.extend([{ 
                    'id'           : m.id ,
                    'author_id'    : m.author.id ,
                    'content'      : m.content ,
                    'reference_id' : m.reference.message_id if m.reference else None ,
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
                    'channel_id'        : m.channel.id ,
                    'channel_name'      : m.channel.name ,
                    'channel_parent_id' : m.channel.parent_id ,
                    } 
                   for m in messages])
                


        with open(tmp_data_path / f'{DISCORD_SERVER_ID}_selected_channels_messages.json', 'w') as f:
            json.dump(all_messages, f)
        return all_messages

def run_client(channel_filter_list : list[int] = []):
    
    if not ( tmp_data_path / f'{DISCORD_SERVER_ID}_selected_channels_messages.json').exists():    
        intents = discord.Intents.default()
        intents.message_content = True
        client = FAQCreatorBotClient(intents=intents, channel_filter_list = channel_filter_list)
        dc = client.run(
            BOT_TOKEN
        )
    else:
        print(f'Messages for DISCORD SERVER {DISCORD_SERVER_ID} are already fetched! (hint: disable this button)')

#* Call this function in order to get all messages from a specific Channel
#* Parameters:
#*  - channel_filter_list : Channel ID 

run_client(channel_filter_list = [
    DISCORD_CHANNEL_ID
    ])