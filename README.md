## Setup

pipenv install

pipenv run uvicorn market_price:app [--reload]

pipenv run gunicorn --daemon --bind 127.0.0.1:3041 market_price:app -w 4 -k uvicorn.workers.UvicornWorker

## API

/docs (auto generated)

/stock/\<symbol>

/stock/\<symbol>/price

/option/\<symbol>/\<option_type>/\<strike>/\<expiry>

/option/\<symbol>/\<option_type>/\<strike>/\<expiry>/price

/prices?tickers=A,B,C
