

from dotenv import load_dotenv
load_dotenv()

import os
import json
import pandas as pd

DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')

def json_raw_to_df( path : str = f'data/private/{DISCORD_SERVER_ID}_selected_channels_messages.json'):
    with open(path, 'r') as f:
        raw = json.loads(f.read())

    #* FETCH SERVER MESSAGES
    data = pd.DataFrame(raw).astype({
        'channel_id' : 'Int64',
        'author_id' : 'Int64',
        'reference_id' : 'Int64',
        'channel_parent_id' : 'Int64',
    })
    return data