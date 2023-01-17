#Kian Haghighi
import streamlit as st
from datetime import date
import yfinance as yf
import requests
import prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go 
import pandas as pd
from datetime import datetime, timedelta

start = "2015-01-01"
today = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

#stocks = ("AAPL", "GOOG", "MSFT", "GME")
#selected_stock = st.selectbox("Select ds", stocks)

#slider time for prediction(interactive part)
n_years = st.slider("Years of prediction: ", 1, 4)
period = n_years * 365

#load_data with alpha vantage
api_key = '9N1F7EYLZRR8K2KO' 
@st.cache
def load_data(ticker):
    data = yf.download(ticker, start, today)
    time_period = 'daily'
    data.reset_index(inplace=True)
    response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_{time_period.upper()}_ADJUSTED&symbol={ticker}&apikey={api_key}')
    #way to get a final row of data frame from json data that I got from alpha vantage?
    return response


@st.cache
def get_stock_data(ticker):
    #retrieve the stock data
    df = yf.Ticker(ticker).history(period="max")

    #set the 'Date' column as the index and reset the index
    df.reset_index(inplace=True)
    return df           

#add functions for animations
#1.stock visualization with TimeSeries data
#2.prediction visualization with TS
#3.animations of the data
#4.potential? -> twitter sentiment analysis

data_load_state = st.text("Load data...")
ticker = st.text_input("Enter the ticker symbol of the stock:")
if(st.button('Submit')):

    data = get_stock_data(ticker)  
    # code that uses the ticker symbol
    #the following line runs before the st.text_input is taken
    #therefore, i am going to change the function
    data_load_state.text("Loading data...done!")

    st.subheader('Raw data')
    #returns the last N rows of a dataframe to get the most
    #recent data points

    st.write(data.tail())

    #for testing purposes: test the dataframe acquired from get_stock_data

    def plot_raw_data():
        fig = go.Figure()      
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))      #Key error: Date(resolved)
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))    #Key error: Date(resolved)
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()


    #find predction for x next years with forecasting
    df_train = data[['Date', 'Close']]
    #look at propher documentation
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    #now apply a prophet to make forecasts
    model = prophet.Prophet()
    df_train["ds"] = pd.to_datetime(df_train["ds"])
    df_train["ds"] = df_train["ds"].dt.tz_localize(None)
    df_train.dropna(thresh=2, inplace=True)

    model.fit(df_train)             #change the parameters of this function so that it can use "df_train" without errors

    #df_train has less than 2 non-NaN rows, so I need to make df_train have at least 2 NaN rows
    #although the previous lines make the code run and I get the model, it raises the ValueError: Dataframe has less than 2 non-NaN rows
    #i seem to only get that error when I first run it

    #CORRECTION: the error seems to be that the get_stock_data() function is waiting for input, but the code keeps running,
    #as a result, I will make getting the stock data and displaying it into functions
    future = model.make_future_dataframe(periods=period)
    forecast = model.predict(future)

    st.subheader('Forecast data')
    st.write(forecast.tail())
    fig1 = plot_plotly(model, forecast)
    st.plotly_chart(fig1)

    st.write('Forecast components')
    fig2 = model.plot_components(forecast)
    st.write(fig2)