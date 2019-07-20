#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:07:52 2019

@author: deborahkhider

Slide visualization econ
"""

#import numpy as np
import pandas as pd

from bokeh.layouts import row, column, widgetbox
from bokeh.models import Slider
from bokeh.plotting import figure, output_file, show, ColumnDataSource, curdoc
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap 
from bokeh.models.glyphs import VBar

econ_data = pd.read_csv("results_summary.csv")
x = list(econ_data["crop"].unique())
y = [1543.7,574.8,1134.6,330.3,1594.6]

#get data
source = ColumnDataSource(data=dict(x=x, y=y))
source1 = ColumnDataSource(data=dict(x=x, y=y))
source2 = ColumnDataSource(data=dict(x=x, y=y))
# Make the histogram
plot = figure(x_range =source.data['x'], y_range=(0, 2500), plot_width=400, plot_height=400,
              title = 'Yield (kg/ha)', toolbar_location=None, tools="")              
              
glyph = VBar(x="x", top="y", width=0.9,
          fill_color=factor_cmap('x', palette=Spectral6, factors=x))
plot.add_glyph(source, glyph)

#show(plot)
# Prepare the sliders
c1_slider = Slider(start=-50, end=40, value=0, step=10, title="Land Cost Adjustment")
c2_slider = Slider(start=-50, end=40, value=0, step=10, title="Nitrogen Fertilizer Cost Adjustment")
p_slider = Slider(start=-50, end=40, value=0, step=10, title="Crop Price Adjustment")


# Make a call back function to get the values

#def search(data, x, c1, c2, p, column_ID):
#    new=[]
#    for item in x:
#        new.append(float(data[(data['c1']==c1) & (data['c2']==c2) & (data['p']==p) & \
#         (data['crop']==item.lower())][column_ID]))
#    print(c1,c2,p,x,new)
#    return new

def update_data(attr, old, new):
    column_ID = 'yield (kg/ha)'
    data = source.data
    data1 = source1.data
    data2 = source2.data
    c1_dynamic = c1_slider.value  # cb_obj.get('a_slider')
    c2_dynamic = c2_slider.value
    p_dynamic = p_slider.value
    #data['y'] = search(econ_data, data['x'], c1_dynamic, c2_dynamic, p_dynamic, column_ID)
    data['y'] = econ_data.query('p=='+str(p_dynamic)+' and c1=='+str(c1_dynamic)+' and c2=='+str(c2_dynamic))[column_ID]
    data1['y'] = econ_data.query('p=='+str(p_dynamic)+' and c1=='+str(c1_dynamic)+' and c2=='+str(c2_dynamic))['Nfert (kg/ha)']
    data2['y'] = econ_data.query('p=='+str(p_dynamic)+' and c1=='+str(c1_dynamic)+' and c2=='+str(c2_dynamic))['production (kg)']
    #print(data['y'])
    #print(source.data)

c1_slider.on_change('value', update_data)
c2_slider.on_change('value', update_data)
p_slider.on_change('value', update_data)

#show(plot)

plot1 = figure(x_range =source1.data['x'], y_range=(0, 500), plot_width=400, plot_height=400,
              title = 'Nfert (kg/ha)', toolbar_location=None, tools="")
glyph1 = VBar(x="x", top="y", width=0.9,
          fill_color=factor_cmap('x', palette=Spectral6, factors=x))
plot1.add_glyph(source1, glyph1)

plot2 = figure(x_range =source2.data['x'], y_range=(0, 1000000000), plot_width=400, plot_height=400,
              title = 'production (kg)', toolbar_location=None, tools="")
glyph2 = VBar(x="x", top="y", width=0.9,
          fill_color=factor_cmap('x', palette=Spectral6, factors=x))
plot2.add_glyph(source2, glyph2)

layout = row(
    plot,
    plot1,
    plot2,
    widgetbox(c1_slider, c2_slider, p_slider),
)

curdoc().add_root(layout)