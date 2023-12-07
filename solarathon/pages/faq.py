from typing import Optional
import solara
from solarathon.core.import_data import import_raw_data
from solarathon.ui_utils import cat2path
from solarathon.components import header, footer, input_search, faq_card, general
from solarathon.doc_functions import *

@solara.component
def Page(faq_id: Optional[str] = None, page: int = 0, page_size=100):
    
    print(f'faq Page')
    
    data,categories,topics = solara.use_memo(import_raw_data, [])
    filter, set_filter = solara.use_state("")

    with solara.Column( style={"padding-top": "0px"}):
        #** Header Bar
        header.Header()
        #** Texts
        general.main_text()
        #** Search Bar Block
        input_search.RetrieverInputBar(filter=filter, set_filter=set_filter)

        if faq_id is None:
            
            if filter:
                    retrieved_docs = input_search.retriever.run_query(filter)
                    results = list_retriever_results(retrieved_docs, show_score=False)
                    print(results)
                    faqs_f = results
            else: faqs_f = data
            
            with solara.GridFixed(columns=3):

                for faq in faqs_f:
                    title  = faq['question'] if len(faq['question'])<60 else faq['question'][:60] + '...'
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
            print(f'faq Page --> faq_id : {faq_id}')
            faq = [faq for faq in data if faq['id']==int(faq_id)][0]
            
            with solara.ColumnsResponsive([8,4]):
                
                with solara.Column(style={'height':'1000px'}):
                            solara.Text(faq['question'], style={"padding":"24px 24px 24px 24px","font-size":"24px"})
                            solara.Text(faq['answer'], style={"padding":"24px 24px 24px 24px","font-size":"20px"})
                            
                with solara.Column():
                    pass
                
        footer.Footer()  