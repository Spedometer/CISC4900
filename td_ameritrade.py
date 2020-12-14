from tda import auth, client
from tda.orders.equities import equity_buy_limit
from tda.orders.common import Duration, Session

import datetime
import pickle
import requests
import json
import td_config as td
import global_variables as gv


def refresh_token():
    url = "https://api.tdameritrade.com/v1/oauth2/token"
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': creds['refresh_token'],
        'access_type': 'offline',
        'client_id': td.api_key,
        'redirect_uri': td.redirect_uri
    }
    new_creds = requests.post(url, data=data)
    new_creds_data = json.loads(new_creds.content)
    # print("New Creds Response", new_creds_data)
    with open(td.token_path, 'wb') as token:
        pickle.dump(new_creds_data, token)


def get_account_information():
    bearer_header = "Bearer " + creds['access_token']
    accounts_endpoint = "https://api.tdameritrade.com/v1/accounts"
    param = {'fields': 'orders'}
    header = {'Authorization': bearer_header}
    accounts_response = requests.get(accounts_endpoint, params=param, headers=header)
    # print("Before renew:", accounts_response)

    if accounts_response.status_code == 401:
        refresh_token()
        accounts_response = requests.get(accounts_endpoint, params=param, headers=header)
        # print("After renew:", accounts_response)

    data = json.loads(accounts_response.content)
    return data


def get_orders_information():
    bearer_header = "Bearer " + creds['access_token']
    orders_endpoint = "https://api.tdameritrade.com/v1/orders"
    param = {
        'accountId': accounts_data[0]['securitiesAccount']['accountId'],
        'maxResults': "",
        'fromEnteredTime': "",
        'toEnteredTime': "",
        'status': ""
    }
    header = {'Authorization': bearer_header}
    orders_response = requests.get(orders_endpoint, params=param, headers=header)
    # print("Orders Response Code:", orders_response)

    data = json.loads(orders_response.content)
    return data


def get_orders_history():
    bearer_header = "Bearer " + creds['access_token']
    accountId = accounts_data[0]['securitiesAccount']['accountId']
    orders_history_endpoint = f"https://api.tdameritrade.com/v1/accounts/{accountId}/transactions"
    param = {
        'type': '',
        'symbol': '',
        'startDate': '',
        'endDate': ''
    }
    header = {'Authorization': bearer_header}
    orders_history_response = requests.get(orders_history_endpoint, params=param, headers=header)
    # print("Order History Response Code:", orders_history_response)

    data = json.loads(orders_history_response.content)
    return data


def place_buy_order(symbol, quantity, live_quote):
    bearer_header = "Bearer " + creds['access_token']
    accountId = accounts_data[0]['securitiesAccount']['accountId']
    place_order_endpoint = f"https://api.tdameritrade.com/v1/accounts/{accountId}/orders"
    buy_order_info = {
        "orderStrategyType": "OCO",
        "childOrderStrategies": [
            {
                "orderType": "LIMIT",
                "session": "NORMAL",
                "price": live_quote,
                "duration": "DAY",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "BUY",
                        "quantity": quantity,
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "EQUITY"
                        }
                    }
                ]
            },
            {
                "orderType": "STOP_LIMIT",
                "session": "NORMAL",
                "price": live_quote,
                "stopPrice": live_quote,
                "duration": "DAY",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "BUY",
                        "quantity": quantity,
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "EQUITY"
                        }
                    }
                ]
            }
        ]
    }
    header = {'Authorization': bearer_header}
    # PURPOSELY DISABLED
    # place_buy_order_response = requests.post(place_buy_order_endpoint, data=buy_order_info, headers=header)
    # data = json.loads(place_order_response.content)
    #return data
    price = "${:,.2f}".format(quantity * live_quote)
    gv.dialog_text['text'] = f"Mock buy order of {symbol} for a quantity of {quantity} for {price} submitted."


def place_sell_order(symbol, quantity, live_quote):
    bearer_header = "Bearer " + creds['access_token']
    accountId = accounts_data[0]['securitiesAccount']['accountId']
    place_order_endpoint = f"https://api.tdameritrade.com/v1/accounts/{accountId}/orders"
    sell_order_info = {
        "orderStrategyType": "OCO",
        "childOrderStrategies": [
            {
                "orderType": "LIMIT",
                "session": "NORMAL",
                "price": live_quote,
                "duration": "DAY",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "SELL",
                        "quantity": quantity,
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "EQUITY"
                        }
                    }
                ]
            },
            {
                "orderType": "STOP_LIMIT",
                "session": "NORMAL",
                "price": live_quote,
                "stopPrice": live_quote,
                "duration": "DAY",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "SELL",
                        "quantity": quantity,
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "EQUITY"
                        }
                    }
                ]
            }
        ]
    }
    header = {'Authorization': bearer_header}
    # PURPOSELY DISABLED
    # place_sell_order_response = requests.post(place_order_endpoint, data=sell_order_info, headers=header)
    # data = json.loads(place_sell_order_response.content)
    #return data
    price = "${:,.2f}".format(quantity * live_quote)
    gv.dialog_text['text'] = f"Mock sell order of {symbol} for a quantity of {quantity} for {price} submitted."


def cancel_order():
    bearer_header = "Bearer " + creds['access_token']
    accountId = accounts_data[0]['securitiesAccount']['accountId']
    orderId = "MOCK ORDER ID: 4114522"
    cancel_orders_endpoint = f"https://api.tdameritrade.com/v1/accounts/{accountId}/orders/{orderId}"
    header = {'Authorization': bearer_header}
    cancel_order_response = requests.delete(cancel_orders_endpoint, headers=header)
    # PURPOSELY DISABLED
    # data = json.loads(cancel_order_response.content)
    # return data
    gv.dialog_text['text'] = f"Mock order: {orderId} cancelled"


def get_quote(symbol):
    bearer_header = "Bearer " + creds['access_token']
    get_quote_endpoint = f"https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes"
    param = {
        'apikey': td.api_key
    }
    header = {'Authorization': bearer_header}
    get_quote_response = requests.get(get_quote_endpoint, params=param, headers=header)
    # print("Get Quote", get_quote_response)

    data = json.loads(get_quote_response.content)
    return data


try:
    c = auth.client_from_token_file(td.token_path, td.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path="CISC4900/Files/chromedriver.exe") as driver:
        c = auth.client_from_login_flow(
            driver, td.api_key, td.redirect_uri, td.token_path)

with open(td.token_path, 'rb') as token:
    creds = pickle.load(token)

# Start session with newly refreshed token
refresh_token()

# Testing use of time to auto-refresh token once it reaches 29 minute mark out of 30
current_time_minus_minute = datetime.datetime.now() - datetime.timedelta(minutes=1)
current_time_in_epoch = int(current_time_minus_minute.timestamp() * 1000)
refresh_token_expire_time = current_time_in_epoch - creds['refresh_token_expires_in']


# print("current time in epoch", current_time_in_epoch)
# print("expire time in epoch", creds['refresh_token_expires_in'])
# print("refresh_token_expire_time", refresh_token_expire_time)


# in GUI main, loop time check to see if token has exceeded expire time, leave if 401 error block in code as backup
# print("Current Time:", int(datetime.datetime.now().timestamp()) * 1000)
# continuously loop to obtain current time in GUI to compare against expire time -1 minute

accounts_data = get_account_information()
orders_data = get_orders_information()
orders_history_data = get_orders_history()

# get_quote_data = get_quote(symbol)
#print(json.dumps(get_quote_data, indent=4))

