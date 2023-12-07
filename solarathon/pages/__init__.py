import solara
from solarathon.core.import_data import import_raw_data
from solarathon.ui_utils import cat2path
from solarathon.components import header, footer, input_search, faq_card,general

route_order = ["/", 'category','faq']

@solara.component
def Page():

    data,categories,topics = solara.use_memo(import_raw_data, [])

    with solara.Column( style={"padding-top": "0px"}):
        #** Header Bar
        header.Header()
        #** Texts
        general.main_text()
        #** Search Bar Block
        input_search.RetrieverInputBar(placeholder=True)
        
        with solara.Column(align='center', style={ 'width':'100%' }):
            with solara.Row(justify='start',style={ 'width':'1100px'}):
                #** Main Home Page Content Block
                with solara.Column():
                    
                    #** Categories Block
                    solara.Text('Tranding Categories', style={"padding":"12px 12px 12px 12px","font-size":"24px"})
                    with solara.GridFixed(columns=3):
                        for category in list(categories.keys())[:11]:
                            with solara.Card(category):
                                                                    
                                    with solara.Link(f"/category/{cat2path(category)}"):
                                        solara.Text('Read more')
                                        
                        with solara.Card('All'):                
                                with solara.Link(f"/category"):
                                    solara.Text('See all categories')   

                    #** Few FAQs Block
                    solara.Markdown("""
                                    Look for specific questions or problems in the Help Center above.\n
                                    Alternatively, explore these tips on how to troubleshoot ad issues and optimize your campaigns
                                    """, style={"padding":"12px 12px 12px 12px","font-size":"16px"})
                    with solara.GridFixed(columns=3, row_gap = '24px'):
                        # print(data[2])
                        for faq in data[:9]:
                            faq_card.FaqCard(faq)
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
                    )
