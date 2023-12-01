import uuid
from typing import Callable, List, Literal, Optional, Union

import solara
from solara.components.input import use_change

from solarathon.doc_functions import *
import os
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever

if os.getenv('run_locally') != '1':
    from dotenv import load_dotenv
    load_dotenv()
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
# ################
# # MODIFY THIS FOR UI
# user_search_term = 'Jupyter notebook' #### MAKE THIS A UI INPUT
# ################


# show_score = False #### Whether or not to show the confidence score of the model that retrieved the results. 
#     # https://docs.haystack.deepset.ai/docs/documents_answers_labels#document
#     # When testing with a few different `user_search_term` values, the score was always around 0.50 with a range of < 0.001, 
#     # even when top_k = 10. 
#     # Tested search terms: ['Solara', 'orange juice', 'Silvia', 'dfaadfadfadfadfadfadfdaf']

# results = list_retriever_results(retrieved_docs, show_score=show_score) ### THIS WILL BE DISPLAYED IN THE FRONTEND
# print(results)

import solara
from solara.components.input import use_change


@solara.component
def SearchRetriever():


    with solara.Column(align='center', style={'background-color':'white', 'width':'620px','height':'60px','align-items':'center'}):
        solara.InputText(label="Type a question . . .")

