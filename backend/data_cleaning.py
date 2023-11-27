import json
from datetime import datetime
import os
def load_json(filename, filepath):
    """
    Load a JSON file using specified file path.
    Back slashes in file path will be converted to forward slashes.

    Arguments:
    - filepath (raw string): Use the format r'<path>'.
    - filename (string).
    """
    filename = f'{filepath}/'.replace('\\','/')+filename
    with open(filename) as file:
        return json.load(file)
    
def filter_messages(messages):
    filtered_messages = []
    print(f'Filtering {len(messages)} messages...')
    for message in messages:
        filtered_message = {
            'id': message['id'],
            'author_id': message['author_id'],
            'content': message['content'],
            'reference_id': message['reference_id']
        }
        filtered_messages.append(filtered_message)
    print(f'Message attributes: {filtered_messages[0].keys()}')
    return filtered_messages

def save_to_json(obj, filename=None, description='Discord_all_messages_cleaned', append_version=False,
    path='../data'
    ):
    """
    Save Python object as a JSON file.
    Parameters:
    - obj: Python object to be saved.
    - filename: Root of the filename.
    - path (raw string): Use the format r'<path>'. If None, file is saved in same directory as script.
    - append_version (bool): If true, append date and time to end of filename.
    """
    if description:
        filename = f'{description}_{datetime.now().strftime("%Y-%m-%d_%H%M")}'
        append_version = False
    elif filename == None:
        filename = f'{datetime.now().strftime("%Y-%m-%d_%H%M")}_outputs'
        append_version = False
    if path:
        path = f'{path}/'.replace('\\','/')
    if append_version:
        filename += f'_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}'
    filename += '.json'
    with open(path+filename, 'w') as f:
        json.dump(obj, f)
    print(f'Object saved as JSON: {filename}')

def load_json(filename, filepath):
    """
    Load a JSON file using specified file path copied from windows file explorer.
    Back slashes in file path will be converted to forward slashes.

    Arguments:
    - filepath (raw string): Use the format r'<path>'.
    - filename (string).
    """
    filename = f'{filepath}/'.replace('\\','/')+filename
    with open(filename) as file:
        return json.load(file)

DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')

filepath = '../data' #### Update if needed
filename_raw = f'{DISCORD_SERVER_ID}_selected_channels_messages.json' #### Update if needed
filename_cleaned = 'Discord_all_messages_cleaned'
messages = load_json(filename_raw, filepath)
filtered_messages = filter_messages(messages)
save_to_json(filtered_messages, filename=filename_cleaned, path=filepath)