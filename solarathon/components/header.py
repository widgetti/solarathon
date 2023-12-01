import uuid
from typing import Callable, List, Literal, Optional, Union

import solara
from solara.components.input import use_change

@solara.component
def Header():
    
    with solara.Column(style = {'padding':'12px', 'background':'rgba(28,43,51,0.01)',"font-size":"14px",'z-index':100}):
        with solara.Row(gap='24px',style = {'padding':'12px', 'background':'rgb(245,246,246)',"font-size":"14px"}):
            solara.Text('Main Page')
            with solara.Link(f"/"):
                solara.Text('Home Page') 
            with solara.Link(f"/category"):
                solara.Text('Categories')  
            with solara.Link(f"/faq"):
                solara.Text('All FAQs')  