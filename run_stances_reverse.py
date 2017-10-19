#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 10:09:47 2017

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

start_id = 50000
end_id = 60780
k_stances = []
err_row = []

# make directory if not exist
try: os.makedirs('nmt_news')
except: pass

# make file if not exist
try: open('nmt_news/bodies.csv','x')
except FileExistsError: pass

for i in range(end_id,start_id,-1):
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
            with open('nmt_news/stances_reverse.csv','a',encoding='UTF-8',newline='') as f:
                w = DictWriter(f, ['Headline','Body ID','Stance'])
                for k_stance in k_stances:
                    w.writerow(k_stance)   
            print('******* row saved: {} *******'.format((i+1)))
            k_stances = []
    

#%%
nmt.quit_browser()
