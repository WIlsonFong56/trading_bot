import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

def recur_inside(lows: list, highs: list, num: int) -> bool:
    '''
    Helper function returning whether the last number of datapoints in lows list
    and highs list are in ascending and descending order, respectively.

    :param lows: A list object consisting of data lows
    :param highs: A list object consisting of data highs
    :param num: An int object representing number of datapoints to check
    :return: A boolean object that is true only if the current low is lower than the next low
             and current high is higher than the next high.
    '''
    if num == 1:
        return True
    else:
        return lows[-num-1] < lows[-num] and highs[-num-1] > highs[-num] and \
               recur_inside(lows, highs, num-1)
    
def recur_ranging(lows: list, highs: list, num: int, std_dev=0.05: float) -> bool:
    '''
    Helper funciton returning whether the last number of candles are inside a range given
    by param std_dev.

    :param lows: A list object consisting of data lows
    :param highs: A list object consisting of data highs
    :param num: An int object representing number of datapoints to check
    :param std_dev: A float object representing standard deviation of range, can be changed
                    depending on volatility of stock
    :return: A boolean object that is true only if the current low is lower than or equal to
             the next low and current high is higher than or equal to the next high.
    '''
    if num == 1:
        return True
    else:
        return lows[-num-1]*(1-std_dev) <= lows[-num] and \
               highs[-num-1]*(1+std_dev) >= highs[-num] and \
               recur_inside(lows, highs, num-1, std_dev)

def volume_filter(volume=None: int or None, avg_or_daily=None: str or None) -> 'function':
    def stock_check(ticker: str) -> bool:
        '''
        Function returning whether the following stock volume criteria are met based on given
        parameters:
            If volume param or/and avg_or_daily param is/are None: Daily volume is greater than average volume.
            If volume param is given and avg_or_daily param is 'avg': Average volume is greater than given volume.
            If volume param is given and avg_or_daily param is 'daily': Daily volume is greater than given volume.

        :param volume: An int object representing user given stock volume
        :param ticker: A string object represeting a stock ticker
        :return: A boolean object that is true only if the volume criteria is met as given above
        '''
        stock = yf.Ticker(ticker)
        if volume is None or avg_or_daily is None:
            return stock.info['volume24Hr'] > stock.info['averageVolume']
        elif avg_or_daily == 'avg':
            return stock.info['averageVolume'] > volume
        elif avg_or_daily == 'daily':
            return stock.info['volume24Hr'] > volume
    return stock_check


def inside_range_filter(num: int, intervl='1d': str) -> 'function':
    def stock_check(ticker: str) -> bool:
        '''
        Function returning whether the stock's price range is getting tighter.

        :param num: An int object representing number of datapoints to check
        :param intervl: A string object representing the datapoint intervals
        :param ticker: A string object representing a stock ticker
        :return: A boolean object that is true only if the price range on the datapoints is contracting
        '''
        yf.pdr_override()
        data = pdr.get_data_yahoo(
                tickers = ticker,
                period = '1y',
                interval = intervl)
        highs_list = data.High.to_list()
        lows_list = data.Low.to_list()
        try:
            return recur_inside(lows_list, highs_list, num)
        except:
            print(f'{ticker}\'s data was unretrievable')
    return stock_check

def base(ticker: str, std_dev=0.05: float, intervl='1d': str) -> bool:
    '''
    Function returning whether the stock is forming a price base/bottom.

    :param ticker: A string object representing a stock ticker
    :param std_dev: A float object representing standard deviation of range, can be changed
                    depending on volatility of stock
    :param intervl: A string object representing the datapoint intervals
    :return: A boolean object that is true only if the prices on the datapoints is forming a base/bottom
    '''
    yf.pdr_override()
    data = pdr.get_data_yahoo(
        tickers = ticker,
        period = '1y',
        interval = intervl)
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
    except:
        print('Base not found')
    return found_base
