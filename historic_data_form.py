# Module creates framework for the Historic Data Form, which will be used to accept stock symbol input from user
# Mid_Right_Top_Frame will be used to display averages of the datapoints obtained from Alpha Vantage API call
#
# May need to implement function to manually input new api key if necessary

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import retrieve_data_from_json as rd
import global_variables as gv
import create_pandas_dataframe
# import standard_deviation
import create_graphs as cg
import td_ameritrade as tda
import json
import threading
import time


# When Time Series button is clicked and new entry data is updated, will default back to Time Series tab, since other
# tabs will contain contents connected to previous symbol
def view_selected(event):
    try:
        # current_item = gv.outputbox.item(gv.outputbox.focus())
        global symbol_label
        current_item = gv.user_list_outputbox.item(gv.user_list_outputbox.focus())
        symbol = current_item['values'][0]

        for k, v in gv.symbol_reference_list:
            if k == symbol:
                symbol_label['text'] = k + " : " + v

        create_pandas_dataframe.create_outputbox1_dataframe(symbol, period)
        # standard_deviation.calculate_std(period)
        # standard_deviation.calculate_moving_averages()
        # tabControl.select(outputbox2_frame)
        update_max_count()
        cg.plot_graph(symbol)
        # bar()

    except IndexError:
        gv.dialog_text['text'] = "Symbol has not been selected."


# Currently remove button not functioning properly, requires further troubleshooting
# It removes symbol from the user_input_list, but needs to be also removed from master dataframe
def remove_symbol():
    gv.dialog_text['text'] = ""
    global name_input
    current_item = gv.user_list_outputbox.item(gv.user_list_outputbox.focus())
    symbol = current_item['values'][0]

    gv.user_input_list.remove(symbol)
    gv.master_dataframe.drop(gv.master_dataframe[gv.master_dataframe['Symbol'] == symbol].index, inplace=True)
    gv.outputbox2.delete(*gv.outputbox2.get_children())
    create_pandas_dataframe.refresh_user_list_outputbox_dataframe()


# def update_max_count(event):
#     global max_count
#     max_count = max_entries_combobox.get()
#     num_entries_label['text'] = "Averages of {} trading days".format(max_count)


def update_max_count():
    num_entries_label['text'] = "Averages of last {} trading days".format(gv.total_count)


# Progress bar not currently used, originally during testing, when multiple symbols were being processed in sequence or
# when full 20+ year historic data was retrieved and processed, it hung the program, decided to stick with compact
# for project and presentation to keep things simple
def bar():
    progress = ttk.Progressbar(dialog_frame, orient=HORIZONTAL,
                               length=100, mode='indeterminate')
    progress.place(relx=0.005, rely=0.1)
    progress_percentage = Label(dialog_frame, bg="silver")
    progress_percentage.place(relx=.075, rely=0.1)

    import time
    progress['value'] = 20
    progress_percentage['text'] = "20%"
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 40
    progress_percentage['text'] = "40%"
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 60
    progress_percentage['text'] = "60%"
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 80
    progress_percentage['text'] = "80%"
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 100
    progress_percentage['text'] = "100%"
    progress.place_forget()
    progress_percentage.place_forget()


def load_symbol_data(event):
    symbol_name = ""

    if combo_box_symbol_list.get() == "None":
        combo_box_symbol_list.set("")
    else:
        #print(combo_box_symbol_list.get())
        # print(gv.symbol_reference_list)
        # selected_symbol_index = gv.user_input_list.index(combo_box_symbol_list.get())
        create_forecast_frame()

        for entry in gv.symbol_reference_list:
            if entry[0] == combo_box_symbol_list.get():
                symbol_name = entry[1]


# Ran out of time, was going to implement an option for user to select time period to calculate moving averages
# Below code is a remnant of that endeavor
#
# def update_avg_sd(event):
#     print(time_period_cb.get())
#
#
# def enter_hit(event):
#     if int(time_period_cb.get()) > 100 or int(time_period_cb.get()) < 1:
#         print(time_period_cb.get(), " Period selected out of range")
#         time_period_cb.set("")
#         return
#     else:
#         print(time_period_cb.get())


