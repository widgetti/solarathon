import os
import json
from pathlib import Path

DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')

with open(f'data/{DISCORD_SERVER_ID}_selected_channels_messages.json', 'r') as f:
    raw = json.loads(f.read())

prod_data_path = Path('solarathon/assets/data')
prod_data_path.mkdir(parents=True, exist_ok=True)

with open(prod_data_path / f'haystack.json', 'w') as f:
    json.dump(raw[:100], f)