"""# Dashboard

dashboard where people could select info cards on selected tokens from Binance
1) So you open up to the page,
2) it has 6 cards of randomly chosen tokens, 
3) you can add/remove new cards for a selected token that contain information from the Binance API

Basically a personalized crypto information dashboard

TODO:
#can be added setting for init basket of tickers
#loading state
#error state
#responsiveness
#refactor
"""

import solara
from typing import Optional
from solara.alias import rv
import requests

# some app state that outlives a single page
init_app_state = solara.reactive(["btc", "eth", "bnb", "ada", "xrp", "doge"])

@solara.component
def GeckoIcon (name: str, handle: str, img: str):
    with solara.v.Html(tag="a", attributes={"href": f"https://www.binance.com/", "target": "_blank"}):
        with solara.v.ListItem(class_="pa-0"):
            with solara.v.ListItemAvatar(color="grey darken-3"):
                solara.v.Img(
                    class_="elevation-6",
                    src=img,
                )
            with solara.v.ListItemContent():
                solara.v.ListItemTitle(children=[name])

def processColor(procentChange):
    if procentChange.startswith("-"):
        return "red"
    else:
        return "green"
    

@solara.component
def DashboardCard(symbol: str, symbolName: Optional[str], image_url: str, market_cap_change_percentage: str, price: str, procentChange: str):
    with solara.Card(
        GeckoIcon(symbol, symbol, image_url)
        , style={"width":"330px", "min-width": "280px","max-width": "350px", "background-color": "#1B2028", "color": "#ffff", "border-radius": "16px", "padding": "20px", "box-shadow": "rgba(0, 0, 0, 0) 0px 0px, rgba(0, 0, 0, 0) 0px 0px, rgba(0, 0, 0, 0.2) 0px 4px 6px -1px, rgba(0, 0, 0, 0.14) 0px 2px 4px -1px"}, margin=0, classes=["my-2", "mx-auto",]):
        price_float = float(price)
        rounded_price = round(price_float, 2)
       
        with solara.Div():
            with solara.Div(
                style={
                "display": "inline",
                "color": "white",
                "position": "relative",
            },
        ):
                with solara.GridFixed(columns=2, justify_items="space-between", align_items="baseline"):
                 solara.Text(str(f"{rounded_price}$"), style={"font-size": "1.5rem", "font-weight": 500})
                 solara.Text(str("price"), style={"font-size": "0.5rem"})
                 solara.Text(str(procentChange + "%"), style={"color": processColor(procentChange), "font-weight": 500})
                 solara.Text(str("24h change price"), style={"font-size": "0.5rem"})
                 solara.Text(str(market_cap_change_percentage) + "%", style={"color": processColor(procentChange), "font-weight": 500})
                 solara.Text(str("24h change market cap"), style={"font-size": "0.5rem"})
   

@solara.component
def Page():
    default_currency = "USDT"
    all_tickers = list(init_app_state.value) + ["link", "atom", "usdc", "xrp"]

    solara.SelectMultiple("Tickers", init_app_state, all_tickers)

    solara.Style(
        """
        .v-list-item__title {
          color: white !important;
        }
        """
    )

    with solara.GridFixed(columns=3, align_items="end", justify_items="stretch"):
     try:
          image_coingecko_json_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc"
          coingecko_response = requests.get(image_coingecko_json_url, verify=False)
          coingecko_data = coingecko_response.json()
          for symbol in init_app_state.value:
            image_url, coin_name, market_cap_change_percentage_24h = get_image_for_symbol(symbol, coingecko_data)
            if image_url and coin_name:
                json_url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol.upper()}{default_currency}"
                response = requests.get(json_url, verify=False)
                data = response.json()
                DashboardCard(data['symbol'], coin_name, image_url, market_cap_change_percentage_24h, data['lastPrice'], data['priceChangePercent'])
            else:
                print(f"Could not find image for {symbol}")
                None
    
     except Exception as e:
         print(f"An error occurred: {e}")
         solara.Error(f"Error {e}")

     
def get_image_for_symbol(symbol, coingecko_list):
    for coin in coingecko_list:
        if coin.get('symbol') == symbol:
            return coin.get('image'), coin.get('name'), coin.get('market_cap_change_percentage_24h')
    return None, None, None