def update_combobox_symbols(event):
    combo_box_symbol_list['values'] = gv.user_input_list


def exit_program():
    close = messagebox.askokcancel("Exit", "Exit Program?")
    if close:
        tda.get_quote_stream = "OFF"
        try:
            get_quote_thread.join()
        except RuntimeError:
            pass
        except NameError:
            pass
        except AttributeError:
            pass
        except Exception:
            pass
        root.destroy()


def create_feed(symbol, data):
    global feed_frame
    feed_frame = Frame(top_right_frame, bg='#0b2438')
    feed_frame.grid(row=1, column=0, padx=20, pady=20)
    symbol_description = Label(feed_frame, text=data[symbol]['description'],
                               justify=LEFT, bg='#0b2438', fg="white", font=9)
    symbol_description.grid(row=0, column=0, padx=10, pady=10, sticky='nw', columnspan=3)
    # blank_space2 = Label(feed_frame, bg='#0b2438', fg="white")
    # blank_space2.grid(row=1, column=0)
    bid_price_label = Label(feed_frame, text="Bid Price", justify=LEFT, bg='#0b2438', fg="white", font=6)
    bid_price_label.grid(row=2, column=0, padx=10, pady=10, sticky='nw')
    bid_price = Label(feed_frame, text='${:,.2f}'.format(data[symbol]['bidPrice']), bg='#0b2438', fg="white", font=6)
    bid_price.grid(row=2, column=1, padx=10, pady=10, sticky='nw')
    ask_price_label = Label(feed_frame, text="Ask Price", justify=LEFT, bg='#0b2438', fg="white", font=6)
    ask_price_label.grid(row=3, column=0, padx=10, pady=10, sticky='nw')
    ask_price = Label(feed_frame, text='${:,.2f}'.format(data[symbol]['askPrice']), bg='#0b2438', fg="white", font=6)
    ask_price.grid(row=3, column=1, padx=10, pady=10, sticky='nw')
    last_price_label = Label(feed_frame, text="Last Price", justify=LEFT, bg='#0b2438', fg="white", font=6)
    last_price_label.grid(row=4, column=0, padx=10, pady=10, sticky='nw')
    last_price = Label(feed_frame, text='${:,.2f}'.format(data[symbol]['lastPrice']), bg='#0b2438', fg="white", font=6)
    last_price.grid(row=4, column=1, padx=10, pady=10, sticky='nw')


def destroy_feed():
    # global feed_frame
    for widget in feed_frame.winfo_children():
        widget.destroy()
    feed_frame.destroy()


def get_quote_loop(symbol):
    while True:
        get_quote_data = tda.get_quote(symbol)
        create_feed(symbol, get_quote_data)
        time.sleep(3)

        if get_quote_stream == "OFF":
            destroy_feed()
            break


def get_quote_toggle(symbol):
    global get_quote_stream
    if live_feed_btn.config('relief')[-1] == 'raised':
        get_quote_stream = "ON"
        live_feed_btn.config(relief='sunken')
        live_feed_btn.config(text="Stop Feed")
        get_quote_thread = threading.Thread(target=get_quote_loop, args=(symbol,))
        get_quote_thread.start()

    elif live_feed_btn.config('relief')[-1] == 'sunken':
        get_quote_stream = "OFF"
        live_feed_btn.config(relief='raised')
        live_feed_btn.config(text='Start Feed')


