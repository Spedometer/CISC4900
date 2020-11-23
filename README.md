# CISC4900
CISC4900 Project Files
<br/>
Brian Chan
bchan15@gmail.com
<br/><br/>
<br/><br/>
Required to install the following libraries:
<br/><br/>
pip install requests
<br/><br/>
pip install pandas
<br/><br/>
pip install pillows
<br/><br/><br/>
got an numpy error, which was packaged with pandas, had to install older version:
<br/><br/>
pip install numpy==1.19.3
<br/>
<br/>
<br/>
11/16/2020
Program is currently in its early stages. GUI is just a framework thus far, a mere skeleton. It can only take input from user via Entry() widget, which calls Alpha Vantage API to retrieve raw data from their TIME_SERIES_DAILY function. Currently using compact datapoints for testing. Will change to full 20 years worth of datapoints when program is ready. It saves as json file to hard drive 'CISC4900/Files' in current directory. Functions use the json with the associated symbol for data manipulation. Averages of the open prices, high prices, low prices, close prices, and volume are passed to a pandas dataframe which is then passed to treeview widget within the main Historic Data GUI.
<br/>
<br/>
<br/>
Known issues thus far, blank or invalid stock sybmols result in junk .json files being created. Possible solution is to implement symbol_reference_list to compare names to verify existence. Need to add standard deviation calculations and pass that to dataframe as well. Dataframe is not aligned properly, will need to adjust font. Aesthetics will be done at the end. iconbitmap stopped working, in the process of troubleshooting. 
<br/>
<br/>
<br/>  
Need to develop interface to order trades via AmeriTrade API exchange once Historic Data GUI is completed or near completed.
