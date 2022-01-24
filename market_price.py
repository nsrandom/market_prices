"""Stocks and options pricing API"""

import datetime
import sys

from fastapi import FastAPI, HTTPException
from typing import List, Optional
from wallstreet import Stock, Call, Put

app = FastAPI()

# Returns a stock's info
@app.get("/stock/{ticker}")
async def stock(ticker: str):
    stock = get_stock(ticker)
    return {
        "symbol": stock.ticker,
        "price": stock.price
    }


# Returns a stock's price
@app.get("/stock/{ticker}/price")
async def stock_price(ticker: str):
    return get_stock(ticker).price


# Returns an option's info
@app.get("/option/{ticker}/{option_type}/{strike}/{expiry}")
async def option(ticker: str, option_type: str, strike:float, expiry:str):
    option = get_option(ticker, option_type, strike, expiry)
    return {
        "symbol": option.ticker,
        "expiry": expiry,
        "type": option_type,
        "strike": strike,
        "price": option.price
    }


# Returns an option's price
@app.get("/option/{ticker}/{option_type}/{strike}/{expiry}/price")
async def option_price(ticker: str, option_type: str, strike:float, expiry:str):
    return get_option(ticker, option_type, strike, expiry).price


# Returns prices for a list of tickers
# Each ticker must either be:
#   - a single "<symbol>", eg: "GOOG", for stocks.
#   - an option ticker in the following format, "<symbol> <yyyy-mm-dd> <strike> <type>", eg: "NET 2023-01-20 100 C"
# Results format is: [<ticker>, <price>]
#   - Price will be in string format.
#   - If ticker was invalid, price will be "NA"
@app.get("/prices")
async def prices(tickers: str):
    prices = []
    tickers = tickers.split(",")
    for ticker in tickers:
        ticker = ticker.strip()
        try:
            if " " in ticker:  # Parse as option
                optdata = ticker.split()
                if len(optdata) == 4:
                    # Format is "<symbol> <yyyy-mm-dd> <strike> <type>"
                    option = get_option(optdata[0], optdata[3], float(optdata[2]), optdata[1])
                    prices.append([ticker, '%.2f' % option.price])
                else:
                    raise ValueError("Invalid option format: " + ticker)
            else:  # Parse as stock
                stock = get_stock(ticker)
                prices.append([ticker, '%.2f' % stock.price])

        except Exception as e:
            print(e)
            prices.append([ticker, "NA"])

    return prices

def get_stock(ticker: str):
    try:
        return Stock(ticker)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Stock not found! => {}".format(sys.exc_info())) from e

def get_option(ticker: str, option_type: str, strike:float, expiry:str):
    option_type = option_type.lower()
    try:
        date = datetime.datetime.strptime(expiry, '%Y-%m-%d')
        if option_type == 'call' or option_type == 'c':
            return Call(ticker, d=date.day, m=date.month, y=date.year, strike=strike)
        if option_type == 'put'  or option_type == 'p':
            return Put(ticker, d=date.day, m=date.month, y=date.year, strike=strike)
        raise HTTPException(status_code=404, detail="Invalid query! Only Call or Put supported!")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Option not found! => {}".format(sys.exc_info())) from e
