from typing import Optional
from solarathon.components import footer
import os
import json
from collections import Counter
from solarathon.components import header

import solara

ENV = os.getenv('ENV')
# data_path = '../../' if ENV == 'LOCAL' else ''
data_path = Path(__file__).parent.parent
FULL_FAQS_PATH = f'{data_path}/assets_backup/full_faq.json'


def import_raw_data():
    data = json.loads(open(FULL_FAQS_PATH).read())
    categories = Counter([f['category'] for f in data])
    topics = set([f['topic'] for f in data])
    print(data[:3])
    print(categories)
    # print(topics)
    return data,categories,topics



@solara.component
def Page(faq_id: Optional[str] = None, page: int = 0, page_size=100):


    data,categories,topics = solara.use_memo(import_raw_data, [])


    with solara.Column( style={"padding-top": "0px"}):
        header.Header()
            
                
        with solara.Column(align='center',gap='4px'):
            solara.Text('Welcome to', style={"padding":"0px 0px 0px 0px","font-size":"22px"})
            solara.Text("Solara Help Center", style={"padding":"24px 24px 24px 24px","font-size":"32px","font-weight": "bold"})

        with solara.Row(justify='center', style={'background-color':'rgb(28,43,51)', 'height':'250px'}):
            with solara.Column(align='center', style={'background-color':'rgb(28,43,51)'}):
                solara.Markdown('## Type in a question, someone may have already answered it', style={"padding":"12px 12px 12px 12px","font-size":"16px", "color":"white"})
                with solara.Column(align='center', style={'background-color':'white', 'width':'620px','height':'60px','align-items':'center'}):
                    solara.InputText('Type a question . . .')
        
        if faq_id is None:
                    with solara.GridFixed(columns=3):

                        for faq in data:
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
                                            with solara.Link(f"/faq/{faq['id']}"):
                                                solara.Button('Read more', classes=['faqbutton'])
        else:
            print(faq_id)
            faq = [faq for faq in data if faq['id']==int(faq_id)][0]
            print(faq)
            print(data[0])
            
            with solara.ColumnsResponsive([8,4]):
                
                with solara.Column(style={'height':'1000px'}):
                            solara.Text(faq['question'], style={"padding":"24px 24px 24px 24px","font-size":"24px"})
                            solara.Text(faq['answer'], style={"padding":"24px 24px 24px 24px","font-size":"20px"})
                with solara.Column():
                    pass
                        # with solara.GridFixed(columns=3):
                        #     for cat in data[:9]:
                                
            
        footer.Footer()  