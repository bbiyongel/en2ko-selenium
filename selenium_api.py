# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 14:15:13 2017

@author: USER
"""

#%% import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

import config as config

#%%
class Selenium():
    def __init__(self):
        aa = os.getcwd().split(os.sep)
        self.driver_path = os.path.join((os.sep).join(aa[:-1]),'chromedriver')
        
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--no-sandbox')
        self.open_browser()
    
    def open_browser(self):
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=self.chrome_options)
        self.driver.implicitly_wait(3)
        self.google_login()
        
    def naver_login(self):
        self.driver.get('https://nid.naver.com/nidlogin.login')
        self.driver.find_element_by_id('id').send_keys(config.naver['login'])
        self.driver.find_element_by_id('pw').send_keys(config.naver['passwd'])
        self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
        time.sleep(1)
        self.driver.get('https://papago.naver.com')
    
    def google_login(self):
        self.driver.get('https://translate.google.co.kr/m/translate?hl=ko')
    
    def naver_translate(self,event,eng):
        self.driver.find_element_by_id('txtSource').send_keys(eng)
        time.sleep(0.5)
        self.driver.find_element_by_id('btnTranslate').click()
        time.sleep(5)
        kor = self.driver.find_element_by_id('targetEditArea').text

        self.driver.find_element_by_id('txtSource').send_keys(Keys.CONTROL + "a")
        self.driver.find_element_by_id('txtSource').send_keys(Keys.DELETE);
        return kor

    def google_translate(self,event,eng):
        self.driver.find_element_by_id('source').send_keys(eng)
        time.sleep(0.5)
        self.driver.find_element_by_class_name('go-wrap').click()
        time.sleep(1)
        kor = self.driver.find_element_by_class_name('translation').text
        
        # clear source text field
        self.driver.find_element_by_id('source').send_keys(Keys.CONTROL + "a")
        self.driver.find_element_by_id('source').send_keys(Keys.DELETE);
        return kor
    
    def google_url_changed(self,event):
        if self.driver.current_url == 'https://translate.google.co.kr/m/translate?hl=ko#op=showhistory':
            return True
        else:
            return False
        
    def google_clear_record(self,event):
        buttons = self.driver.find_elements_by_class_name('ft-icon-img-ctr')
        buttons[0].click()
        
        self.driver.find_element_by_class_name('clearall-label').click()
        
        alert = self.driver.switch_to_alert()
        print(alert.text)
        alert.accept()
        
        self.driver.find_element_by_class_name('toolbar-back-arrow').click()
        time.sleep(0.5)
    
    def quit_browser(self):
        self.driver.quit()
        time.sleep(0.5)
        
