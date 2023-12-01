import solara
from pathlib import Path
import json
import duckdb
import os
from collections import Counter
from solarathon.components import header
from solarathon.components import input_search
from solarathon.components import footer
from pathlib import Path

ENV = os.getenv('ENV')
# data_path = '../../' if ENV == 'LOCAL' else ''

data_path = Path(__file__).parent.parent
FULL_FAQS_PATH = f'{data_path}/assets/full_faq.json'

# in case you want to override the default order of the tabs
route_order = ["/", 'category','faq']

openaikey = os.getenv("OPENAI_API_KEY")
faiss_filename = os.getenv("faiss_filename")
DISCORD_SERVER_ID = solara.reactive("")
DISCORD_SERVER_ID = os.getenv("DISCORD_SERVER_ID")

def import_raw_data():
    # raw_data = Path(__file__).parent.parent
    # with open(raw_data / 'assets' / 'full_fe_faqs.json' , 'r' ) as f:
    #     raw = json.loads(f.read())
    data = json.loads(open(FULL_FAQS_PATH).read())
    categories = Counter([f['category'] for f in data])
    topics = set([f['topic'] for f in data])
    # print(data[:3])
    # print(categories)
    # print(topics)
    return data,categories,topics

@solara.component
def Page():
    
    data,categories,topics = solara.use_memo(import_raw_data, [])

    with solara.Column( style={"padding-top": "0px"}):
        header.Header()

                
        with solara.Column(align='center',gap='4px'):
            solara.Text('Welcome to', style={"padding":"0px 0px 0px 0px","font-size":"22px"})
            solara.Text("Solara Help Center", style={"padding":"24px 24px 24px 24px","font-size":"32px","font-weight": "bold"})

        with solara.Row(justify='center', style={'background-color':'rgb(28,43,51)', 'height':'250px'}):
            with solara.Column(align='center', style={'background-color':'rgb(28,43,51)'}):
                solara.Markdown('## Type in a question, someone may have already answered it', style={"padding":"12px 12px 12px 12px","font-size":"16px", "color":"white"})
                with solara.Link('/faq'):
                    input_search.SearchRetriever()
        
        with solara.Column(align='center', style={ 'width':'100%' }):
            with solara.Row(justify='start',style={ 'width':'1100px'}):
                # text with size 18px:
                with solara.Column():
                    solara.Text('Tranding Categories', style={"padding":"12px 12px 12px 12px","font-size":"24px"})


                    with solara.GridFixed(columns=3):
                        for category in list(categories.keys())[:11]:
                            with solara.Card(category):
                                                                    
                                    with solara.Link(f"/category/{category.replace(' ','-')}"):
                                        solara.Text('Read more')
                        with solara.Card('All'):                
                                with solara.Link(f"/category"):
                                    solara.Text('See all categories')   

                    solara.Markdown("""
                                    Look for specific questions or problems in the Help Center above.\n
                                    Alternatively, explore these tips on how to troubleshoot ad issues and optimize your campaigns
                                    """, style={"padding":"12px 12px 12px 12px","font-size":"16px"})

                    with solara.GridFixed(columns=3):
                        for faq in data[:9]:
                            title = faq['question'] if len(faq['question'])<60 else faq['question'][:60] + '...'
                            answer = faq['answer'] if len(faq['answer'])<350 else faq['answer'][:350] + '...'
                            with solara.Card(title, classes=['faqcard']):
                                
                                with solara.Column(
                                        style={'width':'90%', 
                                               'height':'250px',
                                               'padding':'6px',
                                               'justify-content': 'space-between'
                                               }):                               
                                    with solara.Column(style={'width':'100%'}):                                
                                        solara.Markdown(answer)
                                        
                                    with solara.Column(style={'width':'100%','align-self':'flex-end'}):
                                        with solara.Row(justify='end'):
                                            with solara.Link(f"/faq/{faq}"):
                                            # with solara.Link(f"/faq/{faq['id']}"):
                                                solara.Button('Read more', classes=['faqbutton'])
        footer.Footer()        

@solara.component
def Layout(children):
    # duckdb.query(f"""
    #             INSTALL sqlite;LOAD sqlite; ATTACH '{data_path}solarathon/assets/{faiss_filename}' (TYPE SQLITE);
    #             """)
    # this is the default layout, but you can override it here, for instance some extra padding
    return solara.AppLayout(
                    children=children, 
                    navigation=False,
                    style={"padding": "0px"}
                    # style={"background-color": "red"}
                    )
