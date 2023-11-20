import solara
import solarathon.pages


@solara.component
def Page():
    # make the slider not go under the tabs
    with solara.Column(style={"padding-top": "30px"}):
        solara.SliderInt("Word limit", value=solarathon.pages.word_limit, min=2, max=20)
