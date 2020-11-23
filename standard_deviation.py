import global_variables as gv
import math
from tkinter import *


# Based calculations on information from: https://www.investopedia.com/terms/s/standarddeviation.asp
# Extracted data from multiple for loops, needed average of Close prices first before reiterating through Time Series
# to get deviation from average and square of that deviation. Reiterating a third time based on a default period
# of 10 entries (will be able to be chosen by user) to conclude with Standard Deviation value
def calculate_std(outputbox, period):
    gv.std_dev_outputbox.delete(*gv.std_dev_outputbox.get_children())

    try:
        current_item = outputbox.item(outputbox.focus())
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

    gv.std_dev_outputbox["column"] = ["Date", "Deviation", "Dev Squared", "Standard Dev"]
    gv.std_dev_outputbox["show"] = "headings"

    gv.std_dev_outputbox.column("Date", anchor=CENTER, width=100)
    gv.std_dev_outputbox.column("Deviation", anchor=CENTER, width=100)
    gv.std_dev_outputbox.column("Dev Squared", anchor=CENTER, width=100)
    gv.std_dev_outputbox.column("Standard Dev", anchor=CENTER, width=100)

    for column in gv.std_dev_outputbox["columns"]:
        gv.std_dev_outputbox.heading(column, text=column, anchor=CENTER)

    for index in range(0, len(dates_list)):
        gv.std_dev_outputbox.insert(parent='', iid=index, index='end', values=(dates_list[index], deviation_list[index],
                                                                               deviation_squared_list[index],
                                                                               final_std_deviation_list[index]))
