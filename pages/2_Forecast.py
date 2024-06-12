import streamlit as st
from stocknews import StockNews

from authentication.auth import get_authenticator
from pages_funcs.forecast_funcs import init_sidebar, download_data, ticker_chart, setup_data, check_stationarity, choose_model, test_model, forecast

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
    check_stationarity(initial_data)
    best_model = choose_model(initial_data)
    test_model(dataset=initial_data, chosen_model=best_model)
    forecast(dataset=initial_data, chosen_model=best_model)

with news_tab:
    st.header(f"News of {ticker}")
    sn = StockNews(stocks=ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(5):
        st.subheader(f"News {i+1}")
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f"Title Sentiment {title_sentiment}")
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f"News Sentiment {news_sentiment}")
