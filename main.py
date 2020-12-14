import symbol_processing as sp
import os
import errno
import global_variables as gv


if __name__ == '__main__':
    # Create the two primary sub directories where temp files will be stored
    try:
        os.makedirs(gv.default_dir + '/'+ 'images')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    try:
        os.makedirs(gv.default_dir + '/' + 'symbol_list')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Function to create newly implemented symbol reference list
    sp.create_symbol_list()

    import historic_data_form
