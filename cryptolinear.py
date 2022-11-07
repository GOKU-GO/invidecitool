import pandas as pd

import warnings

from datetime import timedelta

from sklearn.model_selection import train_test_split
warnings.filterwarnings('ignore')
pd.options.display.float_format = '${:,.2f}'.format
from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import streamlit as st





def linreg(start,end,df):
    #df = pdr.DataReader('ETH-INR', 'yahoo', start, end)
    cname="ETHEREUM "
    #Crypto_Dashboard.common_stat(df,cname)
    projection=st.sidebar.number_input("Projection Days",14)



    df['Prediction']=df[['Close']].shift(-projection)
    x=np.array(df[['Close']])
    x=x[:-projection]
    y=df['Prediction']
    y=y[:-projection]
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
    linReg=LinearRegression()
    linReg.fit(x_train,y_train)
    lin_reg_confidence=linReg.score(x_test,y_test)
    #st.header(lin_reg_confidence)
    x_projection=np.array(df[['Close']])[-projection:]

    linReg_prediction=linReg.predict(x_projection)

    #cols=st.beta_columns(2)
    df1=pd.DataFrame(x_projection)
    df2=pd.DataFrame(linReg_prediction)

    value=str(df2.iloc[-1:].to_string(index=False,header=False))
    value=value.replace('$', '')


    #cols[0].header("Actual Closing Price")
    #cols[0].write(df1)
    #cols[1].header("Predicted Closing Price")
    #cols[1].write(df2)
    edate=pd.to_datetime(end)
    enddate=edate+timedelta(days=projection)



    chart_data1 = pd.DataFrame(
    x_projection,
    columns=['Actual_Price'])
    st.header("Actual Closing Price")
    st.line_chart(chart_data1)


    chart_data2 = pd.DataFrame(
    linReg_prediction,
    columns=['Predicted_Price'])
    st.header("Predicted Closing Price")
    st.line_chart(chart_data2)

    st.write("The Closing Price after", projection, "days from", edate.date(), "to", enddate.date(), "=", value)

