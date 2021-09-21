# Setup
1. Fill in the your API keys in binance_keys.py file
2. If you are planning on using Futures, make sure these are enabled in Binance API management
3. Follow the link in binance_keys.py to get your Telegram bot and its keys

# Note
This works for all Binance trading platforms, except isolated margin.

# When does it send a message
If a sell order has been filled that is not a market sell order, the user socket will notice this and sends a message via Telegram.
So it works for Limit, Stop Limit and OCO.
