# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 13:41:01 2021

@author: Alfredo y Antonio


Program Description: 
    
Phone Validator Automatation using Google Chrome Web Driver
https://sites.google.com/a/chromium.org/chromedriver/downloads
"""
#PREPARING THE ENVIROMENT

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np 
import time
import requests
from bs4 import BeautifulSoup
import random

#Define path where the Google Web Driver .exe file is

def get_proxy():
            
    res = requests.get('https://free-proxy-list.net/', headers={'user-agent':'my-app'})
    soup = BeautifulSoup(res.text,'lxml')
    proxy_list = []
    for items in soup.select('.table.table-striped.table-bordered > tbody tr'):
        proxy = ':'.join([item.text for item in items.select('td')[:2]])
        proxy_list.append(proxy)
    
    return proxy_list

######################     SETUP      ##########################

PATH = 'C:\Program Files (x86)\chromedriver.exe'
file_path = r'C:\Users\Alfredo y Antonio\Box\Infusion Advisors\05.00 Data Management Research and Development\06.00 Lead Data\13. New Leads Zoho\VC Investor list for Vivacitas Phone number.csv'
df = pd.read_csv(file_path, encoding='unicode_escape')
 
 
#Convert Phone column into string
df['Phone'] = df['Phone'].astype(str)
# Add Phone Validator Column with zeros
df['Phone Validator']='empty'
idx_empty = list(df[df['Phone Validator']=='empty'].index.values)


# Loop to fill the data
while len(idx_empty) > 0:
    #Define Driver to use, in this case Chrome
    driver = webdriver.Chrome(PATH)
    #Define Website to Access
    driver.get('https://www.numberguru.com/')
    
    for i in idx_empty:
        
        try:
            #Find and input Phone Numbers in the Search Bar
            search = driver.find_element_by_id('phone-number')
            search.send_keys(df.loc[i,'Phone'])
            search.send_keys(Keys.RETURN)
            
            #Extract Info from Phone Number Info
            phone_info = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "info-widget-details")))
            
            info_list = phone_info.text.split('\n')
            phone_type = info_list[7]
            df.loc[i,'Phone Validator'] = phone_type
            idx_empty = list(df[df['Phone Validator']=='empty'].index.values)
            print(df.loc[i,'Phone'])
            print(phone_type)
            print()
            print('{:.2f}% Completed'.format(((len(df)-len(idx_empty))/len(df))*100))
            print(f'{len(df)-len(idx_empty)} out of {len(df)}')
            print()
            driver.find_element_by_id('phone-number').clear()
            
        except Exception as error:
            print(error)
    df['Phone Validator'] = df['Phone Validator'].str.upper()
    df['Phone Validator'] = df['Phone Validator'].apply(lambda x: 'CELL PHONE' if x=='MOBILE')

#convert into csv file
df.to_csv('Vivacitas_VC_Phone_Numbers_Validator.csv')
print(df)
