import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss, arma_order_select_ic
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
from datetime import timedelta
import itertools


def init_sidebar():
    ticker = st.sidebar.text_input(label='Ticker', help="Any ticker from yahoo finance f.g. BTC-USD, ETH-USD, TSLA, NVDA etc.")
    ticker_start_date = st.sidebar.date_input(label='Start Date', value=None)
    ticker_end_date = st.sidebar.date_input(label='End Date', value=None)

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


def adf_test(dataset, lags): 
    try:
        df_test = adfuller(dataset, maxlag=lags, autolag=None)
        st.write("Results of ADF Test:")
        st.write("1. Test Statistic : ", df_test[0])
        st.write("2. P-Value : ", df_test[1])
        st.write("3. Number of Lags : ", df_test[2])
        st.write("4. Critical Values : ")
        for key, val in df_test[4].items():
            st.write(key, ": ", val)
        return df_test[1]
    except:
        st.warning("An error occurred while performing the ADF test.")
        return None
    

def kpss_test(dataset, lags):
    try:
        df_test = kpss(dataset, nlags=lags, regression='c')
        st.write("Results of KPSS Test:")
        st.write("1. Test Statistic : ", df_test[0])
        st.write("2. P-Value : ", df_test[1])
        st.write("3. Number of Lags : ", df_test[2])
        st.write("4. Critical Values : ")
        try:
            df_test[3].pop("2.5%")
        except:
            e = None
        for key, val in df_test[3].items():
            st.write(key, ": ", val)
        return df_test[1]
    except:
        st.warning("An error occurred while performing the KPSS test.")
        return None


def check_stationarity(dataset):
    st.subheader("Check For Stationarity")
    significance_level = 0.05
    dataset_copy = dataset.copy()
    is_stationary = False
    iterations = 0
    while not is_stationary and iterations < 5:
        st.write("Iteration ", iterations + 1)
        st.write(dataset_copy)
        lags = arma_order_select_ic(dataset_copy['Adj Close'].dropna(), ic='aic', trend='c')['aic_min_order'][0]
        #st.write(arma_order_select_ic(dataset_copy['Adj Close'].dropna(), ic='aic', trend='c'))
        adf_stationarity, kpss_stationarity = None, None
        adf_col, kpss_col = st.columns(2)
        with adf_col:
            adf_p_value = adf_test(dataset_copy['Adj Close'].dropna(), lags)
            if adf_p_value is not None:
                if adf_p_value < significance_level:
                    st.write("Based upon the p-value of ADF test of ", round(adf_p_value, ndigits=4), " < ", significance_level, " significance level, the null hypothesis can be rejected.")
                    st.write("The Series is Stationary.")
                    adf_stationarity = True
                    st.write("")
                else:
                    st.write("Based upon the p-value of ADF test of ", round(adf_p_value, ndigits=4), " > ", significance_level, " significance level, the null hypothesis can not be rejected.")
                    st.write("The Series is Non-Stationary.")
                    adf_stationarity = False
                    st.write("")
        with kpss_col:
            kpss_p_value = kpss_test(dataset_copy['Adj Close'].dropna(), lags)
            if kpss_p_value is not None:
                if kpss_p_value < significance_level:
                    st.write("Based upon the p-value of KPSS test of ", round(kpss_p_value, ndigits=4), " < ", significance_level, " significance level, the null hypothesis can be rejected.")
                    st.write("The Series is Non-Stationary.")
                    kpss_stationarity = False
                    st.write("")
                else:
                    st.write("Based upon the p-value of KPSS test of ", round(kpss_p_value, ndigits=4), " > ", significance_level, " significance level, the null hypothesis can not be rejected.")
                    st.write("The Series is Stationary.")
                    kpss_stationarity = True
                    st.write("")
        st.write("CONCLUSION")
        st.write("")
        if adf_stationarity is True and kpss_stationarity is True:
            st.write("Both tests conclude that the series is stationary. The series is stationary.")
            is_stationary = True
        elif adf_stationarity is True and kpss_stationarity is False:
            st.write("ADF indicates stationarity and KPSS indicates non-stationarity. The series is difference stationary. Differencing is to be used to make series stationary. The differenced series is checked for stationarity.")
            dataset_copy['Adj Close'] = dataset_copy['Adj Close'].diff().dropna()
        elif adf_stationarity is False and kpss_stationarity is True:
            st.write("ADF indicates non-stationarity and KPSS indicates stationarity. The series is trend stationary. Trend needs to be removed to make series strict stationary. The detrended series is checked for stationarity.")
            dataset_copy['Adj Close'] = (dataset_copy['Adj Close'] - dataset_copy['Adj Close'].shift(1)).dropna()
        else:
            st.write("Both tests conclude that the series is not stationary. The series is not stationary.")
            dataset_copy['Adj Close'] = dataset_copy['Adj Close'].diff().dropna()
        dataset_copy = dataset_copy.dropna()
        iterations += 1
        st.write("")
        st.write("")
        st.write("")
    return dataset, dataset_copy, is_stationary


