import streamlit as st
from pandas_datareader import data as web
import numpy as np

import plotly.graph_objects as go
from openpyxl import Workbook
from openpyxl import load_workbook

import cryptolinear


import yfinance as yfs

from yahoo_fin import news

import pandas as pd


def overview(start, end, df, mydict):
    result, assets, nodata = smadata(start, end, df, mydict)
    cut = str(assets[0]).split('.')[0]


    nw = str(assets[0])
    #st.write(assets[0])
    news_data = news.get_yf_rss(nw)
    firm_data = yfs.Ticker(nw)
    #analyst_data = get_analysts_info(str(firm_data))

    #mh=get_company_info(str(firm_data))
    #print(mh)
    #st.write(mh)
    #st.write(analyst_data)
    if(news_data):
        for i in range(0,len(news_data)):
            st.header(news_data[i]['title'])
            st.info(news_data[i]['summary'])



    else:
      st.error("We Are Working Hard On Retrieving News Data Of Selected Company")
      st.stop()






def main():
    #df=load_workbook('ticker.xlsx')
    df = pd.read_excel('ticker.xlsx',engine='openpyxl')
    st.header('Indian  Stock Market')
    st.subheader('The BSE and NSE')
    st.write("Most of the trading in the Indian stock market takes place on its two stock exchanges: "
             "the Bombay Stock Exchange (BSE) and the National Stock Exchange (NSE). The BSE has been in "
             "existence since 1875. The NSE, on the other hand, was founded in 1992 and started trading in 1994. "
             "However, both exchanges follow the same trading mechanism, trading hours, and settlement process.As of February 2020, the BSE had 5,518 listed firms "
             "whereas the rival NSE had about 1,799 as of Dec. 31, 2019. Out of all the listed firms on the BSE,"
             " only about 500 firms constitute more than 90% of its market capitalization; the rest of the crowd"
             " consists of highly illiquid shares.Almost all the significant firms of India are listed on both the"
             " exchanges. The BSE is the older stock market but the NSE is the largest stock market, in terms of volume. "
             "As such, the NSE is a more liquid market. In terms of market cap, they're both comparable at "
             "about $2.3 trillion. Both exchanges compete for the order flow that leads to reduced costs, market efficiency, "
             "and innovation. The presence of arbitrageurs keeps the prices on the two stock exchanges within a very tight "
             "range.")

    start = st.sidebar.text_input("Start Date", "2021-01-01")
    end = st.sidebar.text_input("End Date", "2022-01-01")
    if(start==end):
        st.error("Start and End Date Cannot Be Same")
        st.stop()

    method = st.sidebar.selectbox("Select Modelling Method", ("Trading Strategies","Company OverView","Portfolio Optimization","Future Price"))
    mydict = dict(zip(df['Name'], df['Ticker']))
    if (method == 'Portfolio Optimization'):
        portfolio(start, end, df, mydict)

    elif(method=='Future Price'):
        result, assets, nodata = smadata(start, end, df, mydict)
        cryptolinear.linreg(start,end,result)
    elif(method=='Company OverView'):
        overview(start,end,df,mydict)

    else:

        tstrat(start, end, df, mydict)






def hsma(start, end, df, mydict):
    col1, col2 = st.columns(2)

    with col1:
        sw = st.number_input("Enter Short Term Period:", min_value=0)
        sw = int(sw)
    with col2:
        lw = st.number_input("Enter Long Term Period:", min_value=0)
        lw = int(lw)
    if (sw > lw):
        st.info("Short Term Period Should be less than Long Term Period")
    else:
        result, assets,nodata= smadata(start, end, df, mydict)
        res = sma(sw, lw, result)
        # st.write(result)
        result['Signal'] = 0.0
        result['Signal'] = np.where(result['Short-Period MA'] > result['Long-Period MA'], 1.0, 0.0)
        result['Position'] = result['Signal'].diff()
        plotres = plot(result, assets)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        #st.pyplot()
        # st.write(result)


