import streamlit as st
import yfinance as yf

import pandas as pd
import plotly.graph_objects as go
import warnings
from PIL import Image
from io import BytesIO
warnings.filterwarnings('ignore')
pd.options.display.float_format = '${:,.2f}'.format
import cryptolinear
import sentimental_analysis
import Stock
global start;
global crypto_names;
global end;
global crypto_symbol;
global symbol;
import requests as rs

def main():
    option2 = st.sidebar.selectbox("What You Want To Look?", (" ","News Articles", "Techincal Analysis"),key="opt2")

    if(option2=="News Articles"):
        news()
    elif(option2=="Techincal Analysis"):
        technical()
def news():

    url="https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key=1fdf1ebe58e8d107176e8ab8ce54ed713e259ce0300d7e8b4069e3df5f568bf9"
    newsdata=rs.get(url)
    newsdata=newsdata.json()
    #st.write(len(newsdata['Data']))
    leng=len(newsdata['Data'])
    temp1=st.columns(leng)
    for i in range(0,len(newsdata['Data'])):

        im=newsdata['Data'][i]['imageurl']
        im=rs.get(im)
        img=Image.open(BytesIO(im.content))
        newsize = (150, 150)
        img = img.resize(newsize)
        st.info(newsdata['Data'][i]['title'])
        st.image(img)
        st.write(newsdata['Data'][i]['body'])



def crypto_name(symbol):
   symbol=symbol.upper()
   if symbol=="BTC":
        return "Bitcoin "
   elif symbol=="ETH":
       return "ETHEREUM"
   elif symbol == "SOLANA":
       return "Solana "
   elif symbol == "LITECOIN":
       return "LiteCoin "
   elif symbol=="BINANCE_COIN":
       return "BNB coin "
   else:
        return None


def common_stat(df,cryname):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,

        open=df['Open'],
        close=df['Close'],
        high=df['High'],
        low=df['Low'],
        increasing_line_color='green',
        decreasing_line_color='red'

    )])
    st.header(cryname+"Data")
    st.write(df)

    st.header(cryname+"Data Statistics")
    st.write(df.describe())

    st.header(cryname+"Close Price")
    st.line_chart(df['Close'])

    st.header(cryname+"Volume")
    st.line_chart(df['Volume'])

    st.header(cryname+" CANDLE STICK")
    st.plotly_chart(fig)

def get_data(symbol,start,end,cn):
    symbol=symbol.upper()
    if(symbol=="BTC"):
        df = yf.download('BCH-USD', start, end)
        cryptoname=cn
        common_stat(df,cryptoname)
        tecbtc = st.sidebar.selectbox("TECHNICAL ANALYSIS", ("Linear Prediction","Sentimental Analysis","Coming Soon"))
        if (tecbtc == "Linear Prediction"):
           cryptolinear.linreg(start, end, df)
        elif (tecbtc == "Sentimental Analysis"):
           sentimental_analysis.senti(cryptoname)
        else:
            st.write("New Features Coming Soon...")

    elif(symbol=="ETH"):
        df=yf.download('ETH-USD', start, end)
        cryptoname = cn
        tec = st.sidebar.selectbox("TECHNICAL ANALYSIS", ("Linear Prediction","Sentimental Analysis","Coming Soon"))
        common_stat(df, cryptoname)

        if (tec == "Linear Prediction"):
            cryptolinear.linreg(start, end, df)
        elif (tec == "Sentimental Analysis"):
           sentimental_analysis.senti(cryptoname)
        else:
            st.write("New Features Coming Soon...")



    elif(symbol=="SOLANA"):
        df = yf.download('SOL1-USD', start, end)
        cryptoname=cn
        common_stat(df, cryptoname)
        tecdodge = st.sidebar.selectbox("TECHNICAL ANALYSIS", ("Linear Prediction","Sentimental Analysis", "Coming Soon"))
        if (tecdodge == "Linear Prediction"):
            cryptolinear.linreg(start, end, df)
        elif (tecdodge == "Sentimental Analysis"):
           sentimental_analysis.senti(cryptoname)
        else:
            st.write("New Features Coming Soon...")

    elif (symbol =="LITECOIN"):
        df = yf.download('LTC-USD', start, end)
        cryptoname = cn
        tectether = st.sidebar.selectbox("TECHNICAL ANALYSIS", ("Linear Prediction","Sentimental Analysis", "Coming Soon"))
        common_stat(df, cryptoname)

        if (tectether == "Linear Prediction"):
            cryptolinear.linreg(start, end, df)
        elif (tectether == "Sentimental Analysis"):
           sentimental_analysis.senti(cryptoname)
        else:
            st.write("New Features Coming Soon...")


    elif (symbol =="BINANCE_COIN"):
        df = yf.download('BNB-USD', start, end)
        cryptoname = cn
        tectether = st.sidebar.selectbox("TECHNICAL ANALYSIS", ("Linear Prediction","Sentimental Analysis", "Coming Soon"))
        common_stat(df, cryptoname)

        if (tectether == "Linear Prediction"):
            cryptolinear.linreg(start, end, df)
        elif (tectether == "Sentimental Analysis"):
           sentimental_analysis.senti(cryptoname)
        else:
            st.write("New Features Coming Soon...")
    else:
        None
    return df.loc[start:end]


