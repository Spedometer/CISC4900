import pandas as pd
import global_variables as gv
from tkinter import *


# Function creates panda dataframe
def create_outputbox1_dataframe(symbol_request, open_average, high_average, low_average, close_average,
                                volume_average, outputbox):

    temp_dataframe = pd.DataFrame({'Symbol': [symbol_request],
                                   'Open Avg': [open_average],
                                   'High Avg': [high_average],
                                   'Low Avg': [low_average],
                                   'Close Avg': [close_average],
                                   'Volume Avg': [volume_average]})

    if symbol_request in str(gv.master_dataframe.values):
        print("Symbol is already in list")  # to be output later to dialog box
    else:
        gv.master_dataframe = gv.master_dataframe.append(temp_dataframe, ignore_index=True)
        # gv.master_dataframe.sort_values('Symbol', inplace=True)

    outputbox.delete(*outputbox.get_children())
    outputbox["column"] = list(gv.master_dataframe.columns)
    outputbox["show"] = "headings"

    outputbox.column("#0", width=20, stretch=NO)
    outputbox.column("Symbol", anchor=CENTER, width=100)
    outputbox.column("Open Avg", anchor=CENTER, width=140)
    outputbox.column("High Avg", anchor=CENTER, width=140)
    outputbox.column("Low Avg", anchor=CENTER, width=140)
    outputbox.column("Close Avg", anchor=CENTER, width=140)
    outputbox.column("Volume Avg", anchor=CENTER, width=140)
    outputbox.heading("#0", text="", anchor=CENTER)

    for column in outputbox["columns"]:
        outputbox.heading(column, text=column, anchor=CENTER)

    df_rows = gv.master_dataframe.to_numpy().tolist()

    for row in df_rows:
        outputbox.insert("", "end", values=row)


# Due to nested key value pairs with dictionaries and dates appearing as header, iterated through dates
# to form a list to later be appended as first column of data_df (modified data dataframe)
def create_outputbox2_dataframe(symbol):
    gv.outputbox2.delete(*gv.outputbox2.get_children())
    gv.outputbox2["column"] = ["Date", "Open", "High", "Low", "Close", "Volume"]
    gv.outputbox2["show"] = "headings"

    gv.outputbox2.column("#0", width=20, stretch=NO)
    gv.outputbox2.column("Date", anchor=CENTER, width=100)
    gv.outputbox2.column("Open", anchor=CENTER, width=140)
    gv.outputbox2.column("High", anchor=CENTER, width=140)
    gv.outputbox2.column("Low", anchor=CENTER, width=140)
    gv.outputbox2.column("Close", anchor=CENTER, width=140)
    gv.outputbox2.column("Volume", anchor=CENTER, width=140)

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

    for column in gv.outputbox2["columns"]:
        gv.outputbox2.heading(column, text=column, anchor=CENTER)

    df_rows = data_df.to_numpy().tolist()

    for row in df_rows:
        gv.outputbox2.insert("", "end", values=row)
