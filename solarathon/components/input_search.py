import uuid
from typing import Callable, List, Literal, Optional, Union

import solara
from solara.components.input import use_change
from solarathon.core.import_data import ASSETS_PATH, index_filename, config_filename

from solarathon.doc_functions import *
import os
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever

embedding_model = 'sentence-transformers/all-mpnet-base-v2' # https://huggingface.co/sentence-transformers/all-mpnet-base-v2
llm = 'gpt-3.5-turbo-16k'

document_store = FAISSDocumentStore.load( 
    index_path  = f'{ASSETS_PATH}/{index_filename}', 
    config_path = f'{ASSETS_PATH}/{config_filename}'
    )

retriever = EmbeddingRetriever( # https://docs.haystack.deepset.ai/reference/retriever-api
    document_store=document_store,
    embedding_model=embedding_model,
    model_format="sentence_transformers",
    top_k = 5
)

@solara.component
def RetrieverInputBar(filter = None , set_filter = None, placeholder = False):
        with solara.Row(justify='center', style={'background-color':'rgb(28,43,51)', 'height':'250px'}):
            with solara.Column(align='center', style={'background-color':'rgb(28,43,51)'}):
                solara.Markdown('## Type in a question, someone may have already answered it', style={"padding":"12px 12px 12px 12px","font-size":"16px", "color":"white"})
                
                if placeholder:                
                    with solara.Link('/faq'):
                        with solara.Column(align='center', style={'background-color':'white', 'width':'620px','height':'60px','align-items':'center'}):
                            solara.InputText(label="Type a question . . .")
                else :                
                    with solara.Column(align='center', style={'background-color':'white', 'width':'620px','height':'60px','align-items':'center'}):
                        solara.InputText(label="Type a question . . .", value=filter, on_value=set_filter, continuous_update=True)

