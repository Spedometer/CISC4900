# Stock Symbol list obtained from:
# https://old.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE
# Some of the data may be outdated, may need to be addressed, time permitting
# May need to download directly from site for abstraction purposes, from current site above, or new site
# Function to search if file is present and download if not may be needed
import pandas as pd
import global_variables as gv


def update_symbol_csv():
    default_symbol_csv = gv.default_dir + '/' + 'symbol_list/companylist.csv'
    df = pd.read_csv(default_symbol_csv)
    df = df.dropna(how='all')
    df = df.dropna(axis=0, subset=['Sector'])
    df.to_csv(r'CISC4900/files/symbol_list/stock_symbol_reference.csv', index=False, header=True)


# Possible future function to manually update Symbol csv
def add_symbol_entry():
    return


# Possible future function to obtain symbol list from alternative source
def obtain_symbol_csv():
    return

# Code below used to test function
# default_dir = "CISC4900/Files"
# update_symbol_csv(default_dir)
