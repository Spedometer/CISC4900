import pandas as pd

global outputbox2
global std_dev_outputbox
global dialog_text

api_key = "XHVXGZR30PZIGH91"
default_dir = "CISC4900/Files"
master_dataframe = pd.DataFrame({'Symbol': [],
                                 'Open Avg': [],
                                 'High Avg': [],
                                 'Low Avg': [],
                                 'Close Avg': [],
                                 'Volume Avg': []})
master_datapoint_list = []
user_input_list = []
