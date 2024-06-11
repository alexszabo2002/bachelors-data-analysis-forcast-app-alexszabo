import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
from datetime import timedelta


def init_sidebar():

    ticker = st.sidebar.text_input('Ticker')
    ticker_start_date = st.sidebar.date_input('Start Date')
    ticker_end_date = st.sidebar.date_input('End Date')

    return ticker, ticker_start_date, ticker_end_date


def download_data(ticker, ticker_start_date, ticker_end_date):

    if ticker and ticker_start_date and ticker_end_date:
        try:
            downloaded_data = yf.download(tickers=ticker, start=ticker_start_date, end=ticker_end_date)
            return downloaded_data
        except:
            st.error("Could not download data for the given ticker and date range.")
            st.stop()
    else:
        st.warning("Please provide a ticker and date range.")
        st.stop()


def ticker_chart(ticker_data, ticker):

    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ticker_data.index, y=ticker_data['Adj Close'], mode='lines', name='Adj Close'))
        fig.update_layout(
            title=ticker,
            xaxis_title='Date',
            yaxis_title='Adj Close'
        )
        st.plotly_chart(fig)
    except:
        st.warning("Could not plot the chart for the given data.")


def setup_data(data):

    try:
        df = pd.DataFrame(data)
        df = df.dropna()
        return df
    except:
        st.warning("An error occurred while preparing the data.")
        st.stop()


def adf_test(dataset):
    
    try:
        df_test = adfuller(dataset, autolag='AIC')
        st.write("1. ADF : ", df_test[0])
        st.write("2. P-Value : ", df_test[1])
        st.write("3. Number of Lags : ", df_test[2])
        st.write("4. Number of Observations used for ADF Regression and Critical Values calculation : ", df_test[3])
        st.write("5. Critical Values : ")
        for key, val in df_test[4].items():
            st.write(key, ": ", val)
        return df_test[1]
    except:
        st.warning("An error occurred while performing the ADF test.")
        return None


def check_stationarity(dataset):

    st.write("Check For Stationarity")
    p_value = adf_test(dataset['Adj Close'])
    if p_value is not None:
        if p_value < 0.05:
            st.write("The Series is Stationary")
            st.write("")
            st.write("")
            st.write("")
        else:
            st.write("The Series is NOT Stationary")
            st.write("")
            st.write("")
            st.write("")


def choose_model(dataset):

    try:
        st.write("Figure out order for ARIMA Model...")
        st.write("Performing stepwise search to minimize AIC...")
        st.write("Best model found:")
        stepwise_fit = auto_arima(dataset['Adj Close'], trace=True, suppress_warnings=True)
        st.write(stepwise_fit)
        st.write("")
        st.write("")
        st.write("")
        return stepwise_fit
    except:
        st.warning("Could not find a model for the forecast.")
        return None


def model_summary(model):

    if model is not None:
        st.write(model.summary())
    else:
        st.warning("There is no model to summary.")


def versus_chart(test_data, prediction):

    test_data_copy = test_data.copy()
    test_data_copy['Prediction'] = prediction
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=test_data_copy.index, y=test_data_copy['Adj Close'], mode='lines', name='Actual'))
    fig.add_trace(go.Scatter(x=test_data_copy.index, y=test_data_copy['Prediction'], mode='lines', name='Predicted'))
    fig.update_layout(
        title='Actual VS Predicted Adj Close',
        xaxis_title='Date',
        yaxis_title='Adj Close',
        legend_title='Legend'
    )
    st.plotly_chart(fig)


def test_model(dataset):

    try:
        fifth = dataset.shape[0] // 5
        train = dataset.iloc[:-fifth]
        test = dataset.iloc[-fifth:]
        model = ARIMA(train['Adj Close'], order=(1,0,0))
        model = model.fit()
        st.write("Predictions on Test Set")
        start = len(train)
        end = len(train) + len(test) - 1
        pred = model.predict(start=start, end=end, type='levels')
        pred.index = dataset.index[start:end+1]
        left_col, right_col = st.columns(2)
        with left_col:
            st.write(pred)
        with right_col:
            versus_chart(test_data=test, prediction=pred)
        rmse = sqrt(mean_squared_error(pred, test['Adj Close']))
        st.write("RMSE: ", rmse)
        st.write("")
    except:
        st.warning("An error occurred while testing the model.")


def forecast_chart(data, prediction):

    data_copy = data.copy()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_copy.index, y=data_copy['Adj Close'], mode='lines', name='Past'))
    fig.add_trace(go.Scatter(x=prediction.index, y=prediction, mode='lines', name='Forecast'))
    fig.update_layout(
        title='Forecast Adj Close',
        xaxis_title='Date',
        yaxis_title='Adj Close',
        legend_title='Legend'
    )
    st.plotly_chart(fig)


def forecast(dataset):

    try:
        model = ARIMA(dataset['Adj Close'], order=(1,0,0))
        model = model.fit()
        st.write("Forecast")
        start = dataset.index[-1]
        end = start + timedelta(days=10)
        index_future_dates = pd.date_range(start=start, end=end)
        pred = model.predict(start=len(dataset), end=len(dataset)+10, type='levels').rename("ARIMA Predictions")
        pred.index = index_future_dates
        left_col, right_col = st.columns(2)
        with left_col:
            st.write(pred)
        with right_col:
            forecast_chart(data=dataset, prediction=pred)
    except:
        st.warning("An error occurred while forecasting the data.")

