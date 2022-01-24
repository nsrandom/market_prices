## Setup

pipenv install

pipenv run uvicorn market_price:app [--reload]

## API

/docs (auto generated)

/stock/\<symbol>

/stock/\<symbol>/price

/option/\<symbol>/\<option_type>/\<strike>/\<expiry>

/option/\<symbol>/\<option_type>/\<strike>/\<expiry>/price

/prices?tickers=A,B,C