def choose_model(dataset):
    try:
        st.write("Figure out order for ARIMA Model...")
        st.write("Performing stepwise search to minimize AIC...")
        st.write("Best model found:")
        model = auto_arima(dataset['Adj Close'])
        st.write(model)
        st.write("")
        st.write("")
        st.write("")
        return model
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
        title='Actual VS Predicted Differenced Adj Close',
        xaxis_title='Date',
        yaxis_title='Adj Close',
        legend_title='Legend'
    )
    st.plotly_chart(fig)


def test_model(dataset, chosen_model):
    try:
        fifth = dataset.shape[0] // 5
        train = dataset.iloc[:-fifth]
        test = dataset.iloc[-fifth:]
        model = ARIMA(train['Adj Close'], order=chosen_model.get_params()["order"])
        model = model.fit()
        st.write("Predictions on Test Set")
        start = len(train)
        end = len(train) + len(test) - 1
        pred = model.predict(start=start, end=end, typ='levels')
        pred.index = dataset.index[start:end+1]
        left_col, right_col = st.columns([0.4, 0.6])
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


def forecast(dataset, chosen_model):
    try:
        model = ARIMA(dataset['Adj Close'], order=chosen_model.get_params()["order"])
        model = model.fit()
        st.write("Forecast")
        start = dataset.index[-1]
        end = start + timedelta(days=20)
        index_future_dates = pd.date_range(start=start, end=end)
        pred = model.predict(start=len(dataset), end=len(dataset)+20, typ='levels').rename("ARIMA Predictions")
        pred.index = index_future_dates
        left_col, right_col = st.columns([0.4, 0.6])
        with left_col:
            st.write(pred)
        with right_col:
            forecast_chart(data=dataset, prediction=pred)
    except:
        st.warning("An error occurred while forecasting the data.")


def get_news(ticker):
    try:
        st.header(f"News of {ticker}")
        search = yf.Tickers(tickers=ticker)
        for i in range(5):
            st.subheader(search.news()[ticker][i]["title"])
            st.write("Publisher: ", search.news()[ticker][i]["publisher"])
            st.write(search.news()[ticker][i]["link"])
            st.write("")
    except:
        st.warning("Could not load news about ", ticker)


def arima_selection(data, split=0.8):
    p = [0,1,2,3,4,5]
    d = [0,1,2,3]
    q = [0,1,2,3,4,5]
    combs = list(itertools.product(p,d,q))
    limit = int(len(data) * split)
    train = data[:limit]
    test = data[limit:]
    start = len(train)
    end = len(train) + len(test) - 1
    rmse = None
    best_model = None
    best_order = None
    best_pred = None
    best_rmse = 10000000
    for i in combs:
        try:
            model = ARIMA(train['Adj Close'], order=i)
            output = model.fit()
            pred = output.predict(start=start, end=end, typ='levels')
            pred.index = data.index[start:end+1]
            rmse = mean_squared_error(test['Adj Close'], pred)**0.5
            if rmse < best_rmse:
                best_order = i
                best_rmse = rmse
                best_model = output
                best_pred = pred
        except:
            continue
    if rmse == None:
        return None
    else:
        return best_model, best_order, best_pred, test
    

def arima_selection_versus_chart(test, best_pred):
    left_col, right_col = st.columns([0.4, 0.6])
    with left_col:
        st.write(best_pred.rename("differenced_series"))
    with right_col:
        versus_chart(test_data=test, prediction=best_pred)


def arima_selection_loading_text(best_order):
    st.write("Performing search to find the best model...")
    st.write("Figure out order for ARIMA Model...")
    st.write("Best model found:")
    st.write("ARIMA", best_order)
    st.write("")
    st.write("")
    st.write("")


def forecast_with_arima_selection(data, best_order):
    try:
        model = ARIMA(data['Adj Close'], order=best_order)
        output = model.fit()
        st.write("FORECAST")
        start = data.index[-1]
        end = start + timedelta(days=14)
        index_future_dates = pd.date_range(start=start, end=end)
        pred = output.predict(start=len(data), end=len(data)+14, typ='levels').rename("ARIMA Predictions")
        pred.index = index_future_dates
        left_col, right_col = st.columns([0.4, 0.6])
        with left_col:
            st.write(pred)
        with right_col:
            forecast_chart(data=data, prediction=pred)
    except:
        st.warning("An error occurred while forecasting the data.")

