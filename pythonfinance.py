import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import csv
from pandas_datareader import data as pdr
from stock_filters import *

yf.pdr_override()

if __name__ == '__main__':

    stocks_list = [] 
    return_list = []
    
    with open('stocks.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if len(line[0]) <= 4 and line[0].isalpha() and int(line[8]) > 5000000:
                stocks_list.append(line[0])
        csv_file.close()
    
    month_or_week = input('Month or week: ')
    num = int(input('Enter # of months or weeks: '))
    
    
    if month_or_week.upper() == 'WEEK' or month_or_week.upper() == 'W':
        stock_filter = inside_week_filter(num)
                
    elif month_or_week.upper() == 'MONTH' or month_or_week.upper() == 'M':
        stock_filter = inside_month_filter(num)

    for stock in stocks_list:
        if stock_filter(stock):
            return_list.append(stock)

    print(f'{num} inside {month_or_week} list')
    for item in return_list:
        print(item)