def create_forecast_frame():
    symbol = combo_box_symbol_list.get()

    forecast_frame = Frame(left_frame, bg='#0b2438')
    forecast_frame.place(relx=.025, rely=.2, relheight=.8, relwidth=.8)
    forecast_average_label = Label(forecast_frame, text="Latest Average", justify=LEFT, anchor='nw',
                                   bg='#0b2438', fg="white")
    forecast_average_label.grid(row=0, column=0, sticky='nw', padx=5, pady=5)
    forecast_average = Label(forecast_frame, justify=LEFT, anchor='nw',
                                   bg='#0b2438', fg="white")
    forecast_average.grid(row=0, column=1, sticky='nw', padx=5, pady=5)

    forecast_deviation_label = Label(forecast_frame, text="Latest Deviation", justify=LEFT, anchor='nw',
                                   bg='#0b2438', fg="white")
    forecast_deviation_label.grid(row=1, column=0, sticky='nw', padx=5, pady=5)
    forecast_deviation = Label(forecast_frame, justify=LEFT, anchor='nw',
                                   bg='#0b2438', fg="white")
    forecast_deviation.grid(row=1, column=1, sticky='nw', padx=5, pady=5)
    forecast_upper_limit_label = Label(forecast_frame, text="Upper Limit", justify=LEFT, anchor='nw',
                                   bg='#0b2438', fg="white")
    forecast_upper_limit_label.grid(row=2, column=0, sticky='nw', padx=5, pady=5)
    forecast_upper_limit = Label(forecast_frame, justify=LEFT, anchor='nw',
                                   bg='#0b2438', fg="white")
    forecast_upper_limit.grid(row=2, column=1, sticky='nw', padx=5, pady=5)
    forecast_lower_limit_label = Label(forecast_frame, text="Lower Limit", justify=LEFT, anchor='nw',
                                   bg='#0b2438', fg="white")
    forecast_lower_limit_label.grid(row=3, column=0, sticky='nw', padx=5, pady=5)
    forecast_lower_limit = Label(forecast_frame, justify=LEFT, anchor='nw',
                                   bg='#0b2438', fg="white")
    forecast_lower_limit.grid(row=3, column=1, sticky='nw', padx=5, pady=5)
    buy_btn = Button(forecast_frame, text="BUY", justify=LEFT, anchor='center', bg='#0b2438', fg="white",
                     command=lambda:tda.place_buy_order(symbol, 1, 50.50))
    buy_btn.grid(row=4, column=0, sticky='nw', padx=15, pady=20, ipadx=30, ipady=20)
    sell_btn = Button(forecast_frame, text="SELL", justify=LEFT, anchor='center', bg='#0b2438', fg="white",
                      command=lambda:tda.place_sell_order(symbol, 2, 33.33))
    sell_btn.grid(row=4, column=1, sticky='nw', padx=15, pady=20, ipadx=30, ipady=20)
    cancel_btn = Button(forecast_frame, text="CANCEL", justify=LEFT, anchor='center', bg='#0b2438', fg="white",
                        command=tda.cancel_order)
    cancel_btn.grid(row=4, column=2, sticky='nw', padx=15, pady=20, ipadx=20, ipady=20)

    for sublist in gv.moving_avg_datapoint_list:
        if sublist[0] == symbol:
            forecast_average['text'] = '$ {:,.2f}'.format(float(sublist[1]))
            forecast_deviation['text'] = '$ {:,.2f}'.format(float(sublist[2]))
            forecast_upper_limit['text'] = '$ {:,.2f}'.format(float(sublist[1]) + abs(float(sublist[2])))
            forecast_lower_limit['text'] = '$ {:,.2f}'.format(float(sublist[1]) - abs(float(sublist[2])))


period = 10
max_count = 0
HEIGHT = 800
WIDTH = 1200
global get_quote_thread
get_quote_stream = 'OFF'


root = Tk()
root.title("CISC4900 - Robo Trader")
root.iconbitmap(gv.default_dir + '/' + 'images' + '/' + 'BrooklynCollege.ico')
root.geometry("1400x800")

root.tk.call('lappend', 'auto_path', 'CISC4900/Files/awthemes-9.5.1.1')
root.tk.call('package', 'require', 'awdark')
style = ttk.Style()
style.theme_use("awdark")


main_notebook = ttk.Notebook(root)
historic_data_frame = Frame(main_notebook)
historic_data_frame.pack()


top_frame = Frame(historic_data_frame, bg='#0b2438')
top_frame.place(relx=0, rely=0, relheight=.1, relwidth=1, anchor='nw')
title_label = Label(top_frame, text="CISC4900-Robo Trader", bg='#0b2438', fg='white', font=("Helvetica", 20),
                    justify=LEFT)
