"""Stocks and options pricing API"""

import datetime
import hug

from wallstreet import Stock, Call, Put
from urllib.error import HTTPError
from falcon import HTTP_400

@hug.get('/stock/{ticker}', output=hug.output_format.json)
def stock_price(ticker: str):
    stock = get_stock(ticker)
    if stock:
        return {
            "symbol": stock.ticker,
            "price": stock.price
        }
    else:
        raise HTTPError(url, 404, "Stock not found")

@hug.get('/option/{ticker}/{option_type}/{strike}/{expiry}', response, output=hug.output_format.json)
def option_price(ticker: str, option_type: str, strike:hug.types.number, expiry:str):
    option = get_option(ticker, option_type, strike, expiry)
    if option:
        return {
            "symbol": option.ticker,
            "expiry": expiry,
            "type": option_type,
            "strike": strike,
            "price": option.price
        }
    else:
        response.status = HTTP_400


def get_stock(ticker: str):
    try:
        stock = Stock(ticker)
        return stock
    except:
        return None

def get_option(ticker: str, option_type: str, strike:hug.types.number, expiry:str):
    try:
        date = datetime.datetime.strptime(expiry, '%Y-%m-%d')
        if option_type == 'Call':
            return Call(ticker, d=date.day, m=date.month, y=date.year, strike=strike)
        if option_type == 'Put':
            return Put(ticker, d=expiry.date, m=expiry.month, y=expiry.year, strike=strike)
        
        return None
    except:
        return None
