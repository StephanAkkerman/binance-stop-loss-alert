#!/usr/bin/env python3

from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import datetime
import json
import requests
import threading

# Keep all private stuff in another file called binance_keys.py
import binance_keys

# Max 1200 requests per minute; 10 orders per second; 100,000 orders per 24hrs
public_key = binance_keys.public_key
private_key = binance_keys.private_key

# Telegram bot
bot_token = binance_keys.bot_token
send_to = binance_keys.send_to

# This will contain the symbols that have been sent the last minute
sent = []

def sendSellAlert(bot_message):
    """ 
    Sending message via Telegram 
    @param bot_message: string including the text that the telegram account should receive
    """

    tijd = datetime.datetime.now().strftime("%H:%M:%S")
    pMsg = bot_message.replace("%25", "%")  # For displaying in console
    print(" ".join([pMsg, "at", tijd]))

    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + send_to
        + "&parse_mode=HTML&text="
        + bot_message
    )
    response = requests.get(send_text)

def clearSent():
    """ Removes symbol from sent list """
    sent.pop(0)

def userInfo(info_string, stream_buffer_name=False):
    """ Getting user data, through ubwa_user, sends a message if an asset has been sold except for market orders """
    
    try:
        # Convert info from string to dict
        info = json.loads(info_string)
        operation = info.get("e")

        # Other operations are balanceUpdate and outboundAccountInfo
        if operation == "executionReport":

            # Get all the usefull information out of info
            sym = info.get("s")  # ie 'YFIUSDT'
            side = info.get("S")  # ie 'BUY', 'SELL'
            orderType = info.get("o")  # ie 'LIMIT', 'MARKET', 'STOP_LOSS_LIMIT'
            execType = info.get("x")  # ie 'TRADE', 'NEW' or 'CANCELLED'
            execPrice = info.get("L")  # The latest price it was filled at

            # Remove from symbol_dict if it is sold
            if execType == "TRADE":
                if side == "SELL":

                    print("Sold " + sym)

                    # Send a message if it is not a market order
                    if orderType != "MARKET":
                        if sym not in sent:
                            msgPrice = round(float(execPrice), 4)
                            msg = " ".join([orderType, "sold", sym, "$" + str(msgPrice)])
                            sendSellAlert(msg)
                            sent.append(sym)

                            # Remove after 60 sec
                            threading.Timer(60.0, clearSent).start()

    except Exception  as e:
        print(e)
        print("Error in userInfo")

if __name__ == "__main__":

    # Start the sockets
    print("Starting at " + datetime.datetime.now().strftime("%H:%M:%S"))

    try:
        # Start the sockets, binance.com
        spot_user = BinanceWebSocketApiManager(process_stream_data=userInfo)
        spot_user.create_stream(
            "arr", "!userData", api_key=public_key, api_secret=private_key
        )
    
        # Margin
        margin_user = BinanceWebSocketApiManager(process_stream_data=userInfo, exchange="binance.com-margin")
        margin_user.create_stream(
            "arr", "!userData", api_key=public_key, api_secret=private_key
        )

        # Isolated Margin 
        # ONLY WORKS FOR 1 SYMBOL
        #iso_margin_user = BinanceWebSocketApiManager(process_stream_data=userInfo, exchange="binance.com-isolated_margin")
        #iso_margin_user.create_stream(
        #    "arr", "!userData", api_key=public_key, api_secret=private_key, symbol = "btcusdt"
        #)

        # USD-M Futures
        usd_futures_user = BinanceWebSocketApiManager(process_stream_data=userInfo, exchange="binance.com-futures")
        usd_futures_user.create_stream(
            "arr", "!userData", api_key=public_key, api_secret=private_key
        )

        # Coin-M Futures
        coin_futures_user = BinanceWebSocketApiManager(process_stream_data=userInfo, exchange="binance.com-coin-futures")
        coin_futures_user.create_stream(
            "arr", "!userData", api_key=public_key, api_secret=private_key
        )

    except Exception as e:
        print(e)
        print("Error with sockets")

# Maybe restart every 24h https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api/unicorn_binance_websocket_api.html?highlight=replace_stream#unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager.BinanceWebSocketApiManager.replace_stream