title_label.place(relx=.7, rely=.1, relheight=.5, relwidth=.25, anchor='nw')
alpha_vantage_label = Label(top_frame, text="Data Points courtesy of Alpha Vantage", bg='#0b2438', fg='white',
                            font=("Helvetica", 10), justify=RIGHT)
alpha_vantage_label.place(relx=.847, rely=.49, relheight=.5, relwidth=.4, anchor='n')


mid_left_frame = Frame(historic_data_frame, bg='#0b2438')
mid_left_frame.place(relx=0, rely=.1, relheight=.875, relwidth=.4)
name_label = Label(mid_left_frame, text="Enter Symbol: ", bg="#0b2438", fg="white")
name_label.place(relx=0.1, rely=0, relheight=.05, relwidth=.4, anchor='n')
name_input = Entry(mid_left_frame, font=30, bg='#D3D3D3', justify=CENTER)
name_input.place(relx=0.25, rely=0, relheight=.05, relwidth=.15, anchor='n')
hint_label = Label(mid_left_frame, text="(Click Symbol Below for Details)", bg="#0b2438", fg="white", justify=LEFT)
hint_label.place(relx=0.18, rely=.07, anchor='n')

submit_btn = Button(mid_left_frame, text="Add Symbol",
                    command=lambda: rd.retrieve_from_json(name_input.get(), name_input), bg="#0b2438", fg="white")
submit_btn.place(relx=.4, rely=0, relheight=.05, relwidth=.15, anchor='n')

remove_one_btn = Button(mid_left_frame, text="Remove Selected", command=remove_symbol, bg="#0b2438", fg="white")
remove_one_btn.place(relx=.75, rely=0, relheight=.05, relwidth=.2, anchor='n')

# Below is test code, wanted to implement ability for user to select # of trading days to practice first, with the
# intention of eventually allowing user to limit search by dates, however, encountered some difficulties due to
# weekends and holidays when market is closed, need a solution for when non-trading day is selected as one of the
# parameters
#
# max_entries_label = Label(mid_left_frame, text="Select # of Trading Days ", bg="#0b2438", fg="white")
# max_entries_label.place(relx=.123, rely=.075, relheight=.05, relwidth=.3, anchor='n')
#
# tvar = StringVar()
# max_entries_combobox = ttk.Combobox(mid_left_frame, width=25, textvariable=tvar)
# max_entries_combobox.place(relx=.3, rely=.075, relheight=.05, relwidth=.09, anchor='n')
# max_entries_combobox['values'] = ("ALL", 5, 10, 20, 60, 120, 250)
# max_entries_combobox.current(0)
# max_entries_combobox.bind('<<ComboboxSelected>>', update_max_count)

num_entries_label = Label(mid_left_frame,
                          bg='#0b2438', fg="white", font='9')
num_entries_label.place(relx=.135, rely=.15, relheight=.05, relwidth=.5, anchor='nw')

gv.user_list_outputbox = ttk.Treeview(mid_left_frame)
gv.user_list_outputbox.place(relx=.025, rely=0.2, relheight=.8, relwidth=.9)
user_list_outputbox_scrolly = Scrollbar(gv.user_list_outputbox, orient="vertical", command=gv.user_list_outputbox.yview)
gv.user_list_outputbox.configure(yscrollcommand=user_list_outputbox_scrolly.set)
user_list_outputbox_scrolly.pack(side="right", fill="y")
gv.user_list_outputbox.bind('<ButtonRelease-1>', view_selected)


# Below block was initially used, but has been replaced
# details_btn = Button(mid_left_frame, text="View Details\nof Selected Symbol", command=view_selected)
# details_btn.place(relx=.5, rely=.2, relheight=.1, relwidth=.7, anchor='n')
mid_right_top_frame = LabelFrame(historic_data_frame, bg='#0b2438', highlightbackground='black', highlightcolor='black',
                                 highlightthickness=1)
