import streamlit as st
import yfinance as yf
import plotly.express as px
from stocknews import StockNews

from authentication.auth import get_authenticator

authenticator = get_authenticator()

st.markdown("# Plotting Demo")

ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

if ticker and start_date and end_date:
    data = yf.download(tickers=ticker, start=start_date, end=end_date)
    if not data.empty:
        fig = px.line(data_frame=data, x=data.index, y=data['Adj Close'], title=ticker)
        st.plotly_chart(fig)

        pricing_data, fundamental_data, news_data = st.tabs(['Pricing Data', 'Fundamental Data', 'Top News'])

        with pricing_data:
            st.header("Price Movements")
            st.write(data)

        #with fundamental_data:

        with news_data:
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
    else:
        st.write("No data available for the given ticker and date range.")
else:
    st.write("Please provide a ticker and date range.")