def rsi(start, end, df, mydict):
    period = st.number_input("Enter Term Period",min_value=1)
    period=int(period)
    if (period == None):
        st.error("Enter Valid Time Period")
        st.stop()
    else:

        data = smadata(start, end, df, mydict)
        rdata = pd.DataFrame(data[2])

        delta = rdata['Adj Close'].diff(1)
        delta.dropna(inplace=True)
        positive = delta.copy()
        negative = delta.copy()
        positive[positive < 0] = 0
        negative[negative > 0] = 0

        avg_gain = positive.rolling(window=period).mean()

        avg_loss = abs(negative.rolling(window=period).mean())
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))
        combined = pd.DataFrame()
        combined['Adj Close'] = rdata['Adj Close']
        combined['RSI'] = rsi
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=combined.index, y=combined['Adj Close'], mode='lines', name='Adj Close',
                                 line=dict(color="Silver", width=1)))
        fig.update_layout(
            width=800,
            height=500,
            paper_bgcolor="LightSteelBlue",
            title={
                'text': "Adj Close Price",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis_title="Date",
            yaxis_title="Price",
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        st.plotly_chart(fig)
        figrsi = go.Figure()
        figrsi.add_trace(go.Scatter(x=combined.index, y=combined['RSI'], mode='lines', name='RSI',
                                    line=dict(color="Silver", width=1)))

        figrsi.add_hline(y=0, line_dash="dash",line_color="fuchsia")
        figrsi.add_hline(y=10, line_dash="dot",line_color="Orange")
        figrsi.add_hline(y=20, line_dash="dot",line_color="darkviolet")
        figrsi.add_hline(y=30, line_dash="dot" ,line_color="darkturquoise")
        figrsi.add_hline(y=70, line_dash="dot",line_color="darkturquoise")
        figrsi.add_hline(y=80, line_dash="dot",line_color="darkviolet")
        figrsi.add_hline(y=90, line_dash="dot",line_color="Orange")
        figrsi.add_hline(y=100, line_dash="dash",line_color="fuchsia")

        figrsi.update_layout(
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            width=800,
            height=500,
            paper_bgcolor="LightSteelBlue",
            title={
                'text': "Relative Strength Index",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis_title="Date",
            yaxis_title="Index",
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        st.plotly_chart(figrsi)


def srsi(start,end,df,mydict):
    period = st.number_input("Enter Term Period", min_value=1)
    period = int(period)
    if (period == None):
        st.error("Enter Valid Time Period")
        st.stop()
    else:

        data = smadata(start, end, df, mydict)
        sdata = pd.DataFrame(data[2])

        delta = sdata['Close'].diff(1)
        delta.dropna(inplace=True)
        positive = delta.copy()
        negative = delta.copy()
        positive[positive < 0] = 0
        negative[negative > 0] = 0

        avg_gain = positive.rolling(window=period).mean()

        avg_loss = abs(negative.rolling(window=period).mean())
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))
        strsi=(rsi-rsi.rolling(period).min())/(rsi.rolling(period).max()-rsi.rolling(period).min())
        combined = pd.DataFrame()
        combined['Close'] = sdata['Close']
        combined['Stochastic RSI'] = strsi
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=combined.index, y=combined['Close'], mode='lines', name='Close',
                                 line=dict(color="Silver", width=1)))
        fig.update_layout(
            width=800,
            height=500,
            paper_bgcolor="LightSteelBlue",
            title={
                'text': "Close Price",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis_title="Date",
            yaxis_title="Price",
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        st.plotly_chart(fig)
        figstrsi = go.Figure()
        figstrsi.add_trace(go.Scatter(x=combined.index, y=combined['Stochastic RSI'], mode='lines', name='Stochastic RSI',
                                    line=dict(color="Silver", width=1)))

        figstrsi.add_hline(y=0.8, line_dash="dash", line_color="fuchsia")

        figstrsi.add_hline(y=0.2, line_dash="dash", line_color="fuchsia")

        figstrsi.update_layout(
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            width=800,
            height=500,
            paper_bgcolor="LightSteelBlue",
            title={
                'text': "Stochastic Relative Strength Index",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis_title="Date",
            yaxis_title="Index",
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        st.plotly_chart(figstrsi)


def rcross(start, end, df, mydict):
    col1, col2 = st.columns(2)

    with col1:
        sw = st.number_input("Enter Short Term Period:", min_value=0)
        sw = int(sw)
    with col2:
        lw = st.number_input("Enter Long Term Period:", min_value=0)
        lw = int(lw)
    if (sw > lw):
        st.info("Short Term Period Should be less than Long Term Period")
    if(sw==0 and lw==0):
        st.error("Enter Valid Time Period")
        st.stop()
    else:
        result, assets, nodata = smadata(start, end, df, mydict)
        delta1 = nodata['Adj Close'].diff(1)
        delta2 = nodata['Adj Close'].diff(1)
        delta1.dropna(inplace=True)
        delta2.dropna(inplace=True)
        positive1 = delta1.copy()
        positive2 = delta2.copy()
        negative1 = delta1.copy()
        negative2 = delta2.copy()
        positive1[positive1 < 0] = 0
        positive2[positive2 < 0] = 0
        negative1[negative1 > 0] = 0
        negative2[negative2 > 0] = 0

        avg_gain1 = positive1.rolling(window=sw).mean()
        avg_gain2 = positive2.rolling(window=lw).mean()

        avg_loss1 = abs(negative1.rolling(window=sw).mean())
        avg_loss2 = abs(negative2.rolling(window=lw).mean())
        rs1 = avg_gain1 / avg_loss1
        rs2 = avg_gain2 / avg_loss2
        rsi1 = 100.0 - (100.0 / (1.0 + rs1))
        rsi2 = 100.0 - (100.0 / (1.0 + rs2))
        combined = pd.DataFrame()
        combined['Signal'] = 0.0
        combined['Adj Close'] = nodata['Adj Close']
        combined['Short Term RSI'] = rsi1
        combined['Long Term RSI'] = rsi2
        combined['Signal'] = np.where(combined['Short Term RSI'] > combined['Long Term RSI'], 1.0, 0.0)
        combined['Position'] = combined['Signal'].diff()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=combined.index, y=combined['Adj Close'], mode='lines', name='Adj Close',
                             line=dict(color="Silver", width=1)))
        fig.update_layout(
        width=800,
        height=500,
        paper_bgcolor="LightSteelBlue",
        title={
            'text': "Adj Close Price",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
            )
        )
        st.plotly_chart(fig)
        figcrsi = go.Figure()
        figcrsi.add_trace(go.Scatter(x=combined.index, y=combined['Short Term RSI'], mode='lines', name='Short Term RSI',
                                  line=dict(color="darkviolet", width=1)))
        figcrsi.add_trace(go.Scatter(x=combined.index, y=combined['Long Term RSI'], mode='lines', name='Long Term RSI',
                                  line=dict(color="lime", width=1)))
        figcrsi.add_trace(
        go.Scatter(x=combined[combined['Position'] == 1].index, y=combined['Short Term RSI'][combined['Position'] == 1],
                   mode='markers', name='Buy Signal', marker_symbol='triangle-up', marker_size=15,
                   line=dict(color="limegreen", width=1)))
        figcrsi.add_trace(
        go.Scatter(x=combined[combined['Position'] == -1].index, y=combined['Short Term RSI'][combined['Position'] == -1],
                   mode='markers', name='Sell Signal', marker_symbol='triangle-down', marker_size=15,
                   line=dict(color="firebrick", width=1)))

        figcrsi.update_layout(
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        width=800,
        height=500,
        paper_bgcolor="LightSteelBlue",
        title={
            'text': "Relative Strength Index Cross-Over",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Date",
        yaxis_title="Index",
        legend_title="",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
            )
        )
        st.plotly_chart(figcrsi)


def macd(start, end, df, mydict):

    col1, col2 = st.columns(2)

    with col1:
        sw = st.number_input("Enter Short Term Period:", value=12)
        sw = int(sw)
    with col2:
        lw = st.number_input("Enter Long Term Period:", value=26)
        lw = int(lw)
    if (sw > lw):
        st.info("Short Term Period Should be less than Long Term Period")
    if(sw==0 and lw==0):
        st.error("Enter Valid Time Period")
        st.stop()
    else:
        result, assets, nodata = smadata(start, end, df, mydict)
        mdf=pd.DataFrame(result)
        buy,sell=[],[]
        mdf['SEMA']=mdf.Close.ewm(span=sw).mean()
        mdf['lEMA']=mdf.Close.ewm(span=lw).mean()
        mdf['macd']=mdf.SEMA-mdf.lEMA
        mdf['signal']=mdf.macd.ewm(span=9).mean()
        for i in range(2, len(mdf)):
            if (mdf.macd.iloc[i] > mdf.signal.iloc[i] and mdf.macd.iloc[i - 1] < mdf.signal.iloc[i - 1]):
                buy.append(i)
            elif (mdf.macd.iloc[i] < mdf.signal.iloc[i] and mdf.macd.iloc[i - 1] > mdf.signal.iloc[i - 1]):
                sell.append(i)
        combined = pd.DataFrame()
        combined['Close'] = result['Close']
        combined['SEMA']=mdf['SEMA']
        combined['lEMA']=mdf['lEMA']
        combined['macd']= mdf['macd']
        combined['signal']= mdf['signal']

        figmacd = go.Figure()
        figmacd.add_trace(
            go.Scatter(x=mdf.index, y=mdf['signal'], mode='lines', name='Signal',
                       line=dict(color="dodgerblue", width=1)))
        figmacd.add_trace(go.Scatter(x=mdf.index, y=mdf['macd'], mode='lines', name='MACD',

                                     line=dict(color="lime", width=1)))
        figmacd2 = go.Figure()

        figmacd2.add_trace(
            go.Scatter(x=combined.index, y=combined['Close'], mode='lines', name='Close Price',
                       line=dict(color="dodgerblue", width=1)))



        figmacd2.add_trace(
           go.Scatter(x=mdf.iloc[buy].index,
                       y=combined.iloc[buy].Close,
                       mode='markers', name='Buy Signal', marker_symbol='triangle-up', marker_size=15,
                       line=dict(color="limegreen", width=1)))
        figmacd2.add_trace(
            go.Scatter(x=mdf.iloc[sell].index,
                       y=combined.iloc[sell].Close,
                       mode='markers', name='Sell Signal', marker_symbol='triangle-down', marker_size=15,
                       line=dict(color="firebrick", width=1)))



        figmacd.update_layout(
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            width=800,
            height=500,
            paper_bgcolor="LightSteelBlue",
            title={
                'text': "MACD & SIGNAL",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis_title="Date",
            yaxis_title="Index",
            legend_title="",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        figmacd2.update_layout(
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            width=800,
            height=500,
            paper_bgcolor="LightSteelBlue",
            title={
                'text': "Close Price",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis_title="Date",
            yaxis_title="Close Price",
            legend_title="",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        st.plotly_chart(figmacd)
        st.plotly_chart(figmacd2)


        return figmacd,figmacd2


def bolli(start, end, df, mydict):
    period = st.number_input("Enter Term Period", min_value=1)
    period = int(period)
    if (period == None):
        st.error("Enter Valid Time Period")
        st.stop()
    else:
        result, assets, nodata = smadata(start, end, df, mydict)
        buy,sell=[],[]
        result['sma']=result.Close.rolling(window=period).mean()
        result['stdev']=result.Close.rolling(window=period).std()
        result['upper']=result.sma+(result.stdev*2)
        result['lower']=result.sma-(result.stdev*2)
        bdf=pd.DataFrame()
        bdf['Close']=result['Close']
        bdf['upper']=result['upper']
        bdf['lower']=result['lower']
        bdf['sma']=result['sma']
        for i in range(len(result)):
            if(bdf['Close'][i]>bdf['upper'][i]):
                buy.append(np.nan)
                sell.append(bdf['Close'][i])
            elif(bdf['Close'][i]<bdf['lower'][i]):
                buy.append(bdf['Close'][i])
                sell.append(np.nan)

        bdf['buy_signal']=np.where(bdf.lower>bdf.Close,True,False)
        bdf['sell_signal']=np.where(bdf.upper<bdf.Close,True,False)

        combined = pd.DataFrame()
        combined['Close'] = bdf['Close']
        combined['SMA']=bdf['sma']
        combined['Upper']=bdf['upper']
        combined['Lower']=bdf['lower']
        combined['Buy_Signal']=bdf['buy_signal']
        combined['Sell_Signal']=bdf['sell_signal']

        figbolli = go.Figure()
        figbolli.add_trace(go.Scatter(x=combined.index, y=combined['Close'], mode='lines', name='Close',

                                      line=dict(color="Orange", width=1)))
        figbolli.add_trace(go.Scatter(x=combined.index, y=combined['SMA'], mode='lines', name='SMA',

                                     line=dict(color="lime", width=1)))
        figbolli.add_trace(go.Scatter(x=combined.index, y=combined['Upper'], mode='lines', name='Upper Band',fill='tonexty',
                         fillcolor='rgba(173,204,255,0.1)',

                                     line=dict(color="darkcyan", width=1)))
        figbolli.add_trace(go.Scatter(x=combined.index, y=combined['Lower'], mode='lines', name='Lower Band',fill='tonexty',
                         fillcolor='rgba(173,204,255,0.3)',

                                     line=dict(color="darkcyan", width=1)))

        figbolli.add_trace(
            go.Scatter(x=combined.index[combined.Buy_Signal],
                       y=combined[combined.Buy_Signal].Close,
                       mode='markers', name='Buy Signal', marker_symbol='triangle-up', marker_size=15,
                       line=dict(color="limegreen", width=1)))
        figbolli.add_trace(
            go.Scatter(x=combined.index[combined.Sell_Signal],
                       y=combined[combined.Sell_Signal].Close
                       ,
                       mode='markers', name='Sell Signal', marker_symbol='triangle-down', marker_size=15,
                       line=dict(color="firebrick", width=1)))

        figbolli.update_layout(
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            width=800,
            height=500,
            paper_bgcolor="LightSteelBlue",
            title={
                'text': "Close Price",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis_title="Date",
            yaxis_title="Close Price",
            legend_title="",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        st.plotly_chart(figbolli)





def tstrat(start, end, df, mydict):
    res = st.radio(label='Select a Trading Strategy', options=['Strategy', 'Simple Moving Average', 'RSI', 'Stochastic RSI','RSI CrossOver','MACD','Bollinger Bands'])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    if (res == 'Simple Moving Average'):
        hsma(start, end, df, mydict)

    elif (res == 'RSI'):
        rsi(start, end, df, mydict)

    elif (res == 'Stochastic RSI'):
        srsi(start,end,df,mydict)
    elif(res=='RSI CrossOver'):
        rcross(start,end,df,mydict)
    elif(res=='MACD'):
        macd(start,end,df,mydict)
    elif(res=='Bollinger Bands'):
        bolli(start,end,df,mydict)
    else:
        st.info('Select Any Method')


def plot(result, assets):
    name=assets[0]
    combined = pd.DataFrame()
    combined[['Close']] = result[['Close']]
    combined['Date']=result.index
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=combined['Date'], y=combined['Close'], mode='lines', name='Close',
                             line=dict(color="dodgerblue", width=1)))
    fig.add_trace(go.Scatter(x=combined['Date'], y=result['Short-Period MA'], mode='lines', name='Short-Period MA',
                             line=dict(color="lime", width=1)))
    fig.add_trace(go.Scatter(x=combined['Date'], y=result['Long-Period MA'], mode='lines', name='Long-Period MA',
                             line=dict(color="darkorange", width=1)))
    fig.add_trace(go.Scatter(x=result[result['Position'] == 1].index, y=result['Short-Period MA'][result['Position'] == 1], mode='marke'
                                                                                                                                 'rs', name='Buy Signal',marker_symbol='triangle-up',marker_size=15,
                             line=dict(color="limegreen", width=1)))
    fig.add_trace(
        go.Scatter(x=result[result['Position'] == -1].index, y=result['Short-Period MA'][result['Position'] == -1],
                   mode='markers', name='Sell Signal', marker_symbol='triangle-down', marker_size=15,
                   line=dict(color="firebrick", width=1)))
    fig.update_layout(
        width=800,
        height=500,
        paper_bgcolor="LightSteelBlue",
        title={
            'text': str(name)+" Close Price",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    st.plotly_chart(fig)

    return fig


def sma(sw, lw, result):
    if (sw or lw):
        # st.write(sw,lw)
        result['Short-Period MA'] = result['Close'].rolling(window=sw, min_periods=1).mean()
        result['Long-Period MA'] = result['Close'].rolling(window=lw, min_periods=1).mean()
        return result
    else:
        st.info("Enter Valid Time Period")
        st.stop()


def smadata(start, end, df, mydict):
    cnames = st.sidebar.multiselect("Select Company By Name", (df['Name']))
    assets = []
    if (cnames):
        for j in cnames:
            assets.append(mydict.get(j))
            assets.append(cnames)
            if (len(assets) >2):
                st.error("Only One Company Is Allowed")
                st.stop()
        for ticker in assets:
            try:
                data = web.DataReader(assets[0], 'yahoo', start, end)
            except:
                st.error("The Data Related To Select Company Does Not Exists! Select SomeOther Company")
                st.stop()
            data = pd.DataFrame(data)
            rdata = pd.DataFrame(data)
            data = data.drop(columns=['Volume', 'Adj Close'])


    else:

        st.error("Select A Company")
        st.stop()
    return data, assets, rdata


def portfolio(start, end, df, mydict):
    cnames = st.sidebar.multiselect("Select Company By Name", (df['Name']), default=(df['Name'][0]))
    assets = []
    nop = st.sidebar.number_input("Select No Of Portfolio's", min_value=50, max_value=25000)
    if (cnames == None):
        st.error("Select Atleast One Company")

    st.info('**PORTFOLIO BASED ON SELECTED COMPANIES**')

    if (cnames):

        for j in cnames:
            assets.append(mydict.get(j))

            portfolio_returns = []
            portfolio_weights = []
            portfolio_risk = []
            sharpe_ratios = []
            RF = 0
            returns = pd.DataFrame()

        for ticker in assets:
            data = web.DataReader(assets, 'yahoo', start, end)
            data = pd.DataFrame(data)
            data[assets] = data['Adj Close'].pct_change()
            if (returns.empty):
                returns = data[[ticker]]
            else:
                returns = returns.join(data[[ticker]], how='outer')
        for portfolio in range(nop):
            weights = np.random.random_sample(len(assets))
            weights = np.round((weights / np.sum(weights)), 3)
            portfolio_weights.append(weights)
        # Calculating Annualized Return
        annual_return = np.sum(returns.mean() * weights) * 252
        portfolio_returns.append(round(annual_return, 2))
        # Matrix Covariance & Portfolio Risk Calculation
        matrix_covaraince = returns.cov() * 252
        portfolio_varaince = np.dot(weights.T, (np.dot(matrix_covaraince, weights)))
        portfolio_stdev = np.sqrt(portfolio_varaince)
        portfolio_risk.append(round(portfolio_stdev, 2))
        # Sharpe Ratio
        sharpe_ratio = (annual_return - RF) / portfolio_stdev
        sharpe_ratios.append(round(sharpe_ratio, 2))
        simulations_data = [portfolio_returns, portfolio_risk, sharpe_ratios, portfolio_weights]
        simulations_df = pd.DataFrame(data=simulations_data).T
        simulations_df.columns = [
            'Returns',
            'Portfolio Risk',
            'Sharpe Ratios',
            'Portfolio Weights'
        ]
        simulations_df = simulations_df.infer_objects()
        max_sharpe_ratio = simulations_df.iloc[simulations_df['Sharpe Ratios'].astype(float).idxmax()]
        min_volatility = simulations_df.iloc[simulations_df['Portfolio Risk'].astype(float).idxmin()]
        max_return = simulations_df.iloc[simulations_df['Returns'].astype(float).idxmax()]

        colsmax = st.columns(len(max_return))
        colsmin = st.columns(len(min_volatility))
        header = ["PORTFOLIO RETURNS", "PORTFOLIO RISK", "Sharpe Ratios", "PORTFOLIO WEIGHTS", ]
        option = st.sidebar.selectbox("Select Risk Measure", (
        "", "MAXIMUM RETURN AVERAGE", "MINIMUM RISK AVERAGE", "EXPECTED EXCESS RETURN AVERAGE"))
        if (option == "MAXIMUM RETURN AVERAGE"):
            for i in range(0, len(max_return)):
                colsmax[i].header(header[i])
                colsmax[i].success(max_return[i])
        elif (option == "MINIMUM RISK AVERAGE"):
            for j in range(0, len(min_volatility)):
                colsmin[j].header(header[j])
                colsmin[j].success(min_volatility[j])
        elif (option == "EXPECTED EXCESS RETURN AVERAGE"):
            for k in range(0, len(max_sharpe_ratio)):
                colsmin[k].header(header[k])
                colsmin[k].success(max_sharpe_ratio[k])
        else:
            st.error("Kindly Select Any Measure")
        df2 = pd.DataFrame()
        for stock in assets:
            df2[stock] = web.DataReader(stock, data_source='yahoo', start=start, end=end)['Adj Close']
        pd.set_option("display.max_rows", None, "display.max_columns", None)


if __name__ == "__main__":
    main()
