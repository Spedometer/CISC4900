# Function retrieves data associated with user inputted Symbol and saves json to 'Files' directory.
# Data manipulation will be conducted using those files. 'Outputsize' argument will be
# implemented later to allow for Compact or Full data
#
# Also need to implement solution to prevent invalid entries from having .json files created
import json
import requests


def retrieve_by_symbol(symbol, api_key, default_dir):
    symbol = symbol.upper()
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
    outputsize = ""
    params = {'apikey': api_key, 'symbol': symbol, 'outputsize':outputsize}
    api_request = requests.get(url, params)
    api = json.loads(api_request.content)
    symbol_file_name = default_dir + '/' + symbol + '.json'
    with open(symbol_file_name, 'w') as json_file:
        json.dump(api, json_file)

# Below code used to test above.
# api_key = "XHVXGZR30PZIGH91"
# symbol = input("Enter Symbol to test: ")
# retrieve_by_symbol(symbol, api_key, "Files")
