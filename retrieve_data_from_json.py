# Function will 'retrieve_data_from_api.retrieve_by_symbol(symbol, api_key, default_dir) function
# before returning values once data has been processed
#
# Current outputs are placeholders, intent is to past a Table with values to outputbox label
from tkinter import *
import json
import retrieve_data_from_api as rd
import pandas as pd
import global_variables as gv
import create_pandas_table


def retrieve_from_json(symbol_request, outputbox, api_key, default_dir, mid_right_top_frame, name_input):
    title = "Time Series (Daily)"
    symbol_request = symbol_request.upper()
    open_total = 0
    close_total = 0
    high_total = 0
    low_total = 0
    volume_total = 0
    count = 0

    try:
        combined_file_name = default_dir + '/' + symbol_request + '.json'
        rd.retrieve_by_symbol(symbol_request, api_key, default_dir)
        with open(combined_file_name) as symbol_json:
            data = json.load(symbol_json)

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
            volume_total += float(volume)
            count += 1

        open_average = round((open_total / count),2)
        high_average = round((high_total / count),2)
        low_average = round((low_total / count), 2)
        close_average = round((close_total / count), 2)
        volume_average = round((volume_total / count), 2)


        try:
            create_pandas_table.create_update_table(symbol_request, open_average,
                                                high_average, low_average, close_average, volume_average, outputbox)
        except Exception as e:
            print("create panda function error")

        # Label(mid_right_top_frame,
        #                      text=('%s\t%s\t%s\t%s\t\t%s\t%s\n' % (symbol_request, open_average, high_average,
        #                                                            low_average, close_average,
        #                                                            volume_average)), justify=LEFT).pack()
        name_input.delete(0, END)

    except Exception as e:
        outputbox['text'] = "Stock Symbol: " + symbol_request + " not found."
        name_input.delete(0, END)
        return

# Test code below
# retrieve_from_json()
