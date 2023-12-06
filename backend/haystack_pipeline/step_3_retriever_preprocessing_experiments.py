#!python step_3_retriever_preprocessing_experiments.py
from doc_functions import *
import os
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever
# import pdb ##### REMOVE IN FINAL SCRIPT

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

split_by_list = ['word', 'sentence']
split_length_dict = {
        'word': [20, 40, 60, 200],
        'sentence': [1, 2, 3, 4]
        }

# Get every combination of split_by_list and split_length_list:
split_by_combinations = [('word', split_length) for split_length in split_length_dict['word']] + \
    [('sentence', split_length) for split_length in split_length_dict['sentence']]

results_dict = {}

for split_by, split_length in split_by_combinations:
    split_description = f'split_by_{split_length}_{split_by}'
    index_filename = f'{DISCORD_SERVER_ID}_index_{split_description}.faiss'
    config_filename = f'{DISCORD_SERVER_ID}_config_{split_description}.json'
    faiss_filename = f'faiss_document_store_{split_description}.db'

    print(f'{index_filename}, {config_filename}, {faiss_filename}')
    # ##### REMOVE IN FINAL SCRIPT
    # pdb.set_trace() 
    try:
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
        user_search_term = 'Jupyter notebook' #### MAKE THIS A UI INPUT
        ################


        show_score = True #### Whether or not to show the confidence score of the model that retrieved the results. 
            # https://docs.haystack.deepset.ai/docs/documents_answers_labels#document
            # When testing with a few different `user_search_term` values, the score was always around 0.50 with a range of < 0.001, 
            # even when top_k = 10. 
            # Tested search terms: ['Solara', 'orange juice', 'Silvia', 'dfaadfadfadfadfadfadfdaf']
        retrieved_docs = retriever.run_query(user_search_term)
        results_dict[split_description] = list_retriever_results(retrieved_docs, show_score=show_score) ### THIS WILL BE DISPLAYED IN THE FRONTEND
    except Exception as error:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        message = f'{index_filename} and/or {config_filename}: {error} [{lineno} in {filename}].'
        print(message)
    # ##### REMOVE IN FINAL SCRIPT
    # pdb.set_trace() 


