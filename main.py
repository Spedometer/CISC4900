import historic_data_form
import update_symbol_csv
import os
import errno
import pandas as pd

if __name__ == '__main__':

    default_dir = "CISC4900/Files"

    # Create the two primary sub directories where temp files will be stored
    try:
        os.makedirs(default_dir + '/'+ 'images')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    try:
        os.makedirs(default_dir + '/' + 'symbol_list')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Checks if file is present, if not, create stock symbol reference list off of the companylist from Nasdaq's website
    file_path = default_dir + "/" + "symbol_list" + "/" + "stock_symbol_reference.csv"
    if not os.path.isfile(file_path):
        update_symbol_csv.update_symbol_csv(default_dir)

