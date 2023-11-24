"""Dashboard

dashboard where people could select info cards on selected tokens from Binance
1) So you open up to the page,
2) it has 6 cards of randomly chosen tokens, 
3) you can add/remove new cards for a selected token that contain information from the Binance API

Basically a personalized crypto information dashboard

TODO:
#can be added setting for init basket of tickers
#default_currency can be taken from key qoteAsset from api/v3/exchangeInfo
#responsiveness
#refactor
"""

import solara
from typing import Optional
import requests

# some app state that outlives a single page
init_app_state = solara.reactive(["ada", "btc","bnb", "eth","doge", "xrp"])

@solara.component
def GeckoIcon (name: str, img: str):
    with solara.v.Html(tag="a", attributes={"href": f"https://www.binance.com/en/trade", "target": "_blank"}):
        with solara.v.ListItem(class_="pa-0"):
            with solara.v.ListItemAvatar(color="grey darken-3"):
                solara.v.Img(
                    class_="elevation-6",
                    src=img,
                )
            with solara.v.ListItemContent():
                solara.v.ListItemTitle(children=[name], class_="v-list-item__title_avatar")

def processColor(procentChange):
    if procentChange.startswith("-"):
        return "red"
    else:
        return "green"
    
def decimals(price):
    price_float = float(price)
    rounded_price = round(price_float, 2)
    return rounded_price

def format_price(price):
    formatted_price = '{:,.0f}'.format(float(price)).replace(',', ' ')
    return formatted_price

@solara.component
def DashboardCard(price: str, procentChange: str, icon: solara.Element = None, market_cap: Optional[str] = None,  market_cap_change_percentage: Optional[str] = None, pending: Optional[bool] = False): 
    if pending:
             with solara.Card(
            GeckoIcon('', '')
            , style={"width":"330px", "min-width": "280px","max-width": "350px", "background-color": "#1B2028", "color": "#ffff", "border-radius": "16px", "padding": "20px", "box-shadow": "rgba(0, 0, 0, 0) 0px 0px, rgba(0, 0, 0, 0) 0px 0px, rgba(0, 0, 0, 0.2) 0px 4px 6px -1px, rgba(0, 0, 0, 0.14) 0px 2px 4px -1px"}, margin=0, classes=["my-2", "mx-auto",]):
    
                with solara.Div():
                    with solara.Div(
                        style={
                        "display": "inline",
                        "color": "white",
                        "position": "relative",
                        "filter": "blur(3px)",
                        "opacity": "0.5",
                    },
                ):
                        with solara.GridFixed(columns=2, justify_items="space-between", align_items="baseline"):
                            solara.Text('loading', style={"font-size": "1.5rem", "font-weight": 500})
                            solara.Text(str("price"), style={"font-size": "0.6rem"})
                            solara.Text('loading', style={"font-weight": 400})
                            solara.Text(str("market cap"), style={"font-size": "0.6rem"})
                            solara.Text('loading', style={"font-weight": 500})
                            solara.Text(str("24h change price"), style={"font-size": "0.6rem"})
                            solara.Text('loading', style={"font-weight": 500})
                            solara.Text(str("24h change market cap"), style={"font-size": "0.6rem"})
    else:
        with solara.Card(
            icon
            , style={"width":"330px", "min-width": "280px","max-width": "350px", "background-color": "#1B2028", "color": "#ffff", "border-radius": "16px", "padding": "20px", "box-shadow": "rgba(0, 0, 0, 0) 0px 0px, rgba(0, 0, 0, 0) 0px 0px, rgba(0, 0, 0, 0.2) 0px 4px 6px -1px, rgba(0, 0, 0, 0.14) 0px 2px 4px -1px"}, margin=0, classes=["my-2", "mx-auto",]):
                with solara.Div():
                    with solara.Div(
                        style={
                        "display": "inline",
                        "color": "white",
                        "position": "relative",
                    },
                ):
                        with solara.GridFixed(columns=2, justify_items="space-between", align_items="baseline"):
                            solara.Text(str(f"{decimals(price)}$"), style={"font-size": "1.5rem", "font-weight": 500})
                            solara.Text(str("price"), style={"font-size": "0.6rem"})
                            if market_cap is not None: solara.Text(str(f"{format_price(decimals(market_cap))}$"), style={"font-weight": 400})
                            if market_cap is not None:  solara.Text(str("market cap"), style={"font-size": "0.6rem"})
                            solara.Text(str(procentChange + "%"), style={"color": processColor(procentChange), "font-weight": 500})
                            solara.Text(str("24h change price"), style={"font-size": "0.6rem"})
                            if market_cap_change_percentage is not None: solara.Text(str(market_cap_change_percentage) + "%", style={"color": processColor(procentChange), "font-weight": 500})
                            if market_cap_change_percentage is not None: solara.Text(str("24h change market cap"), style={"font-size": "0.6rem"})

@solara.component
def Page():
    loading, set_loading = solara.use_state(True)
    default_currency = "USDT"
    default_echange = "Binance"
    symbols_url = "https://api.binance.com/api/v3/exchangeInfo"
    coingecko_json_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc"
    binance_url = "https://api.binance.com/api/v3/ticker/24hr?symbol="

    try:
        symbols_response = requests.get(symbols_url, verify=False)
        symbols_data = symbols_response.json()
        available_symbols = sorted(list(set([symbol['baseAsset'].lower() for symbol in symbols_data['symbols']])))
    except Exception as e:
        available_symbols = []

    all_tickers = list(init_app_state.value) + available_symbols

    solara.SelectMultiple(f"Tickers from {default_echange}", init_app_state, all_tickers)

    solara.Style(
        """
        .v-list-item__title_avatar {
          color: white !important;
        }

        .v-list-item__content {
            color: #1B2028;
        }

        .v-application .primary--text {
            color: #1B2028 !important;
        }

        .v-label {
            color: #1B2028 !important;
            font-size: 0.8rem;
            font-weight: 500;
        }

        .v-card {
            height: 100%;
        }
        """
    )

    with solara.GridFixed(columns=3, align_items="end", justify_items="stretch"):
     try:
          coingecko_response = requests.get(coingecko_json_url, verify=False)
          coingecko_data = coingecko_response.json()
          for symbol in init_app_state.value:
            coingecko_data_for_symbol = get_data_for_symbol(symbol, coingecko_data)
            json_url = f"{binance_url}{symbol.upper()}{default_currency}"
            response = requests.get(json_url, verify=False)
            data = response.json()              

            if coingecko_data_for_symbol:
             set_loading(False)
             DashboardCard(data['lastPrice'], data['priceChangePercent'], GeckoIcon(data['symbol'], coingecko_data_for_symbol['image']), coingecko_data_for_symbol['market_cap'], coingecko_data_for_symbol['market_cap_change_percentage_24h'], loading)
            else:
                 set_loading(False)
                 DashboardCard(data['lastPrice'], data['priceChangePercent'], data['symbol'], loading)

     except Exception as e:
         print(f"An error occurred: {e}")
         solara.Error(f"Error {e}")
     
def get_data_for_symbol(symbol, coingecko_list):
    for coin in coingecko_list:
        if coin.get('symbol') == symbol:
            return coin
    return None