mid_right_top_frame.place(relx=.4, rely=.1, relheight=.45, relwidth=.6)

tabControl = ttk.Notebook(mid_right_top_frame)
outputbox_frame = Frame(tabControl)

gv.outputbox = ttk.Treeview(outputbox_frame)
gv.outputbox.place(relheight=1, relwidth=1)
outputbox_scrolly = Scrollbar(gv.outputbox, orient="vertical", command=gv.outputbox.yview)
gv.outputbox.configure(yscrollcommand=outputbox_scrolly.set)
outputbox_scrolly.pack(side="right", fill="y")
# gv.outputbox.bind('<ButtonRelease-1>', view_selected)
tabControl.add(outputbox_frame, text="Time Series (Daily)")
tabControl.place(relx=0, rely=0, relheight=.9, relwidth=1)


########################
### AMERITRADE START ###
########################

ameritrade_frame = Frame(main_notebook, bg='#0b2438')
left_frame = LabelFrame(ameritrade_frame, text="Select Stock Symbol", bg='#0b2438', fg="white", font=10)
left_frame.place(relx=.025, rely=.025, relheight=.45, relwidth=.425)

main_notebook.bind('<<NotebookTabChanged>>', update_combobox_symbols)

combo_box_var = StringVar()
combo_box_symbol_list = ttk.Combobox(left_frame, width=3, textvariable=combo_box_var, justify=LEFT)
combo_box_symbol_list.place(relx=.025, rely=.025, relheight=.1, relwidth=.15)
combo_box_symbol_list.bind('<<ComboboxSelected>>', load_symbol_data)


# Ran out of time, was going to implement an option for user to select time period to calculate moving averages
# Below test code is a remnant of that endeavor
# time_period_var = StringVar()
# time_period_cb = ttk.Combobox(left_frame, width=3, height=5, textvariable=time_period_var, justify=LEFT)
# time_period_cb['values'] = [i for i in range(1, 101)]
# time_period_cb.bind('<<ComboboxSelected>>', update_avg_sd)
# time_period_cb.bind('<Return>', enter_hit)
# time_period_cb.place(relx=.25, rely=.3, relheight=.1, relwidth=.1)
# standard_dev_label = Label(left_frame, text="Standard Dev info here", justify=LEFT, anchor='nw',
#                            bg='#0b2438', fg="white")
# standard_dev_label.place(relx=0.025, rely=.45, relheight=.1, relwidth=.3)


top_right_frame = LabelFrame(ameritrade_frame, text="Live Stock Quote", bg='#0b2438', fg="white", font=10)
top_right_frame.place(relx=.55, rely=.025, relheight=.45, relwidth=.425)
live_feed_btn = Button(top_right_frame, text="Start Feed", justify=CENTER,
                       command=lambda:get_quote_toggle(combo_box_symbol_list.get()),
                       relief="raised", bg="#0b2438", fg="white")
live_feed_btn.grid(row=0, column=0, padx=20, pady=20, ipadx=20, ipady=15, sticky='nw')


bottom_left_frame = LabelFrame(ameritrade_frame, text="Account Information", bg='#0b2438', fg="white", font=10)
bottom_left_frame.place(relx=.025, rely=.5, relheight=.45, relwidth=.310)

bottom_left_inner_frame = Frame(bottom_left_frame, bg='#0b2438')
bottom_left_inner_frame.place(relx=.05, rely=.05, relheight=.9, relwidth=.9)

account_id_label = Label(bottom_left_inner_frame, text="Account ID:     ", bg="#0b2438", fg="white", font=10)
account_id_label.grid(row=0, column=0, sticky=W)
account_id = Label(bottom_left_inner_frame,
        text=tda.accounts_data[0]['securitiesAccount']['accountId'],
        justify=LEFT, bg="#0b2438", fg="white", font=10)
