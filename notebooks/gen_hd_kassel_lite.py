#!/usr/bin/env python
# coding: utf-8

# # Hassediagram für Kassel

import pathlib
from pyhasse.core.csv_io import CSVReader
from pyhasse.core.order import Order
from pyhasse.core.hddata import HDData
import json
from IPython.core.display import display, HTML
from string import Template
import hd3d_lib

TESTFILENAME = '/csvdata/kassel1.txt'

HERE = pathlib.Path('__file__').parent
csv = CSVReader(fn=str(HERE) + TESTFILENAME, ndec=3)
red = csv.calc_reduced_system()

hd = HDData(csv)
data_dict = hd.jsondata()
data_dict['dmred'] = csv.dmred
selected_obj = ''
data_dict['lst_downsets'] = []
data_dict['lst_upsets'] = []
data_dict['lst_incomparables'] = []
    
settings = {
    "preselected": [],
    "arrowShow": 1,
    "unselectedHide": 0,
    "edgeHighlight": 1,
    "arrowWidth": 20,
    "arrowSideRight": 1,
    "unselectedNodeColor": "#00ff00",
    "selectedNodeColor": "#ffbfff",
    "arrowColor": "#ff0000",
    "textColor": "#000000",
    "lineColor": "#FFF",
    "selectedBkgColor": "#008",
    "bkgGradient1": "#2db4ff",
    "bkgGradient2": "#2db4ff",
    "shortLength": 4,
    "hNodeDist": 2,
    "vNodeDist": 2,
    "r": 20,         # node size
    "bkgR": 15,  # background upset/downset
    "frameHeight": 600
}

data_dict.update(settings)


precision = 4
order = Order(csv.dmred,
              csv.redrows,
              csv.cols)
zeta = order.calc_relatmatrix(
    datamatrix=csv.dmred,
    rows=csv.redrows,
    cols=csv.cols,
    prec=precision)
data_dict['lst_downsets'] = order.calc_downset(zeta, csv.redrows)
data_dict['lst_upsets'] = order.calc_upset(zeta, csv.redrows)


# set a startnode to visualize connections
node = ''
data_dict['preselected'] = []
if node != '':
    node_index = data_dict['lst_obj_red'].index(node)
    # Upsets
    upsets = [data_dict['lst_obj_red'][i] for i in data_dict['lst_upsets'][node_index]]
    # Downset
    downsets = [data_dict['lst_obj_red'][i] for i in data_dict['lst_downsets'][node_index]]
    
eqm = csv.generate_eqcl(csv.obj,csv.eqm)



