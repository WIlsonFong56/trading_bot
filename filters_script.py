import yfinance as yf
import csv
from pandas_datareader import data as pdr
from stock_filters import *

if __name__ == '__main__':

    stocks_list = []
    return_list = []
    filters_list = []

    tickers = input('List tickers to search, each seperated by one space(Default is all): ')

    if len(tickers) == 0:
        with open('stocks.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                stocks_list.append(line[0])
            csv_file.close()
    else:
        stocks_list = tickers.split()

    chosen_filter = input('Filter(s): ')

    if 'VOLUME' in chosen_filter.upper():

        volume = input("Enter desired volume (Leave empty if looking for relative): ")
        avg_or_daily = input("Comparing to average or daily volume? (Leave empty if looking for relative): ")
        
        if len(volume) == 0 or len(avg_or_daily) == 0:
            volume_filt = volume_filter()
        else:
            volume_filt = volume_filter(int(volume), avg_or_daily)

        filters_list.append(volume_filt)

    if 'INSIDE' in chosen_filter.upper() or 'RANGE' in chosen_filter.upper():
        
        num = int(input('Enter # of inside datapoints: '))
        intervl = input('Enter interval of datapoints(1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo): ')
        inside_or_range = input('Inside or ranging candles? ')
        if inside_or_range.upper() == 'RANGING':
            dev = float(input('Enter deviation (ie. 0.05, 0.25): '))
            inside_range_filt = inside_range_filter(num, intervl, inside_or_range, dev)
        else:
            inside_range_filt = inside_range_filter(num, intervl, inside_or_range)

        filters_list.append(inside_range_filt)

    if 'BASE' in chosen_filter.upper():

        dev = float(input('Enter deviation for base(ie. 0.05, 0.25): '))
        intervl = input('Enter interval of datapoints(1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo): ')
        base_filt = base_filter(dev, intervl)

        filters_list.append(base_filt)

    
    for stock in stocks_list:
        passed_all_filters = True
        for filt in filters_list:
            if not filt(stock):
                passed_all_filters = False
        if passed_all_filters:
            return_list.append(stock)        

    for stock in return_list:
        print(stock)

