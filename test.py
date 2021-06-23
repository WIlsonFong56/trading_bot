import yfinance as yf
import pandas as pd
import pickle as pk

df = pd.read_csv('stocks.csv')

tickers = df['Symbol'].values.tolist()

