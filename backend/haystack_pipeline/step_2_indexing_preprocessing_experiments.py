#!pip install discord.py farm-haystack[faiss] python-dotenv farm-haystack[inference] farm-haystack[preprocessing]
#!python step_2_indexing_preprocessing_experiments.py
from doc_functions import *
import os
if os.getenv('run_locally') != '1':
    from dotenv import load_dotenv
    load_dotenv()
from haystack.pipelines import Pipeline
from haystack.nodes import PreProcessor
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever
import logging
import json
from haystack.nodes import  JsonConverter
# import pdb ##### REMOVE IN FINAL SCRIPT

#* Refactor Discord Messages JSON file
DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')
data_path = 'data/'
assets_path = 'solarathon/assets/'
if os.getenv('run_locally') == '1':
    data_path = f'../../{data_path}'
    assets_path = f'../../{assets_path}'


DISCORD_MESSAGES_PATH_JSON = f'{data_path}{DISCORD_SERVER_ID}_selected_channels_messages.json'
DISCORD_MESSAGES_PATH_JSON_FORMATTED = f'{data_path}filtered_{DISCORD_SERVER_ID}_selected_channels_messages.json'
FULL_FAQS_PATH = f'{data_path}full_faq.json'
FAQS_PATH_JSON_FORMATTED = f'{assets_path}full_fe_faqs.json'

with open(FULL_FAQS_PATH, 'r') as f:
    data = json.loads(f.read())

faqs = [
    {  
     'id' : id, 
     'content' : f"""
                    Question : 
                    {faq['question']} ;
                    Answer :
                    {faq['answer']}
                  """,
     'content_type' : 'text',
     'integrations' : faq['integrations'] if faq['integrations'] else [], 
     'topic' : faq['topic'] if faq['topic'] else '' , 
     'category' : faq['category'] if faq['category'] else ''
     } for id, faq in enumerate(data)
]
with open(FAQS_PATH_JSON_FORMATTED, 'w') as f:
    json.dump(faqs, f)
    
#* Indexing Pipeline

embedding_model = 'sentence-transformers/all-mpnet-base-v2' # https://huggingface.co/sentence-transformers/all-mpnet-base-v2

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
haystack_logger = logging.getLogger("haystack")

# Create a logging handler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Add the console handler to the logger
haystack_logger.addHandler(console_handler)

split_by_list = ['word', 'sentence']
split_length_dict = {
        'word': [20, 40, 60, 200],
        'sentence': [1, 2, 3]
        }

# # Get every combination of split_by_list and split_length_list:
split_by_combinations = [('word', split_length) for split_length in split_length_dict['word']] + \
    [('sentence', split_length) for split_length in split_length_dict['sentence']]
# split_by_combinations = [('sentence', split_length) for split_length in split_length_dict['sentence']]
# split_by_combinations = [('word', split_length) for split_length in split_length_dict['word']] 

for split_by, split_length in split_by_combinations:
    split_description = f'split_by_{split_length}_{split_by}'
    print(f'\n\n**{split_description}**')
    index_filename = f'{DISCORD_SERVER_ID}_index_{split_description}.faiss'
    config_filename = f'{DISCORD_SERVER_ID}_config_{split_description}.json'
    faiss_filename = f'faiss_document_store_{split_description}.db'

    delete_documents(index_filename, assets_path)
    delete_documents(config_filename, assets_path)
    delete_documents(faiss_filename, assets_path)

    document_store = FAISSDocumentStore( # https://docs.haystack.deepset.ai/reference/document-store-api#faissdocumentstore
        sql_url=f"sqlite:///{assets_path}{faiss_filename}",
        faiss_index_factory_str="Flat",
        similarity = 'cosine'
        )
    print(f'FAISSDocumentStore instantiated.')
    preprocessor = PreProcessor( # https://docs.haystack.deepset.ai/docs/preprocessor
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        remove_substrings=None,
        # split_by=None, # Unit for splitting the document. Can be "word", "sentence", or "passage". Set to None to disable splitting.
        split_by=split_by, # Unit for splitting the document. Can be "word", "sentence", or "passage". Set to None to disable splitting.
        split_length=split_length,
        split_respect_sentence_boundary=True if split_by == 'word' else False,
        split_overlap=0,
        max_chars_check = 10000
    )
    print(f'PreProcessor instantiated.')

    retriever = EmbeddingRetriever( # https://docs.haystack.deepset.ai/reference/retriever-api#embeddingretriever
        document_store=None,
        embedding_model=embedding_model,
        model_format="sentence_transformers",
        top_k = 100
    )
    print(f'Retriever instantiated.')

    file_converter = JsonConverter() # https://docs.haystack.deepset.ai/docs/file_converters
    indexing_pipeline = Pipeline()
    indexing_pipeline.add_node(component=file_converter, name="FileConverter", inputs=["File"])
    indexing_pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["FileConverter"])
    indexing_pipeline.add_node(component=retriever, name="Retriever", inputs=["PreProcessor"])
    indexing_pipeline.add_node(component=document_store, name="DocumentStore", inputs=["Retriever"])
    print('Pipeline created.')
    indexing_pipeline.run(file_paths=[FAQS_PATH_JSON_FORMATTED])
    print(f'Pipeline ran.')
    document_store.update_embeddings(retriever)
    print(f'Embeddings updated.')
    document_store.save(
        index_path  = f'{assets_path}{index_filename}', 
        config_path = f'{assets_path}{config_filename}'
        )
    print(f'Number of documents: {document_store.get_document_count()}')
    print(f'Document store saved.')
    # ##### REMOVE IN FINAL SCRIPT
    # pdb.set_trace() 