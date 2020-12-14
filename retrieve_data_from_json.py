# Function will 'retrieve_data_from_api.retrieve_by_symbol(symbol, api_key, default_dir) function
# before returning values once data has been processed
#
# Current outputs are placeholders, intent is to past a Table with values to outputbox label
from tkinter import *
import retrieve_data_from_api as rd
import global_variables as gv
import create_pandas_dataframe


# Used to create container for symbol and data retrieved from Alpha Vantage
# Trying to avoid saving .json hard copies onto hard drive
# Attempt to create one massive variable failed with Memory Errors once 5000+ copies was exceeded in tests
class AddSymbolData:
    def __init__(self, symbol, symbol_json):
        self.symbol = symbol
        self.symbol_json = symbol_json


# Function calculates averages of the open, high, low, close, and volume from json retrieved from api call
def retrieve_from_json(symbol_request, name_input):
    gv.dialog_text['text'] = ""
    title = "Time Series (Daily)"
    symbol_request = symbol_request.upper()
    open_total = 0
    close_total = 0
    high_total = 0
    low_total = 0
    volume_total = 0
    count = 0

    # Exit function if symbol_request is blank
    if symbol_request == "":
        gv.dialog_text['text'] = "No Symbol has been entered."
        return

    # Commented lines were from previous version where data was stored locally on hard drive
    # combined_file_name = gv.default_dir + '/' + symbol_request + '.json'
    # rd.retrieve_by_symbol(symbol_request)
    # with open(combined_file_name) as symbol_json:
    #     data = json.load(symbol_json)

    # If symbol entered by user is a duplicate, exit function
    if symbol_request in str(gv.master_dataframe.values):
        gv.dialog_text['text'] = "Symbol is already in list"
        name_input.delete(0, END)
        return

    data = rd.retrieve_by_symbol(symbol_request)

    try:
        if "Invalid API call" in data['Error Message']:
            gv.dialog_text['text'] = "Invalid Symbol - Please Try Again"
            name_input.delete(0, END)
            data.clear()
            return
    except KeyError:
        pass

    # Adding symbol to user's symbol list
    gv.user_input_list.append(symbol_request)

    # Adding object containing symbol + json data retrieved from API to master datapoint list
    gv.master_datapoint_list.append(AddSymbolData(symbol_request, data))

    for entry in data[title]:
        open_price = data[title][entry]["1. open"]
        high_price = data[title][entry]["2. high"]
        low_price = data[title][entry]["3. low"]
        close_price = data[title][entry]["4. close"]
        volume = data[title][entry]["5. volume"]
        open_total += float(open_price)
        high_total += float(high_price)
        low_total += float(low_price)
        close_total += float(close_price)
        volume_total += int(volume)
        count += 1

    open_average = format(open_total / count, '.4f')
    high_average = format(high_total / count, '.4f')
    low_average = format(low_total / count, '.4f')
    close_average = format(close_total / count, '.4f')
    volume_average = (volume_total // count)

    gv.total_count = count

    create_pandas_dataframe.create_user_list_outputbox_dataframe(symbol_request, open_average,
                                                                 high_average, low_average, close_average,
                                                                 volume_average)

    name_input.delete(0, END)
