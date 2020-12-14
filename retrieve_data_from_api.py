# Function retrieves data associated with user inputted Symbol and saves json to 'Files' directory.
# Data manipulation will be conducted using those files. 'Outputsize' argument will be
# implemented later to allow for Compact or Full data
#
# Also need to implement solution to prevent invalid entries from having .json files created
import json
import requests
import global_variables as gv


# Commented lines were from previous version where data from API was copied to hard drive
def retrieve_by_symbol(symbol):
    symbol = symbol.upper()
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
    outputsize = "compact"
    params = {'apikey': gv.api_key, 'symbol': symbol, 'outputsize': outputsize}

    try:
        api_request = requests.get(url, params)
    except Exception as e:
        gv.dialog_text['text'] = "Issue with API key and/or parameters."
        return

    api = json.loads(api_request.content)

    # symbol_file_name = gv.default_dir + '/' + symbol + '.json'
    # with open(symbol_file_name, 'w') as json_file:
    #     json.dump(api, json_file)

    return api

# Below code used to test above.
# api_key = "XHVXGZR30PZIGH91"
# symbol = input("Enter Symbol to test: ")
# retrieve_by_symbol(symbol, api_key, "Files")
