# Binance Stop Loss Alert
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MIT License](https://img.shields.io/github/license/StephanAkkerman/Binance_Stop_Loss_Alert.svg?color=brightgreen)](https://opensource.org/licenses/MIT)

---

## Setup
- Clone this repository.
- Fill in the your API keys in `src/binance_keys.py`
- EXTRA: If you are planning on using Futures, make sure these are enabled in Binance API management
- Follow the link in binance_keys.py to get your Telegram bot and its keys
- Run `$ python src/main.py`
- See result

## When does it send a message?
If a sell order has been filled that is not a market sell order, the user socket will notice this and sends a message via Telegram.
So it works for Limit, Stop Limit and OCO.

## Dependencies
The required packages to run this code can be found in the `requirements.txt` file. To run this file, execute the following code block:
```
$ pip install -r requirements.txt 
```
Alternatively, you can install the required packages manually like this:
```
$ pip install <package>
```

## Note
This works for all Binance trading platforms, except isolated margin.
