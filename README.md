# CISC4900
CISC4900 Project Files
<br/>
Brian Chan
bchan15@gmail.com
<br/><br/>
<br/><br/>
Required to install the following libraries:
<br/>
pip install requests
<br/>
pip install pandas
<br/>
pip install pillows
<br/><br/><br/>
got an numpy error, which was packaged with pandas, had to install older version:
<br/>
pip install numpy==1.19.3
<br/><br/><br/>
11/16/2020 - 
Program is currently in its early stages. GUI is just a framework thus far, a mere skeleton. It can only take input from user via Entry() widget, which calls Alpha Vantage API to retrieve raw data from their TIME_SERIES_DAILY function. Currently using compact datapoints for testing. Will change to full 20 years worth of datapoints when program is ready. It saves as json file to hard drive 'CISC4900/Files' in current directory. Functions use the json with the associated symbol for data manipulation. Averages of the open prices, high prices, low prices, close prices, and volume are passed to a pandas dataframe which is then passed to treeview widget within the main Historic Data GUI. Known issues thus far, blank or invalid stock sybmols result in junk .json files being created. Possible solution is to implement symbol_reference_list to compare names to verify existence. Need to add standard deviation calculations and pass that to dataframe as well. Dataframe is not aligned properly, will need to adjust font. Aesthetics will be done at the end. iconbitmap stopped working, in the process of troubleshooting. Need to develop interface to order trades via AmeriTrade API exchange once Historic Data GUI is completed or near completed.
<br/><br/>
11/23/2020 - Added function to calculate standard deviation. I want to add option for user to define the period time, default is 10 entries(days in this instance). Added a notebook to bottom right frame to display time series and second tab to display standard devaition. Intending to include options to display graph if time permits. Considering swap positions of outputbox displays with Averages and Time series. Also want to combine standard deviation columns with time series for a more complete overview rather than it being fragmented, with that information still on display in conjunction with possible graphs. Function that calculates standard deviation feels a bit clunky. Instead of three separate lists, I want to combine it into one list of lists [(a,b,c), (d,e,f)...], if time permits will clean up that code. Currently tab change is bound so when Standard deviation is clicked, function is called, want to change so view_selected will update entire notebook instead. Another change I want to make is to add a smaller separate frame for the selected stock symbols where user can choose to display details for. However, due to the time constraint, beginning next week, I will need to get started on the AmeriTrade aspect of the project and come back to the extra stuff if there is time.
