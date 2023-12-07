from collections import Counter
import os
from pathlib import Path
import solara
import json

data_path = Path(__file__).parent.parent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_SERVER_ID = os.getenv("DISCORD_SERVER_ID")
FULL_FAQS_PATH = f'{data_path}/assets/full_faq.json'
ASSETS_PATH = f'{data_path}/assets/'
FULL_FAQS_PATH = f'{data_path}/assets/full_faq.json'

index_filename = f'{DISCORD_SERVER_ID}_index.faiss'
config_filename = f'{DISCORD_SERVER_ID}_config.json'
faiss_filename = 'faiss_document_store.db'

def import_raw_data():
    data       = json.loads(open(FULL_FAQS_PATH).read())
    categories = Counter([f['category'] for f in data])
    topics     = set([f['topic'] for f in data])
    return data,categories,topics