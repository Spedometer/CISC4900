# Module creates framework for the Historic Data Form, which will be used to accept stock symbol input from user
# Mid_Right_Top_Frame will be used to display averages of the datapoints obtained from Alpha Vantage API call
#
# May need to implement function to manually input new api key if necessary

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import requests
import json
import csv
import pandas as pd
import retrieve_data_from_json as rd

default_dir = "CISC4900/Files"
api_key = "XHVXGZR30PZIGH91"

HEIGHT = 800
WIDTH = 1200

root = Tk()
root.title("Historic Data")
# root.iconbitmap(default_dir + '/' + 'images' + '/' + 'BrooklynCollege.ico')

canvas = Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

top_frame = Frame(root, bg='#CCD9FF')
top_frame.place(relx=.05, rely=.05, relheight=.1, relwidth=.9, anchor='nw')
name_label = Label(top_frame, text="Enter Symbol: ", bg='#ccd9ff', font=30)
name_label.place(relx=.05, rely=.25, relheight=.5, relwidth=.25, anchor='n')
name_input = Entry(top_frame, font=30, bg='#D3D3D3')
name_input.place(relx=.15, rely=.25, relheight=.45, relwidth=.075, anchor='n')
submit_btn = Button(top_frame, text="SUBMIT", command=lambda:rd.retrieve_from_json(name_input.get(),
                                                                                   outputbox, api_key, default_dir,
                                                                                   mid_right_top_frame,
                                                                                   name_input))
submit_btn.place(relx=.25, rely=.25, relheight=.45, relwidth=.1, anchor='n')

mid_left_frame = Frame(root, bg='red')
mid_left_frame.place(relx=.05, rely=.15, relheight=.8, relwidth=.15)

mid_right_top_frame = LabelFrame(root, bg='#FAEBD7', highlightbackground='black', highlightcolor='black',
                            highlightthickness=1)
mid_right_top_frame.place(relx=.2, rely=.15, relheight=.4, relwidth=.75)
# header_label = Label(mid_right_top_frame, text="StockSymbol\t\tOpen Avg\tHigh Avg\tLow Avg\t\tClose Avg\tVolume Avg")
# header_label.pack()


outputbox = ttk.Treeview(mid_right_top_frame)
outputbox.place(relheight=1, relwidth=1)

outputbox_scrolly = Scrollbar(mid_right_top_frame, orient="vertical", command=outputbox.yview)
outputbox_scrollx = Scrollbar(mid_right_top_frame, orient="horizontal", command=outputbox.xview)
outputbox.configure(yscrollcommand=outputbox_scrolly, xscrollcommand=outputbox_scrollx)
outputbox_scrollx.pack(side="bottom", fill="x")
outputbox_scrolly.pack(side="right", fill="y")

mid_right_bottom_frame = Frame(root, bg='green')
mid_right_bottom_frame.place(relx=.2, rely=.55, relheight=.4, relwidth=.75)

root.mainloop()
