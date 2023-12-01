import uuid
from typing import Callable, List, Literal, Optional, Union

import solara
from solara.components.input import use_change


@solara.component
def Footer():
    
    with solara.Column(style = {'padding':'12px', 'background':'rgb(28,43,51)',"font-size":"14px"}):
        with solara.Row(style={'width':'100%', 'justify-content':'space-around','background':'rgb(28,43,51)'}):
            with solara.Column():
                pass
            with solara.Column():
                pass
            with solara.Column():
                pass
            with solara.Column( gap = '24px' , style = {'padding':'12px', 'background':'rgb(28,43,51)',"font-size":"14px", "color":"white"}):
                solara.Text('Main Page')
                with solara.Link(f"/"):
                    solara.Text('Home Page') 
                with solara.Link(f"/category"):
                    solara.Text('Categories')  
                with solara.Link(f"/faq"):
                    solara.Text('All FAQs') 
            with solara.Column( gap = '24px' , style = {'padding':'12px', 'background':'rgb(28,43,51)',"font-size":"14px", "color":"white"}):
                solara.Text('Main Page')
                with solara.Link(f"/"):
                    solara.Text('Home Page') 
                with solara.Link(f"/category"):
                    solara.Text('Categories')  
                with solara.Link(f"/faq"):
                    solara.Text('All FAQs') 