account_id.grid(row=0, column=1, sticky=W)
blank_space = Label(bottom_left_inner_frame, bg="#0b2438", fg="white", justify=LEFT)
blank_space.grid(row=1, column=0, sticky=W)
accruedInterest_label = Label(bottom_left_inner_frame, text="Accrued Interest:", bg="#0b2438", fg="white")
accruedInterest_label.grid(row=2, column=0, sticky=W, padx=5, pady=5)
accruedInterest = Label(bottom_left_inner_frame,
        text='${:,.2f}'.format(tda.accounts_data[0]['securitiesAccount']['currentBalances']['accruedInterest']),
        justify=LEFT, bg="#0b2438", fg="white")
accruedInterest.grid(row=2, column=1, sticky=W, padx=5, pady=5)
cashBalance_label = Label(bottom_left_inner_frame, text="Cash Balance:", bg="#0b2438", fg="white")
cashBalance_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)
cashBalance = Label(bottom_left_inner_frame,
        text='${:,.2f}'.format(tda.accounts_data[0]['securitiesAccount']['currentBalances']['cashBalance']),
        justify=LEFT, bg="#0b2438", fg="white")
cashBalance.grid(row=3, column=1, sticky=W, padx=5, pady=5)
cashReceipts_label = Label(bottom_left_inner_frame, text="Cash Receipts:", justify=LEFT, bg="#0b2438", fg="white")
cashReceipts_label.grid(row=4, column=0, sticky=W, padx=5, pady=5)
cashReceipts = Label(bottom_left_inner_frame,
        text='${:,.2f}'.format(tda.accounts_data[0]['securitiesAccount']['currentBalances']['cashReceipts']),
        justify=LEFT, bg="#0b2438", fg="white")
cashReceipts.grid(row=4, column=1, sticky=W, padx=5, pady=5)
cashAvailableForTrading_label = Label(bottom_left_inner_frame, text="Cash Available for Trading:", justify=LEFT,
                                      bg="#0b2438", fg="white")
cashAvailableForTrading_label.grid(row=5, column=0, sticky=W, padx=5, pady=5)
cashAvailableForTrading = Label(bottom_left_inner_frame,
        text='${:,.2f}'.format(tda.accounts_data[0]['securitiesAccount']['currentBalances']['cashAvailableForTrading']),
        justify = LEFT, bg="#0b2438", fg="white")
cashAvailableForTrading.grid(row=5, column=1, sticky=W, padx=5, pady=5)
cashAvailableForWithdrawal_label = Label(bottom_left_inner_frame, text="Cash Available for Withdrawal:  ",
                                         justify=LEFT, bg="#0b2438", fg="white")
cashAvailableForWithdrawal_label.grid(row=6, column=0, sticky=W, padx=5, pady=5)
cashAvailableForWithdrawal = Label(bottom_left_inner_frame,
        text='${:,.2f}'.format(tda.accounts_data[0]['securitiesAccount']['currentBalances']['cashAvailableForWithdrawal']),
        justify=LEFT, bg="#0b2438", fg="white")
cashAvailableForWithdrawal.grid(row=6, column=1, sticky=W, padx=5, pady=5)
totalCash_label = Label(bottom_left_inner_frame, text="Total Cash:", justify=LEFT, bg="#0b2438", fg="white")
totalCash_label.grid(row=7, column=0, sticky=W, padx=5, pady=5)
totalCash = Label(bottom_left_inner_frame,
        text='${:,.2f}'.format(tda.accounts_data[0]['securitiesAccount']['currentBalances']['totalCash']),
        justify=LEFT, bg="#0b2438", fg="white")
totalCash.grid(row=7, column=1, sticky=W, padx=5, pady=5)
unsettledCash_label = Label(bottom_left_inner_frame, text="Unsettled Cash:", justify=LEFT, bg="#0b2438", fg="white")
unsettledCash_label.grid(row=8, column=0, sticky=W, padx=5, pady=5)
unsettledCash = Label(bottom_left_inner_frame,
        text='${:,.2f}'.format(tda.accounts_data[0]['securitiesAccount']['currentBalances']['unsettledCash']),
        justify=LEFT, bg="#0b2438", fg="white")
unsettledCash.grid(row=8, column=1, sticky=W, padx=5, pady=5)


