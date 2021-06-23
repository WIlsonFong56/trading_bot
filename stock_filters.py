import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

def recur_inside(lows: list, highs: list, num: int) -> bool:
    if num == 1:
        return True
    else:
        return lows[-num-1] < lows[-num] and highs[-num-1] > highs[-num] and \
               recur_inside(lows, highs, num-1)

def volume_filter(volume: int) -> 'function':
    def stock_check(ticker: str) -> bool:
        stock = yf.Ticker(ticker)
        return stock.info['averageVolume'] > volume
    return stock_check

def inside_week_filter(weeks: int) -> 'function':
    def stock_check(ticker: str) -> bool:
        yf.pdr_override()
        data = pdr.get_data_yahoo(
                tickers = ticker,
                period = 'ytd',
                interval = '1wk')
        highs_list = data.High.to_list()
        lows_list = data.Low.to_list()
        try:
            return recur_inside(lows_list, highs_list, weeks)
        except:
            print(f'{ticker}\'s data was unretrievable')
    return stock_check

def inside_month_filter(months: int) -> 'function':
    def stock_check(ticker: str) -> bool:
        yf.pdr_override()
        data = pdr.get_data_yahoo(
                tickers = ticker,
                period = 'ytd',
                interval = '1mo')
        highs_list = data.High.to_list()
        lows_list = data.Low.to_list()
        try:
            return recur_inside(lows_list, highs_list, months)
        except:
            print('f{ticker}\'s data was unretrievable')
    return stock_check

def daily_base(ticker: str, std_dev=0.05: float) -> bool:
    yf.pdr_override()
    data = pdr.get_data_yahoo(
        tickers = ticker,
        period = 'ytd',
        interval = '1d')
    close_list = data.Close.to_list()
    high = close_list[-1]*(1+std_dev)
    low = close_list[-1]*(1-std_dev)
    found_intersect = False
    found_base = False
    index = -2
    try:
        while not found_intersect:
            if close_list[index] <= high and close_list[index] >= low:
                found_intersect = True
                found_base = True
            elif close_list[index] > high:
                found_intersect = True
            index -= 1
