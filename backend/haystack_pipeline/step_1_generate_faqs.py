
#!pip install discord.py farm-haystack[faiss] python-dotenv farm-haystack[inference] farm-haystack[preprocessing]
from dotenv import load_dotenv
load_dotenv()
import os
from haystack.pipelines import Pipeline
from haystack.nodes import PreProcessor
from haystack.nodes import PromptNode, PromptTemplate
from pathlib import Path
import json
from haystack.nodes import  JsonConverter

#* Refactor Discord Messages JSON file
DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')
DISCORD_MESSAGES_PATH_JSON = f'data/{DISCORD_SERVER_ID}_selected_channels_messages.json'
DISCORD_MESSAGES_PATH_JSON_FORMATTED = f'data/filtered_{DISCORD_SERVER_ID}_selected_channels_messages.json'

data_path = 'data/'
assets_path = 'solarathon/assets/'
if os.getenv('run_locally') == '1':
    data_path = f'../../{data_path}'
    assets_path = f'../../{assets_path}'

FULL_FAQS_PATH = f'{assets_path}full_faq.json'

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

discord_messages = json.loads(open(DISCORD_MESSAGES_PATH_JSON).read())
discord_messages = [
    {  
     'id' : m['id'], 
     'author_id' : m['author_id'], 
     'content' : m['content'],
     'content_type' : 'text',
     'reference_id' : m['reference_id'], 
     'created_at' : m['created_at']
     } for m in discord_messages
]
with open(DISCORD_MESSAGES_PATH_JSON_FORMATTED, 'w') as f:
    json.dump(discord_messages, f)

preprocessor = PreProcessor( # https://docs.haystack.deepset.ai/docs/preprocessor
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=True,
  	remove_substrings=None,
    split_by=None, # Unit for splitting the document. Can be "word", "sentence", or "passage". Set to None to disable splitting.
    split_length=100,
    split_respect_sentence_boundary=False,
    split_overlap=0,
  	max_chars_check = 600000
)

file_converter = JsonConverter() # https://docs.haystack.deepset.ai/docs/file_converters
p = Pipeline()
p.add_node(component=file_converter, name="FileConverter", inputs=["File"])
p.add_node(component=preprocessor, name="PreProcessor", inputs=["FileConverter"])

message_documents = p.run(file_paths = [DISCORD_MESSAGES_PATH_JSON_FORMATTED])

# llm = 'gpt-3.5-turbo-16k'
llm = 'gpt-4-0613'
max_length = 3000

# Initalize the node
prompt_template = PromptTemplate("""
                   You are a really smart conversation analyzer that generate Frequently Asked Questions document from users messages.
                   Your goal is to identify the main questions and problems that users have with the Solara.
                   Solara is a new and fantastic framework for development of web app using python.
                   The following context contains some messages.
                   Your goal is to identify the different conversations between the messages.
                   The given context is a list of JSON messages.
                   
                   Some attributes are given:
                    - id: The ID of the message.
                    - author_id: The ID of the message write.
                    - content: The content of the message.
                    - reference_id: The ID of the parent message. If the message is not a reply, this will be None. Otherwise, this value indicates that the message is a reply to the message with the specified ID.
                   
                   Take a deep breath and work on this step by step.
                   Your Goal is to identify the main problems and questions that users have and summarize the content:
                   - Question : Summarize different similar questions within a specific question.
                   - Answer : Summarize the response in order to provide a comprensive answer with relative step of resolution if any messages provide the solution. 
                        If you don't find the answer to this general question, skip the question.
                   - Topic : The main specific topic.
                   - Integration: a list of python libraries, code framework, and/or cloud provider that are related to the question.
                   - Category : Generate some consistent category related to the question.
                    
                    Query : {query}
                                 
                    Context: {join(documents)}
                   """)

prompt_node = PromptNode(
    llm, 
    api_key=OPENAI_API_KEY, 
    max_length=max_length, # The maximum number of tokens the generated text output can have,
    default_prompt_template=prompt_template,
    model_kwargs={
        "temperature": 0,
        "response_format": { "type": "json_object" }
        }
    )

def run_pipeline(docs):
    pipe = Pipeline()
    pipe.add_node(component=prompt_node, name="prompt_node", inputs=["Query"])
    output = pipe.run(query="""
                    Remember, your main goal is to summarize the messages to create a Frequently Asked Questions document where each 
                    element is a question-answer pair with only the requested attributes. Do not include warnings.
                    Return the output as a JSON array in the following format:
                        [
                            {
                                "question": "Question 1",
                                "answer": "Answer 1",
                                "topic" : "Topic 1" ,
                                "integrations" : ["integration1", "integration2" ] ,
                                "category" : "Category A"
                            },
                            {
                                "question": "Question 2",
                                "answer": "Answer 2",
                                "topic" : "Topic 1" ,
                                "integrations" : ["integration1", "integration2" ] ,
                                "category" : "Category A"
                            }
                        ] 
                    Do not deviate from the specified JSON array format.""", 
                    documents=docs
                    )
    return pipe,  output

full_docs = []
DOCUMENTS = message_documents['documents']
for i in range(0, len(DOCUMENTS), 80) :
    try:
        pipe , out = run_pipeline(DOCUMENTS[i:(i+80)])
        # print(out['results'][0])
        full_docs.append(out)
        with open(f'data/faq_{i}.json', 'w') as f:
            json.dump(out['results'][0], f)
            print(f'PROCESSED - Chunck messages from {i} to {i+80}')
    except:
        print(f'SKIPPED - Chunck messages from {i} to {i+80}')

from pathlib import Path
full_json_docs = []
for jpath in Path('data').glob('faq_*.json'):
    try:
        data = json.load(open(jpath))
        print(len(data))
        full_json_docs.extend( json.loads(data,  strict=False) )
        print(f'PROCESSED - JSON Parsing ok from {jpath}')
    except Exception as e:
        print(f'SKIPPED - JSON Parsing Failed from {jpath} - {e}')
        

print('total discord message : ', len(full_json_docs))


for i,_ in enumerate(full_json_docs):
    full_json_docs[i]['id'] = i+1
    
with open(FULL_FAQS_PATH, 'w') as f:
    json.dump(full_json_docs, f)