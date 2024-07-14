import streamlit as st

from authentication.auth import get_authenticator
from pages_funcs.forecast_funcs import init_sidebar, download_data, ticker_chart, setup_data, check_stationarity, choose_model, test_model, forecast, get_news
from pages_funcs.forecast_funcs import arima_selection, arima_selection_loading_text, arima_selection_versus_chart, forecast_with_arima_selection

authenticator = get_authenticator()

st.markdown("# Forecast")

ticker, ticker_start_date, ticker_end_date = init_sidebar()

downloaded_data = download_data(ticker, ticker_start_date, ticker_end_date)

ticker_data_tab, forecast_tab, news_tab = st.tabs(["Ticker Data", "Forecast", "Top News"])

with ticker_data_tab:
    ticker_chart(downloaded_data, ticker)
    st.dataframe(data=downloaded_data, use_container_width=True)

with forecast_tab:
    initial_data = setup_data(downloaded_data)
    initial_data, stationary_data, is_stationary = check_stationarity(initial_data)
    #best_model = choose_model(stationary_data)
    #test_model(dataset=stationary_data, chosen_model=best_model)
    #forecast(dataset=stationary_data, chosen_model=best_model)
    best_model, best_order, best_pred, test = arima_selection(stationary_data)
    arima_selection_loading_text(best_order)
    arima_selection_versus_chart(test, best_pred)
    forecast_with_arima_selection(initial_data, best_order)

with news_tab:
    get_news(ticker)
