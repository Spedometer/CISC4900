import json
import pandas as pd
import global_variables as gv
import numpy

def create_update_table(symbol_request, open_average, high_average, low_average, close_average,
                        volume_average, outputbox):

    temp_dataframe = pd.DataFrame({'Symbol': [symbol_request],
                                   'Open Avg': [open_average],
                                   'High Avg': [high_average],
                                   'Low Avg': [low_average],
                                   'Close Avg': [close_average],
                                   'Volume Avg': [volume_average]})


    if not symbol_request in gv.master_dataframe.values:
        gv.master_dataframe = gv.master_dataframe.append(temp_dataframe, ignore_index=True)
    else:
        print("Symbol is already in list")   # to be output later to dialog box

    gv.master_dataframe.sort_values('Symbol', inplace=True)


    outputbox.delete(*outputbox.get_children())
    outputbox["column"] = list(gv.master_dataframe.columns)
    outputbox["show"] = "headings"
    for column in outputbox["columns"]:
        outputbox.heading(column, text=column)

    df_rows = gv.master_dataframe.to_numpy().tolist()
    for row in df_rows:
        outputbox.insert("", "end", values=row)
