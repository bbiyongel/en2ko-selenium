# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 23:36:25 2017

@author: USER
"""
#%% import
import urllib.request
import ast

import config as config

#%%
def translate(english):
    client_id = config.papago['client_id']
    client_secret = config.papago['client_secret']
    encText = urllib.parse.quote(english)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
#        print(response_body.decode('utf-8'))
        json_translated = response_body.decode('utf-8') # str
        json_translated = ast.literal_eval(json_translated) # str2dict
        translated = json_translated['message']['result']['translatedText']
        return translated
    else:
        print("Error Code:" + rescode)