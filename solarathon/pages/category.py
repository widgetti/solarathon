from typing import Optional
import solara
from solarathon.core.import_data import import_raw_data
from solarathon.ui_utils import cat2path
from solarathon.components import header, footer, input_search, faq_card, general

@solara.component
def Page(cat_name: Optional[str] = None, page: int = 0, page_size=100):

    print('category Page')
    data,categories,topics = solara.use_memo(import_raw_data, [])


    with solara.Column( style={"padding-top": "0px"}):
        #** Header Bar
        header.Header()
        #** Texts
        general.main_text()
        #** Search Bar Block
        input_search.RetrieverInputBar(placeholder=True)
    
        if cat_name is None:
            with solara.Column(align='center', style={ 'width':'100%' }):
                with solara.Row(justify='start',style={ 'width':'900px'}):

                    with solara.Column():
                        solara.Text('Trending Categories', style={"padding":"12px 12px 12px 12px","font-size":"24px"})

                        with solara.GridFixed(columns=3):
                            for category in list(categories.keys()):
                                with solara.Card(category):
                                                                        
                                        with solara.Link(f"/category/{cat2path(category)}"):
                                            solara.Text('Read more')
                            with solara.Card('All'):                
                                    with solara.Link(f"/category"):
                                        solara.Text('See all categories')
        else:
            cat = cat2path(cat_name)
            print(f'category Page --> cat_name : {cat}')
            cat_faqs = [faq for faq in data if cat2path(faq['category'])==cat]
            with solara.Column(style={'height':'1000px'}):
                with solara.GridFixed(columns=3):
                    for faq in cat_faqs:
                        faq_card.FaqCard(faq)
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
            
        footer.Footer()