#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 17:43:27 2017

@author: jm
"""

#%% import
from dataset import DataSet
from selenium_api import Selenium

import numpy as np
import os

from csv import DictWriter
#%%
dataset = DataSet(name='total')
#e_stances = dataset.stances   # list(dict), dict key: 'Body ID', 'Headline', 'Stance'
e_articles = dataset.articles # dict, {int(Body ID) : articleBody}

max_body_id = max(e_articles.keys()) # 2532 # total: 5586

#%%
nmt = Selenium()

start_id = 1573
end_id = 3002
k_dicts = []
long_body_id = []
err_body_id = [80]

# make directory if not exist
try: os.makedirs('nmt_news')
except: pass

# make file if not exist
try: open('nmt_news/bodies.csv','x')
except FileExistsError: pass

for body_id in range(start_id,max_body_id+1):
    if body_id in e_articles.keys() and body_id not in (80,1375):
        e_article = e_articles[body_id]
        print('body ID: {}, length: {}'.format(body_id, len(e_article)))
            
        if len(e_article)<5000:
            try:
                k_article = nmt.google_translate('', e_article)
               
                k_dict = {'Body ID':body_id, 'articleBody':k_article}
                k_dicts.append(k_dict)
            except Exception as e:
                print(e)
                err_body_id.append(body_id)
        else:
            long_body_id.append(body_id)
        
        # if url is changed to the record one, close and reopen the browser
        if nmt.google_url_changed(''):
            nmt.google_login()
            err_body_id.append(body_id)
        
        # save in .csv file every 10 articles
        if len(k_dicts) == 10:
            with open('nmt_news/bodies.csv','a',encoding='UTF-8',newline='') as f:
                w = DictWriter(f, ['Body ID','articleBody'])
                for k_dict in k_dicts:
                    w.writerow(k_dict)   
            print('******* Body ID saved: {} *******'.format(k_dicts[-1]['Body ID']))
            k_dicts = []

#%%
print (err_body_id)
nmt.quit_browser()