bottom_mid_frame = LabelFrame(ameritrade_frame, text="Current Orders", bg='#0b2438', fg="white", font=10)
bottom_mid_frame.place(relx=0.335, rely=.5, relheight=.45, relwidth=.315)
bottom_mid_inner_frame = Frame(bottom_mid_frame, bg='#0b2438')
bottom_mid_inner_frame.place(relx=.05, rely=.05, relheight=.9, relwidth=.9)
orders_info = Text(bottom_mid_inner_frame, bg='#0b2438', fg="white")
orders_info.pack(padx=5, pady=5)
orders_info.insert(INSERT, json.dumps(tda.orders_data, indent=4))


bottom_right_frame = LabelFrame(ameritrade_frame, text="Orders History", bg='#0b2438', fg="white", font=10)
bottom_right_frame.place(relx=.65, rely=.5, relheight=.45, relwidth=.315)
bottom_right_inner_frame = Frame(bottom_right_frame, bg='#0b2438')
bottom_right_inner_frame.place(relx=.05, rely=.05, relheight=.9, relwidth=.9)
history_info = Text(bottom_right_inner_frame, bg='#0b2438', fg="white")
history_info.pack(padx=5, pady=5)
history_info.insert(INSERT, json.dumps(tda.orders_history_data, indent=4))

######################
### AMERITRADE END ###
######################


mid_right_bottom_frame = Frame(historic_data_frame, bg='#0b2438', highlightbackground='black', highlightcolor='black',
                               highlightthickness=1)
mid_right_bottom_frame.place(relx=.4, rely=.5, relheight=.475, relwidth=.6)

symbol_label = Label(mid_right_bottom_frame, bg="#0b2438", fg="white", font='9')
symbol_label.place(relx=0, rely=0, relwidth=1, relheight=.1, anchor='nw')

tabControl2 = ttk.Notebook(mid_right_bottom_frame)
outputbox2_frame = Frame(tabControl2)
gv.outputbox2 = ttk.Treeview(outputbox2_frame)
gv.outputbox2.place(relheight=1, relwidth=1)
outputbox2_scrolly = Scrollbar(gv.outputbox2, orient="vertical", command=gv.outputbox2.yview)
gv.outputbox2.configure(yscrollcommand=outputbox2_scrolly.set)
outputbox2_scrolly.pack(side="right", fill="y")

standard_deviation_frame = Frame(tabControl2)
gv.std_dev_outputbox = ttk.Treeview(standard_deviation_frame)
gv.std_dev_outputbox.place(relheight=1, relwidth=1)
std_dev_outputbox_scrolly = Scrollbar(standard_deviation_frame, orient="vertical", command=gv.std_dev_outputbox.yview)
gv.std_dev_outputbox.configure(yscrollcommand=std_dev_outputbox_scrolly.set)
std_dev_outputbox_scrolly.pack(side="right", fill="y")


gv.graph_frame = Frame(tabControl2, bg='#0b2438')
# tabControl2.add(outputbox2_frame, text="Time Series (Daily)")
# tabControl2.add(standard_deviation_frame, text="Graph")
tabControl2.add(gv.graph_frame, text="Close Price")
tabControl2.place(relx=0, rely=.1, relheight=.9, relwidth=1)
# Below code initially use to have a bind to only load data when tab is clicked, instead, right now, all tabs
# are pre-processed before switching tabs
# tabControl.pack(expand=1, fill="both")
# tabControl.bind('<<NotebookTabChanged>>', on_tab_change)


dialog_frame = Frame(root, bg="silver")
dialog_frame.place(relx=0, rely=.974, relheight=.025, relwidth=1)
gv.dialog_text = Label(dialog_frame, bg="silver", fg="black", relief=RIDGE)
gv.dialog_text.pack(anchor=E)


main_notebook.add(historic_data_frame, text="Historic Market Data")
main_notebook.add(ameritrade_frame, text="Ameritrade")
main_notebook.pack(expand=1, fill="both")


root.protocol("WM_DELETE_WINDOW", exit_program)

root.mainloop()
