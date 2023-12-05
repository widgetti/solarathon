import solara

@solara.component
def FaqCard(faq):
    # print(faq)
    title =  faq['question'] if len(faq['question'])< 60 else faq['question'][:60] + '...'
    answer = faq['answer']   if len(faq['answer'])  < 200 else faq['answer'][:200]   + '...'
    # print(faq['title'])
    # print(len(faq['answer']))

    with solara.Column(
            style={'width':'90%', 
                    'height':'250px',
                    'padding':'6px',
                    'justify-content': 'space-between'
                    }):                               
        with solara.Column(style={'width':'100%'}):                                
            solara.Markdown(answer.replace("```", "```\n") , unsafe_solara_execute = True)
            
        with solara.Column(style={'width':'100%','align-self':'flex-end'}):
            with solara.Row(justify='end'):
                with solara.Link(f"/faq/{faq['id']}"):
                    solara.Button('Read more', classes=['faqbutton'])