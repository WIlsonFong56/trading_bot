import yfinance as yf
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
    
def recur_ranging(lows: list, highs: list, num: int, dev: float) -> bool:
    '''
    Helper funciton returning whether the last number of candles are inside a range given
    by param dev.

    :param lows: A list object consisting of data lows
    :param highs: A list object consisting of data highs
    :param num: An int object representing number of datapoints to check
    :param dev: A float object representing the deviation of range, can be changed
                    depending on volatility of stock
    :return: A boolean object that is true only if the current low is lower than or equal to
             the next low and current high is higher than or equal to the next high.
    '''
    if num == 1:
        return True
    else:
        return lows[-num-1]*(1-dev) <= lows[-num] and \
               highs[-num-1]*(1+dev) >= highs[-num] and \
               recur_inside(lows, highs, num-1, dev)

def volume_filter(volume:int or None=None , avg_or_daily:str or None=None) -> 'function':
    def stock_check(ticker: str) -> bool:
        '''
        Function returning whether the following stock volume criteria are met based on given
        parameters:
            If volume param or/and avg_or_daily param is/are None: Daily volume is greater than average volume.
            If volume param is given and avg_or_daily param is 'avg': Average volume is greater than given volume.
            If volume param is given and avg_or_daily param is 'daily': Daily volume is greater than given volume.

        :param volume: An int object representing user given stock volume, or None
        :param avg_or_daily: A string object that allows the user to use either the average or daily volume
                             to compare to given volume
        :param ticker: A string object represeting a stock ticker
        :return: A boolean object that is true only if the volume criteria is met as given above
        '''
        stock = yf.Ticker(ticker)
        if volume is None or avg_or_daily is None:
            return stock.info['volume24Hr'] > stock.info['averageVolume']
        elif avg_or_daily.upper() in 'AVG AVERAGE':
            return stock.info['averageVolume'] > volume
        elif avg_or_daily.upper() == 'DAILY':
            return stock.info['volume24Hr'] > volume
    return stock_check


def inside_range_filter(num: int, intervl: str, inside_or_range: str, dev: float=0.0) -> 'function':
    def stock_check(ticker: str) -> bool:
        '''
        Function returning whether the stock's price action is getting tighter or is ranging based on
        input of param inside_or_range.

        :param num: An int object representing number of datapoints to check
        :param intervl: A string object representing the datapoint intervals
        :param inside_or_range: A string object deciding which algorithm to use.
        :param dev: A float object representing the deviation of range, can be changed
                        depending on volatility of stock
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
            if inside_or_range.upper() == 'INSIDE':
                return recur_inside(lows_list, highs_list, num)
            elif inside_or_range.upper() == 'RANGE':
                return recur_ranging(lows_list, highs_list, num, dev)
        except:
            print(f'{ticker}\'s data was unretrievable')
    return stock_check

def base_filter(dev: float, intervl: str) -> bool:
    def stock_check(ticker: str) -> bool:
        '''
        Function returning whether the stock is forming a price base/bottom.

        :param dev: A float object representing the deviation of range, can be changed
                        depending on volatility of stock
        :param intervl: A string object representing the datapoint intervals
        :param ticker: A string object representing a stock ticker
        :return: A boolean object that is true only if the prices on the datapoints is forming a base/bottom
        '''
        yf.pdr_override()
        data = pdr.get_data_yahoo(
            tickers = ticker,
            period = '1y',
            interval = intervl)
        close_list = data.Close.to_list()
        high = close_list[-1]*(1+dev)
        low = close_list[-1]*(1-dev)
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
            return found_base
        except:
            print('Base not found')
    return stock_check
