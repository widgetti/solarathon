import solara
import reacton.ipyvuetify as rv

# @solara.component
# def FaqCard(faq):

#     title =  faq['question'] if len(faq['question'])< 60 else faq['question'][:60] + '...'
#     answer = faq['answer']   if len(faq['answer'])  < 200 else faq['answer'][:200]   + '...'

#     with solara.Card(title = title) :
#         with solara.Column(
#                 style={'width':'90%', 
#                         'height':'250px',
#                         'padding':'6px',
#                         'justify-content': 'space-between'
#                         }):                               
#             with solara.Column(style={'width':'100%'}):                                
#                 solara.Markdown(answer.replace("```", "```\n") , unsafe_solara_execute = True)
                
#             with solara.Column(style={'width':'100%','align-self':'flex-end'}):
#                 with solara.Row(justify='end'):
#                     with solara.Link(f"/faq/{faq['id']}"):
#                         solara.Button('Read more', classes=['faqbutton'])
                        
@solara.component
def FaqCard(faq):

    title =  faq['question'] if len(faq['question'])< 60 else faq['question'][:60] + '...'
    answer = faq['answer']   if len(faq['answer'])  < 200 else faq['answer'][:200]   + '...'

    with solara.Column(classes=['faqcard']) :
        
        with solara.Row(style = {'padding':'12px'}):
            solara.Markdown(f"""
                            ##{title}
                            """)
            
        with solara.Column(classes = ['faqcontainer']):
                                     
            with solara.Column(style={'width':'100%', 'height':'250px'}):                                 
                solara.Markdown(answer.replace("```", "```\n") , unsafe_solara_execute = True)
            
            with solara.Column(style={'width':'100%','align-self':'flex-end'}):
                with solara.Row(justify='end',style={'margin-bottom':'12px'}):
                    for integration in faq['integrations']:
                        with rv.Chip(color='blue', text_color='white', light=True, small=True):
                            solara.Text(integration)
            
            with solara.Column(style={'width':'100%','align-self':'flex-end'}):
                with solara.Row(justify='end'):
                    with solara.Link(f"/faq/{faq['id']}"):
                        solara.Button('Read more', classes=['faqbutton'])