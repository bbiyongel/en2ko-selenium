#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 18:52:39 2017

@author: jm
"""

#%% import
from dataset import DataSet, extract_sub_stances
from selenium_api import Selenium

import numpy as np
import os

from csv import DictWriter
#%%
dataset = DataSet(name='total')
e_stances = dataset.stances   # list(dict), dict key: 'Body ID', 'Headline', 'Stance'
# len(e_stances) = 75385
# length for not 'discuss' : 62088

#e_articles = dataset.articles # dict, {int(Body ID) : articleBody}

#%%
nmt = Selenium()

start_id = 35469
end_id = 50001
k_stances = []
err_row = []

# make directory if not exist
try: os.makedirs('nmt_news')
except: pass

# make file if not exist
try: open('nmt_news/stances.csv','x')
except FileExistsError: pass

for i in range(start_id,end_id):
        e_stance = e_stances[i]
        if e_stance['Stance'] == 'discuss':
            continue
        
        print('row: {}, Body ID: {}'.format((i+1), e_stance['Body ID']))
        
        try:
            k_headline = nmt.google_translate('', e_stance['Headline'])
           
            k_stance = {'Headline':k_headline,
                        'Body ID':e_stance['Body ID'],
                        'Stance':e_stance['Stance']}
            k_stances.append(k_stance)
        except Exception as e:
                print(e)
                err_row.append(i)
        
        # save in .csv file every 20 articles
        if len(k_stances) == 20:
            with open('nmt_news/stances.csv','a',encoding='UTF-8',newline='') as f:
                w = DictWriter(f, ['Headline','Body ID','Stance'])
                for k_stance in k_stances:
                    w.writerow(k_stance)   
            print('******* row saved: {} *******'.format((i+1)))
            k_stances = []
    
        # for google translate, we should periodically reopen
#        if np.mod(len(k_dicts),100) == 0:
#            nmt.quit_browser()
#            nmt.open_browser()
#            print('quit and reopen the browser')
        
#%%
'''
# check
for bid, body in enumerate(k_dicts):
    print(body)
    print('\n\n ******************\n\n')

        
# save in .csv file
open_mode = 'w' # w: write, a: append
with open('nmt_news/GNMT/bodies.csv',open_mode,encoding='UTF-8',newline='') as f:
    w = DictWriter(f, ['Body ID','articleBody'])
    if open_mode=='w':
        w.writeheader()
    for k_dict in k_dicts:
        print(k_dict['Body Id'])
        w.writerow(k_dict)
'''
#%%
nmt.quit_browser()
