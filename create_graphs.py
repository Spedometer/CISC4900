import global_variables as gv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt


def plot_graph(symbol):
    for item in gv.graph_frame.winfo_children():
        item.destroy()

    fig = Figure(figsize=(5, 2), dpi=85)
    fig.patch.set_facecolor('black')

    x = []
    y = []
    symbol_index = gv.user_input_list.index(symbol)

    for entry in gv.master_datapoint_list[symbol_index].symbol_json['Time Series (Daily)']:
            x.append(entry)

    for entry in gv.master_datapoint_list[symbol_index].symbol_json['Time Series (Daily)']:
        y.append(float(gv.master_datapoint_list[symbol_index].symbol_json['Time Series (Daily)'][entry]['4. close']))

    plt.style.use('dark_background')
    plot = fig.add_subplot(111)

    fig.autofmt_xdate()
    plot.plot(x, y)
    plot.invert_xaxis()

    n = int(gv.total_count / 25)
    for index, label in enumerate(plot.xaxis.get_ticklabels()):
        if index % n != 0:
            label.set_visible(False)

    canvas = FigureCanvasTkAgg(fig, master=gv.graph_frame)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0, rely=0, relheight=.9, relwidth=1)
    toolbar = NavigationToolbar2Tk(canvas, gv.graph_frame, pack_toolbar=False)
    toolbar.place(relx=0, rely=.9, relheight=.1, relwidth=1)
    toolbar.update()
