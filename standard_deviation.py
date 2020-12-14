import global_variables as gv
import math
from tkinter import *


# Based calculations on information from: https://www.investopedia.com/terms/s/standarddeviation.asp
# Extracted data from multiple for loops, needed average of Close prices first before reiterating through Time Series
# to get deviation from average and square of that deviation. Reiterating a third time based on a default period
# of 10 entries (will be able to be chosen by user) to conclude with Standard Deviation value
def calculate_std(period):
    # gv.std_dev_outputbox.delete(*gv.std_dev_outputbox.get_children())

    try:
        current_item = gv.user_list_outputbox.item(gv.user_list_outputbox.focus())
        symbol = current_item['values'][0]
    except IndexError:
        print("No symbol selected")
        return

    total = 0
    count = 0

    dates_list = []
    deviation_list = []
    deviation_squared_list =[]

    selected_symbol_index = gv.user_input_list.index(symbol)
    for date in gv.master_datapoint_list[selected_symbol_index].symbol_json["Time Series (Daily)"]:
        total = total + float(gv.master_datapoint_list[selected_symbol_index].symbol_json["Time Series (Daily)"]
                              [date]["4. close"])
        dates_list.append(date)
        count += 1

    deviation_average = float(total/count)

    for date in gv.master_datapoint_list[selected_symbol_index].symbol_json["Time Series (Daily)"]:
        close_value = gv.master_datapoint_list[selected_symbol_index].symbol_json["Time Series (Daily)"][date]["4. close"]
        deviation = format(float(close_value) - deviation_average, '.2f')
        deviation_squared = format(float(deviation) * float(deviation), '.2f')
        deviation_list.append(deviation)
        deviation_squared_list.append(deviation_squared)

    final_std_deviation_list = []

    period_count = 0
    period_total = 0

    for entry in deviation_squared_list:
        period_total = period_total + float(entry)
        period_count += 1
        if period_count != 0 and period_count % 10 == 0:
            final_std_deviation_list.append(format(math.sqrt(period_total / period_count), '.2f'))
        else:
            final_std_deviation_list.append(" ")

    return deviation_list, deviation_squared_list, final_std_deviation_list


def calculate_moving_averages():
    gv.std_dev_outputbox.delete(*gv.std_dev_outputbox.get_children())

    try:
        current_item = gv.user_list_outputbox.item(gv.user_list_outputbox.focus())
        symbol = current_item['values'][0]
    except IndexError:
        print("No symbol selected")
        return

    period = 10
    sum = 0

    moving_avg_list = []
    deviation_list = []
    close_price_list = []

    for i in range(0, period-1):
        moving_avg_list.append("")
        deviation_list.append("")

    selected_symbol_index = gv.user_input_list.index(symbol)
    for date in gv.master_datapoint_list[selected_symbol_index].symbol_json["Time Series (Daily)"]:
        close_price_list.append(gv.master_datapoint_list[selected_symbol_index].symbol_json["Time Series (Daily)"]
                                [date]["4. close"])

    # print("Close Price List:", close_price_list)

    index_counter, count, sum, average, last_close_price, deviation = 0, 0, 0, 0, 0, 0

    for price in close_price_list:
        index_counter += 1
        if index_counter <= len(close_price_list) - 9:
            sum = 0
            count = 0
            for entry in close_price_list[index_counter - 1: index_counter + 9]:
                entry = float(entry)
                sum += entry
                count += 1
                last_close_price = entry
            average = sum/count
            deviation = last_close_price - average
            moving_avg_list.append('{0:.4f}'.format(average))
            deviation_list.append('{0:.4f}'.format(deviation))

    gv.moving_avg_datapoint_list.append([symbol, moving_avg_list[period], deviation_list[period]])
    remove_duplicates = []
    [remove_duplicates.append(x) for x in gv.moving_avg_datapoint_list if x not in remove_duplicates]
    gv.moving_avg_datapoint_list = remove_duplicates
    # print("Updated list:", gv.moving_avg_datapoint_list)

    return moving_avg_list, deviation_list







