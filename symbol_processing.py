import global_variables as gv
import pandas as pd


# Creates list of reference symbols from nasdaq acquired .txt file
def create_symbol_list():
    symbol_reference_path = gv.default_dir + '/symbol_list/nasdaqtraded.txt'
    df = pd.read_csv(symbol_reference_path, delimiter="|", usecols=['Symbol', 'Security Name'])
    gv.symbol_reference_list = df.to_numpy().tolist()


# Verifies symbol entered by user against list, not currently utilized, using alternative
def symbol_verification():
    any_entry_found = False
    for symbol, name in gv.symbol_reference_list:
        for entry in gv.user_input_list:
            if (entry == symbol):
                # print("{} and {} found".format(symbol, name))
                any_entry_found = True
    if any_entry_found == False:
        gv.dialog_text['text'] = "Symbol Unknown, Please Try Again."


def clear_list():
    gv.user_input_list.clear()
