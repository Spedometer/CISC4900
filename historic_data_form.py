# Module creates framework for the Historic Data Form, which will be used to accept stock symbol input from user
# Mid_Right_Top_Frame will be used to display averages of the datapoints obtained from Alpha Vantage API call
#
# May need to implement function to manually input new api key if necessary

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import retrieve_data_from_json as rd
import global_variables as gv
import create_pandas_dataframe
import standard_deviation


# When standard deviation tab is clicked, calls function to populate frame
def on_tab_change(event):
    tab = event.widget.tab('current')['text']
    if tab == "Standard Deviation":
        standard_deviation.calculate_std(outputbox, period)


# When Time Series button is clicked and new entry data is updated, will default back to Time Series tab, since other
# tabs will contain contents connected to previous symbol
def view_selected():
    try:
        current_item = outputbox.item(outputbox.focus())
        symbol = current_item['values'][0]
        create_pandas_dataframe.create_outputbox2_dataframe(symbol)
        tabControl.select(outputbox2_frame)

    except IndexError:
        gv.dialog_text['text'] = "Symbol has not been selected."


HEIGHT = 800
WIDTH = 1200

root = Tk()
root.title("Historic Data")
# root.iconbitmap(gv.default_dir + '/' + 'images' + '/' + 'BrooklynCollege.ico')

canvas = Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3",
                font=("Helvetica", "10"))
style.map('Treeview', background=[('selected', 'silver')])
style.configure("Treeview.Heading", font=("Helvetica", "11"), rowheight=30)

top_frame = Frame(root, bg='#CCD9FF')
top_frame.place(relx=0, rely=0, relheight=.1, relwidth=1, anchor='nw')
title_label = Label(top_frame, text="CISC4900-Robo Trader", bg='#ccd9ff', font=("Helvetica", 20), justify=LEFT)
title_label.place(relx=0, rely=.25, relheight=.5, relwidth=.25, anchor='nw')
alpha_vantage_label = Label(top_frame, text="Data Points courtesy of Alpha Vantage", bg='#ccd9ff',
                            font=("Helvetica", 15), justify=RIGHT)
alpha_vantage_label.place(relx=.85, rely=.25, relheight=.5, relwidth=.4, anchor='n')


mid_left_frame = Frame(root, bg='#CCD9FF')
mid_left_frame.place(relx=0, rely=.1, relheight=.875, relwidth=.2)
name_input = Entry(mid_left_frame, font=30, bg='#D3D3D3')
name_input.place(relx=.5, rely=0, relheight=.1, relwidth=.7, anchor='n')
submit_btn = Button(mid_left_frame, text="Temporary\nSUBMIT Button",
                    command=lambda: rd.retrieve_from_json(name_input.get(), outputbox, name_input))
submit_btn.place(relx=.5, rely=.1, relheight=.1, relwidth=.7, anchor='n')
details_btn = Button(mid_left_frame, text="View Time Series\nof Selected Symbol", command=view_selected)
details_btn.place(relx=.5, rely=.2, relheight=.1, relwidth=.7, anchor='n')


mid_right_top_frame = LabelFrame(root, bg='#FAEBD7', highlightbackground='black', highlightcolor='black',
                                 highlightthickness=1)
mid_right_top_frame.place(relx=.2, rely=.1, relheight=.438, relwidth=.799)
outputbox = ttk.Treeview(mid_right_top_frame)
outputbox.place(relheight=1, relwidth=1)
outputbox_scrolly = Scrollbar(mid_right_top_frame, orient="vertical", command=outputbox.yview)
outputbox.configure(yscrollcommand=outputbox_scrolly.set)
outputbox_scrolly.pack(side="right", fill="y")


mid_right_bottom_frame = Frame(root, bg='#D3D3D3', highlightbackground='black', highlightcolor='black',
                               highlightthickness=1)
mid_right_bottom_frame.place(relx=.2, rely=.54, relheight=.4347, relwidth=.799)

tabControl = ttk.Notebook(mid_right_bottom_frame)

outputbox2_frame = Frame(tabControl)
gv.outputbox2 = ttk.Treeview(outputbox2_frame)
gv.outputbox2.place(relheight=1, relwidth=1)
outputbox2_scrolly = Scrollbar(outputbox2_frame, orient="vertical", command=gv.outputbox2.yview)
gv.outputbox2.configure(yscrollcommand=outputbox2_scrolly)
outputbox2_scrolly.pack(side="right", fill="y")

standard_deviation_frame = Frame(tabControl)
gv.std_dev_outputbox = ttk.Treeview(standard_deviation_frame)
gv.std_dev_outputbox.place(relheight=1, relwidth=1)
std_dev_outputbox_scrolly = Scrollbar(standard_deviation_frame, orient="vertical", command=gv.std_dev_outputbox.yview)
gv.std_dev_outputbox.configure(yscrollcommand=std_dev_outputbox_scrolly)
std_dev_outputbox_scrolly.pack(side="right", fill="y")

tabControl.add(outputbox2_frame, text="Time Series")
tabControl.add(standard_deviation_frame, text="Standard Deviation")
tabControl.pack(expand=1, fill="both")

tabControl.bind('<<NotebookTabChanged>>', on_tab_change)

dialog_frame = Frame(root, bg="silver")
dialog_frame.place(relx=0, rely=.975, relheight=.025, relwidth=1)
gv.dialog_text = Label(dialog_frame, text="Status updates will go here", bg="silver", relief=RIDGE)
gv.dialog_text.pack(anchor=E)

period = 10

root.mainloop()
