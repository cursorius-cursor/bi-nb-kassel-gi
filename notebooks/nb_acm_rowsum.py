#!/usr/bin/env python
# coding: utf-8

# # What can pyhasse.acm be used for?

# ### Objectives
# 
# Analysis of conflicts (Antichain: a subset of the set of objects, mutually incomparable)
# 
# ### Let's calculate the rowsum
# 
# Number of conflicting indicator pairs, concerning a given object pair. (row sum)

# ### Import all necessary libraries

# In[1]:


import pathlib
from pyhasse.core.csv_io import CSVReader
from pyhasse.core.hddata import HDData
import json
import random
from IPython.core.display import display, HTML
from string import Template
import hd3d_lib
from pyhasse.acm.calc import ACM


# ### load library for visualisation

# In[2]:


HTML('<script src="lib/d3/d3.min.js"></script>')


# ### Note:
# 
# start: all bars whose length >= 'start' will be visible
# 
# stop:  all bars whose length <= 'stop' will be shown
# 

# In[3]:


##second exmple set
#TESTFILENAME = '/csvdata/chain_pollution.csv'
#prefs={
#    'start': 4,
#    'stop': 21,
#    'user_list' : [],
#    'labelLen': 3,
#    'actwidth': 550,
#    'actheight': 200
#}


# ### Preparing the data

# In[4]:


prefs={
    'start': 0,  # all bars with values between 'start'...
    'stop': 4,   # and 'stop' will be shown. To avoid trivial results it is recommended
                 # to select start '1' . Note: if stop '2' then bars whose length > 2 will
                 # not be visible. 
    'user_list' : [],
    'labelLen': 3,
    'actwidth': 550,
    'actheight': 200
}
TESTFILENAME = '/csvdata/kassel1.txt'
HERE = pathlib.Path('__file__').parent
csv = CSVReader(fn=str(HERE) + TESTFILENAME, ndec=3)
red = csv.calc_reduced_system()
acm = ACM(csv.data, csv.rows, csv.cols)
prefs['user_list'] = csv.objred


#  ### Basic calculations
# 

# In[5]:


px, pq = acm.generate_setofpairs(csv.objred, prefs['user_list'])
px, qp = acm.generate_setofpairs(csv.objred, csv.objred)
acm.calc_acm(px, pq)
rowsumacm, colsumacm = acm.calc_obj_attprofile()
maxrowsum, maxcolsum = acm.calc_optimum()
mobjobj, mattatt = acm.find_optimalpairs(px, pq)
ac = acm.calc_acm(px, pq)
#ac


# In[6]:


name_ordinate1, name_ordinate2, labels_obj, labels_att, labelmaxobj, labelmaxatt = acm.acm_graphics(csv.objred, csv.prop)

#labels_obj
#labels_att


# ### Prepare the data for visualisation

# In[7]:


data = '[\n'
for k,v in prefs.items():
    data += "var {} = {};\n".format(k,v)
data += ']\n'
# print(data)

tmpl = '{{"legendLabel": "{0}", "magnitude": {1}}},'
ll = prefs['labelLen']
rowsum, colsum = acm.calc_obj_attprofile()
data = '['
for x in range(0, len(rowsum)):
    if rowsum[x] in range(prefs['start'], prefs['stop']+1):
        l1 = labels_obj[x][0][:ll]
        l2 = labels_obj[x][1][:ll]
        value = str(rowsum[x])
        data += tmpl.format("{} - {}".format(l1, l2), value)
data += "];"
#data


# In[8]:


#HTML(hd3d_lib.draw_graph('acm_rowsum',{'data': data}))

acm_with_labels = [[' '] + labels_att]
for i in range(len(ac)):
   acm_with_labels.append([labels_obj[i]] + ac[i])

ppmatrix = ""
for line in acm_with_labels:
    for item in line:
        ppmatrix += f'{str(item):^12}'
    ppmatrix += '\n'
