'''
A bokeh-based interface for Eric Ayars coincidence counter
First-draft attempt at controls, graphs and values.
'''

import numpy as np

import numpy.random as random
import time
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, column
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import Slider, TextInput, Paragraph
from bokeh.plotting import figure


import automationhat

times = np.linspace(0,50,100)
data = np.zeros(100)

# create bokeh data sources for the two graphs
source = ColumnDataSource(data=dict(x=times, y=data))

# Set up plot
plot = figure(plot_height=400, plot_width=1000, title="ADC volts",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0,50], y_range=[0, 3])

# colors are dark for use in the dark optics labs
plot.background_fill_color = "black"
plot.border_fill_color = "black"

plot.line(x='x', y='y', line_width=0.5, source=source, color="red")

a = data.tolist()

# TODO change these to actual range sliders
scalemin = Slider(title="Scale minimum", value=0.0, start=0.0, end=5.0, step=0.2)
scalemax = Slider(title="Scale maximum", value=5.0, start=0.0, end=5.0, step=0.2)

# other widgets (not all are used yet)
phase = Slider(title="phase", value=0.0, start=0.0, end=5.0, step=0.1)
statsA = Paragraph(text="100", width=400, height=40)
statsB = Paragraph(text="100", width=400, height=40)
g2 = Paragraph(text="100", width=400, height=80)
g2_2d = Paragraph(text="100", width=400, height=40)


# start out keeping 20 data points
datapoints = 100

def update_data():
    # TODO: store data in a stream for charting vs time
    # this function is called every 10 ms (set below if you want to change it)

    data = automationhat.analog.one.read()

    # populate the list
    a.append(data)

    # resize this lists to keep only datapoints
    while len(a) > datapoints: a.pop(0)

    # set the A and B count displays
    statsA.text = "A: %d +/- %d" % (np.mean(a), np.std(a))

    source.data = dict(x=times, y=a)

def update_scales(attrname, old, new):
    global datapoints

    # Get the current slider values
    smin = scalemin.value
    smax = scalemax.value
    w = phase.value

    plot.y_range.start = smin
    plot.y_range.end = smax

# Add on_change listener to each widget that we're using:
for w in [scalemin, scalemax]:
    w.on_change('value', update_scales)


# Set up layouts and add to document
countControls = widgetbox(scalemin, scalemax)

# build the app document, this is just layout control and arranging the interface
curdoc().add_root(row(countControls, plot, column(statsA, statsB, g2), width=1800))
curdoc().title = "RaspberryPlot"

# set the callback to pull the data every 100 ms:
curdoc().add_periodic_callback(update_data, 10)
