# CISC4900
CISC4900 Project Files

Required to install the following libraries:
>> pip install requests
>> pip install pandas
>> pip install pillows
got an numpy error, which was packaged with pandas, had to install older version:
>> pip install numpy==1.19.3

iconbitmap stopped working, in the process of troubleshooting. 

Program is currently in its early stages. GUI is just a framework thus far, a mere skeleton. It can only take input from user via Entry() widget, which calls Alpha Vantage API to retrieve raw data from their TIME_SERIES_DAILY function. Currently using compact datapoints for testing. Will change to full 20 years worth of datapoints when program is ready. It saves as json file to hard drive 'CISC4900/Files' in current directory. Functions use the json with the associated symbol for data manipulation. Averages of the open prices, high prices, low prices, close prices, and volume are passed to a pandas dataframe which is then passed to treeview widget within the main Historic Data GUI.

Known issues thus far: 
  -Blank or invalid stock sybmols result in junk .json files being created. Possible solution is to implement symbol_reference_list to compare names to verify existence.
  -need to add standard deviation calculations and pass that to dataframe as well
  -dataframe is not aligned properly, will need to adjust font
  -Aesthetics will be done at the end
  
Need to next after Historic Data GUI completed or near completed:
  -Develop interface to order trades via AmeriTrade API exchange.
