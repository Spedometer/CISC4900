import pandas as pd
import global_variables as gv
from tkinter import *
import standard_deviation as sd


# Function creates panda dataframe
def create_user_list_outputbox_dataframe(symbol_request, open_average, high_average, low_average, close_average,
                                         volume_average):

    temp_dataframe = pd.DataFrame({'Symbol': [symbol_request],
                                   'Open Avg': [open_average],
                                   'High Avg': [high_average],
                                   'Low Avg': [low_average],
                                   'Close Avg': [close_average],
                                   'Volume Avg': [volume_average]})

    if symbol_request in str(gv.master_dataframe.values):
        print("Symbol is already in list")  # to be output later to dialog box, used during testing
    else:
        gv.master_dataframe = gv.master_dataframe.append(temp_dataframe, ignore_index=True)
        # gv.master_dataframe.sort_values('Symbol', inplace=True)

    gv.user_list_outputbox.delete(*gv.user_list_outputbox.get_children())
    gv.user_list_outputbox["column"] = list(gv.master_dataframe.columns)
    gv.outputbox["show"] = "headings"

    gv.user_list_outputbox.column("#0", width=20, stretch=NO)
    gv.user_list_outputbox.column("Symbol", anchor=W, width=50)
    gv.user_list_outputbox.column("Open Avg", anchor=E, width=75)
    gv.user_list_outputbox.column("High Avg", anchor=E, width=75)
    gv.user_list_outputbox.column("Low Avg", anchor=E, width=75)
    gv.user_list_outputbox.column("Close Avg", anchor=E, width=75)
    gv.user_list_outputbox.column("Volume Avg", anchor=E, width=75)
    gv.user_list_outputbox.heading("#0", text="", anchor=E)

    for column in gv.user_list_outputbox["columns"]:
        gv.user_list_outputbox.heading(column, text=column, anchor=E)
    gv.user_list_outputbox.heading("Symbol", anchor=W)

    df_rows = gv.master_dataframe.to_numpy().tolist()

    for row in df_rows:
        gv.user_list_outputbox.insert("", "end", values=row)


# Used to refresh data, like when a symbol is removed from list
def refresh_user_list_outputbox_dataframe():
    gv.user_list_outputbox.delete(*gv.user_list_outputbox.get_children())
    gv.user_list_outputbox["column"] = list(gv.master_dataframe.columns)
    gv.outputbox["show"] = "headings"

    gv.user_list_outputbox.column("#0", width=20, stretch=NO)
    gv.user_list_outputbox.column("Symbol", anchor=W, width=50)
    gv.user_list_outputbox.column("Open Avg", anchor=E, width=75)
    gv.user_list_outputbox.column("High Avg", anchor=E, width=75)
    gv.user_list_outputbox.column("Low Avg", anchor=E, width=75)
    gv.user_list_outputbox.column("Close Avg", anchor=E, width=75)
    gv.user_list_outputbox.column("Volume Avg", anchor=E, width=75)
    gv.user_list_outputbox.heading("#0", text="", anchor=E)

    for column in gv.user_list_outputbox["columns"]:
        gv.user_list_outputbox.heading(column, text=column, anchor=E)
    gv.user_list_outputbox.heading("Symbol", anchor=W)

    df_rows = gv.master_dataframe.to_numpy().tolist()

    for row in df_rows:
        gv.user_list_outputbox.insert("", "end", values=row)


# Due to nested key value pairs with dictionaries and dates appearing as header, iterated through dates
# to form a list to later be appended as first column of data_df (modified data dataframe)
def create_outputbox1_dataframe(symbol, period):
    gv.outputbox.delete(*gv.outputbox.get_children())
    # gv.outputbox["column"] = ["Date", "Open", "High", "Low", "Close", "Volume", "Deviation", "DevSq", "StdDev"]
    gv.outputbox["column"] = ["Date", "Open", "High", "Low", "Close", "Volume", "Moving Avg", "Deviation"]
    gv.outputbox["show"] = "headings"

    gv.outputbox.column("#0", width=20, stretch=NO)
    gv.outputbox.column("Date", anchor=W, width=75)
    gv.outputbox.column("Open", anchor=E, width=100)
    gv.outputbox.column("High", anchor=E, width=100)
    gv.outputbox.column("Low", anchor=E, width=100)
    gv.outputbox.column("Close", anchor=E, width=100)
    gv.outputbox.column("Volume", anchor=E, width=100)
    gv.outputbox.column("Moving Avg", anchor=E, width=100)
    gv.outputbox.column("Deviation", anchor=E, width=100)
    # gv.outputbox.column("Deviation", anchor=E, width=75)
    # gv.outputbox.column("DevSq", anchor=E, width=75)
    # gv.outputbox.column("StdDev", anchor=E, width=75)

    selected_symbol_index = gv.user_input_list.index(symbol)

    date_list = []
    for entry in gv.master_datapoint_list[selected_symbol_index].symbol_json["Time Series (Daily)"]:
        date_list.append(entry)

    data_list = []
    for date in date_list:
        try:
            data_list.append(gv.master_datapoint_list[selected_symbol_index].symbol_json["Time Series (Daily)"][date])
        except Exception as e:
            gv.dialog_text['text'] = "Date append to data error"

    data_df = pd.DataFrame(data_list)
    data_df.insert(0, "Date", date_list, True)

    # dev_list, dev_squared_list, standard_dev_list = sd.calculate_std(period)
    # data_df.insert(len(data_df.columns), "Deviation", dev_list, True)
    # data_df.insert(len(data_df.columns), "DevSq", dev_squared_list, True)
    # data_df.insert(len(data_df.columns), "StdDev", standard_dev_list, True)

    # global moving_averages_list, deviation_list
    moving_averages_list, deviation_list = sd.calculate_moving_averages()
    data_df.insert(len(data_df.columns), "Moving Averages", moving_averages_list, True)
    data_df.insert(len(data_df.columns), "Deviation", deviation_list, True)

    for column in gv.outputbox["columns"]:
        gv.outputbox.heading(column, text=column, anchor=E)
    gv.outputbox.heading("Date", anchor=W)

    df_rows = data_df.to_numpy().tolist()

    for row in df_rows:
        gv.outputbox.insert("", "end", values=row)
