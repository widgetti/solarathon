# import libraries
import solara
import yfinance as yf
import mplfinance as mpf
import pandas_ta as ta
from datetime import date, timedelta

# TODO: 
# add progress bar
# improve the performance 
# refactoring

# plot definition
def plotTA(ticker, days_range, returns, volume, bbanduplow, bbandmidd, ema10, ema30):

    # set the dates to download the data
    today_date = date.today() - timedelta(days=1)
    past_date = today_date - timedelta(days=days_range)
    message = ""

    # download data daily candles 
    try:
        # Attempt to download the data
        df = yf.download(tickers=ticker, start=past_date, end=today_date)
        message = "Download_successful"

    except Exception as e:
        # Handle the exception and return the error
        fig = mpf.plot(ta.DataFrame(), type='candle', style='yahoo', title='Empty Plot')
        return fig, e

    # Create a list to store plot configurations
    addplots = []

    # check the alternatives that has been selected, and add the plot to the list
    if (ema10.value):
        # calculate EMA10
        df['EMA10'] = ta.ema(df['Adj Close'], length=10)
        addplots.append(mpf.make_addplot(df['EMA10'], color='blue', secondary_y=False, label="EMA10"))
         
    if (bbanduplow.value):
        # calculate bbands
        df.ta.bbands(append=True)
        addplots.append(mpf.make_addplot(df['BBL_5_2.0'], color='purple', secondary_y=False, label="Low BBand"))
        addplots.append(mpf.make_addplot(df['BBU_5_2.0'], color='purple', secondary_y=False, label="Up BBand"))

    if (bbandmidd.value):
        # if not bbands calculation
        if "BBM_5_2.0" not in df.columns:
            df.ta.bbands(append=True)
        
        addplots.append(mpf.make_addplot(df['BBM_5_2.0'], color='orange', secondary_y=False, label="Mid BBand"))

    if (ema30.value):
        # calculate EMA30
        df['EMA30'] = ta.ema(df['Adj Close'], length=30)
        addplots.append(mpf.make_addplot(df['EMA30'], color='red', secondary_y=False, label="EMA30"))

    if (returns.value):
        # Calculate daily returns
        df['return'] = df['Adj Close'].pct_change()

        addplots.append(mpf.make_addplot(df["return"], color='silver', 
                                         alpha=0.45, secondary_y=True, label='Returns', type="bar", width=1))
    
    # Define the style of the candlestick chart
    style = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mpf.make_marketcolors(up='g', down='r'))

    # Create a subplot to display the candlestick chart and add indicators
    fig, axes = mpf.plot(df, volume=volume.value, type='candle', style=style, title=f'Candlestick and TA - {ticker}', 
                        ylabel='Price', addplot=addplots, figsize=(12, 8), returnfig=True)
    
  
    return fig, message

# Technical analysis, feature selection state initialization
bbanduplow = solara.reactive(True)
bbandmidd = solara.reactive(True)
ema10 = solara.reactive(True)
ema30 = solara.reactive(True)
days_range = solara.reactive(60)
returns = solara.reactive(False)
volume = solara.reactive(False)
message = ""

# Crypto ticker list from yahoo finance
crypto_list = ['BTC-USD', 'ETH-USD', 'USDT-USD', 'BNB-USD', 'XRP-USD', 'USDC-USD', 'SOL-USD',
               'STETH-USD', 'ADA-USD', 'DOGE-USD', 'TRX-USD', 'WTRX-USD', 'TON11419-USD', 'LINK-USD', 'AVAX-USD',
               'MATIC-USD', 'DOT-USD', 'WBTC-USD', 'DAI-USD', 'LTC-USD', 'WEOS-USD', 'SHIB-USD', 'BCH-USD',
               'LEO-USD', 'UNI7083-USD', 'OKB-USD', 'ATOM-USD', 'XLM-USD', 'TUSD-USD', 'XMR-USD']

# Initialization default ticker
crypto = solara.reactive("BTC-USD")

# solara component
@solara.component
def Page():
    solara.Markdown(r'''
    # Interactive Technical Analysis - Crypto assets
    ''')
    solara.Select(label="Select Crypto asset:", value=crypto, values=crypto_list)
    solara.SliderInt("Days range", value=days_range, min=30, max=365)
    with solara.GridFixed(columns=5):
        # feature selection 
        solara.Checkbox(label="Daily Returns", value=returns)
        solara.Checkbox(label="Volume", value=volume)
        solara.Switch(label="Bollinger Up/Low", value=bbanduplow)
        solara.Switch(label="Bollinger Middle", value=bbandmidd)
        solara.Switch(label="EMA10", value=ema10)
        solara.Switch(label="EMA30", value=ema30)

    # main function to plot technical indicator, input the component values
    fig, message = plotTA(crypto.value, days_range.value, returns, volume, bbanduplow, bbandmidd, ema10, ema30)
    solara.FigureMatplotlib(fig)
    
    # Status message for crypto selection
    if message == "Download_successful":
        solara.Success(f"Asset selected: {crypto} {message}", text=True, dense=True, outlined=True, icon=True)
    else:
        solara.Error(f"There was an Error {message}", dense=True, text=True, outlined=True, icon=True)
        
# The following line is required only when running the code in a Jupyter notebook
#Page()