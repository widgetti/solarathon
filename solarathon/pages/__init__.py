import solara
from pathlib import Path
import json

# Declare reactive variables at the top level. Components using these variables
# will be re-executed when their values change.
sentence = solara.reactive("Solara makes our team more productive.")
word_limit = solara.reactive(10)


# in case you want to override the default order of the tabs
route_order = ["/", "settings", "chat", "clickbutton"]

import os
openaikey = solara.reactive("")
openaikey = os.getenv("OPENAI_API_KEY")
DISCORD_SERVER_ID = solara.reactive("")
DISCORD_SERVER_ID = os.getenv("DISCORD_SERVER_ID")

@solara.component
def Page():
    with solara.Column(style={"padding-top": "30px"}):
        with solara.Column(align='center',gap='4px'):
            solara.Markdown("# Welcome to", style={"padding":"0px 0px 0px 0px","font-size":"16px"})
            solara.Markdown("## Solara Help Center", style={"padding":"0px 0px 0px 0px","font-size":"32px"})

        with solara.Row(justify='center', style={'background-color':'rgb(28,43,51)', 'height':'250px'}):
            with solara.Column(align='center', style={'background-color':'rgb(28,43,51)'}):
                solara.Markdown('## Frequently Asked Questions', style={"padding":"12px 12px 12px 12px","font-size":"16px", "color":"white"})
                with solara.Column(align='center', style={'background-color':'white', 'width':'320px'}):
                    solara.InputText('Type a question . . .')
                
        raw_data = Path(__file__).parent.parent
        with open(raw_data / 'assets' / 'full_fe_faqs.json' , 'r' ) as f:
            raw = json.loads(f.read())
        solara.Markdown(f'{raw}')

@solara.component
def Layout(children):
    # this is the default layout, but you can override it here, for instance some extra padding
    return solara.AppLayout(
                    children=children, 
                    navigation=False,
                    style={"padding": "20px"}
                    # style={"background-color": "red"}
                    )
