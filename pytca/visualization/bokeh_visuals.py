from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot

def plot_bokeh_dashboard(data):
    p1 = figure(plot_width=400, plot_height=400, title="Closing Prices")
    p1.line(data['Date'], data['Close'], color='blue', legend_label='Close')
    
    p2 = figure(plot_width=400, plot_height=400, title="Volume")
    p2.vbar(x=data['Date'], top=data['Volume'], width=0.5, color='green', legend_label='Volume')

    layout = gridplot([[p1, p2]])
    output_file("dashboard.html")
    show(layout)
