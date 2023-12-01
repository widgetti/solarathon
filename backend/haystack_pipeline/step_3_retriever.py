from file_functions import *
import os
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever

################
#* THIS SCRIPT IS JUST A REFERENCE, WE COULD USE THE RETRIEVER FOR SEARCH FEATURE IN THE SOLARA FRONTEND
################

DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')
data_path = 'data/'
assets_path = 'solarathon/assets'
if os.getenv('run_locally') == '1':
    data_path = f'../../{data_path}'
    assets_path = f'../../{assets_path}'

DISCORD_MESSAGES_PATH_JSON = f'{data_path}{DISCORD_SERVER_ID}_selected_channels_messages.json'
DISCORD_MESSAGES_PATH_JSON_FORMATTED = f'{data_path}filtered_{DISCORD_SERVER_ID}_selected_channels_messages.json'
FULL_FAQS_PATH = f'{data_path}full_faq.json'
FAQS_PATH_JSON_FORMATTED = f'{data_path}full_faq_formatted.json'

embedding_model = 'sentence-transformers/all-mpnet-base-v2' # https://huggingface.co/sentence-transformers/all-mpnet-base-v2
llm = 'gpt-3.5-turbo-16k'

index_filename = f'{DISCORD_SERVER_ID}_index.faiss'
config_filename = f'{DISCORD_SERVER_ID}_config.json'
faiss_filename = 'faiss_document_store.db'

document_store = FAISSDocumentStore.load( 
    index_path  = f'{assets_path}/{index_filename}', 
    config_path = f'{assets_path}/{config_filename}'
    )

retriever = EmbeddingRetriever( # https://docs.haystack.deepset.ai/reference/retriever-api
    document_store=document_store,
    embedding_model=embedding_model,
    model_format="sentence_transformers",
    top_k = 5
)
################
# MODIFY THIS FOR UI
################
user_search_term = 'Jupyter notebook' #### MAKE THIS A UI INPUT
retrieved_docs = retriever.run_query(user_search_term)
results = list_retriever_results(retrieved_docs) ### THIS WILL BE DISPLAYED IN THE FRONTEND


