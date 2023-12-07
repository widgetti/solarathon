
#%% []
import pandas as pd
from doc_functions import *
import os
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever
#%% []

################
#* THIS SCRIPT IS JUST A REFERENCE, WE COULD USE THE RETRIEVER FOR SEARCH FEATURE IN THE SOLARA FRONTEND
################

DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')
data_path = 'data/'
assets_path = 'solarathon/assets/'
if True:
    data_path = f'../../{data_path}'
    assets_path = f'../../{assets_path}'

DISCORD_MESSAGES_PATH_JSON = f'{data_path}{DISCORD_SERVER_ID}_selected_channels_messages.json'
DISCORD_MESSAGES_PATH_JSON_FORMATTED = f'{data_path}filtered_{DISCORD_SERVER_ID}_selected_channels_messages.json'
FULL_FAQS_PATH = f'{assets_path}full_faq.json'
FAQS_PATH_JSON_FORMATTED = f'{assets_path}full_fe_faqs.json'

#%% []
df = pd.read_json(FULL_FAQS_PATH).astype({'id':'float32'})
df.info()
#%% []
# embedding_model = 'sentence-transformers/all-mpnet-base-v2' # https://huggingface.co/sentence-transformers/all-mpnet-base-v2
embedding_model = 'sentence-transformers/all-MiniLM-L6-v2' # https://huggingface.co/sentence-transformers/all-mpnet-base-v2
llm = 'gpt-3.5-turbo-16k'

index_filename = f'{DISCORD_SERVER_ID}_index.faiss'
config_filename = f'{DISCORD_SERVER_ID}_config.json'
faiss_filename = 'faiss_document_store.db'
#%% []
document_store = FAISSDocumentStore( # https://docs.haystack.deepset.ai/reference/document-store-api#faissdocumentstore
    sql_url=f"sqlite:///{assets_path}{faiss_filename}",
    faiss_index_factory_str="Flat",
    similarity='cosine',
    embedding_dim=384
    )

retriever = EmbeddingRetriever( # https://docs.haystack.deepset.ai/reference/retriever-api
    document_store=document_store,
    embedding_model=embedding_model,
    model_format="sentence_transformers",
    top_k = 10,
    scale_score=False
)

#%% []
# Get dataframe with columns "question", "answer" and some custom metadata
# Minimal cleaning
df["question"] = df["question"].apply(lambda x: x.strip())
print(df.head())
import numpy as np
# Create embeddings for our questions from the FAQs
# In contrast to most other search use cases, we don't create the embeddings here from the content of our documents,
# but rather from the additional text field "question" as we want to match "incoming question" <-> "stored question".
questions = list(df["question"].values)
df["embedding"] =retriever.embed_queries(queries=questions).astype('float32').tolist()
# df["embedding"] = [np.expand_dims(np.float32(a), axis=0) for a in retriever.embed_queries(queries=questions).astype('float32').tolist()]
df = df.rename(columns={"question": "content"})

# Convert Dataframe to list of dicts and index them in our DocumentStore
docs_to_index = df.to_dict(orient="records")
document_store.write_documents(docs_to_index)
#%% []
from haystack.pipelines import Pipeline
from haystack.nodes import Docs2Answers

################
# MODIFY THIS FOR UI
user_search_term = 'Solara supports fastapi?' #### MAKE THIS A UI INPUT
################


pipeline = Pipeline()

pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
pipeline.add_node(component=Docs2Answers(), name="Docs2Answers", inputs=["Retriever"])
result = pipeline.run(query=user_search_term, params={"Retriever": {"top_k": 5}})

print(result)

# %%