def technical():
    symbol = st.sidebar.selectbox("Crypto Symbol", ("BTC", "ETH", "SOLANA", "LITECOIN", "BINANCE_COIN"))
    crypto_names = crypto_name(symbol)
    if(symbol=="BTC"):
            start = st.sidebar.text_input(label="Start Date", value="2017-08-01",key="sd")
            end = st.sidebar.text_input(label="End Date", value="2021-01-01",key="ed")
    elif(symbol=="ETH"):
            start = st.sidebar.text_input(label="Start Date", value="2015-07-30", key="sd")
            end = st.sidebar.text_input(label="End Date", value="2021-01-01", key="ed")
    elif (symbol == "SOLANA"):
            start = st.sidebar.text_input(label="Start Date", value="2020-04-10", key="sd")
            end = st.sidebar.text_input(label="End Date", value="2021-01-01", key="ed")
    elif (symbol == "LITECOIN"):
            start = st.sidebar.text_input(label="Start Date", value="2014-09-17", key="sd")
            end = st.sidebar.text_input(label="End Date", value="2021-01-01", key="ed")
    elif (symbol == "BINANCE_COIN"):
            start = st.sidebar.text_input(label="Start Date", value="2017-07-25", key="sd")
            end = st.sidebar.text_input(label="End Date", value="2021-01-01", key="ed")
    else:
            st.info("Select CryptoCurrency")
    if(start==end):
            st.write("START AND END DATE CANNOT BE SAME")

    else:
            get_data(symbol, start, end, crypto_names)
def start():
    st.markdown('**INVESTMENT DECISION TOOL**')
    image1 = Image.open("Investment.jpg")
    st.image(image1, use_column_width=True)

    option = st.selectbox("Select Market Type", ("INVESTMENT DECISION TOOL", "Stock Market", "Crypto_Market"),key="opt1")
    if (option == 'Stock Market'):
        Stock.main()
    elif (option == 'Crypto_Market'):
        #st.balloons()
        st.header("CRYTOCURRENCY DASHBOARD APPLICATION")
        st.header("The Rise Of Cryptocurrencies")
        st.write(
        "Cryptocurrency is a major topic of discussion recently as its market cap surged to a record $2 trillion in April 2021. To put that into comparison, the market cap of Apple, a 45 year old company has a market cap of around 2 trillion dollars as well.",
        "If you don’t know about cryptocurrencies yet, it might be the time to start learning about them. They are branded as the future of not just money, but many processes and operations that power our day-to-day lives. In simple terms, it’s like an amalgamation of cryptography, programming, and finance.",
        "Talking about cryptocurrency, Ethereum is the second-largest cryptocurrency by market capitalization, right behind Bitcoin. Its main purpose is to help execute decentralized smart contracts. As of today, its market cap is larger that big companies like Walmart, Netflix and Disney.")
        main()
    else:
        st.info('Kindly Select Type Of Market')


if __name__ == "__main__":
    start()









