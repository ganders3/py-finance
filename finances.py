#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 15:09:52 2020

@author: gregory
"""

import json, urllib
from bs4 import BeautifulSoup
from pycoingecko import CoinGeckoAPI
import yfinance as yf

FNAME_CRYPTO = 'balances-crypto.json'
FNAME_STOCKS = 'balances-stocks.json'
FNAME_METALS = 'balances-metals.json'
METALS_URL = 'https://www.kitco.com/charts/live***.html' #'https://www.apmex.com/xxx-price'

def find(list, ind, val):
    for cl in coinsList:
        if cl[ind] == val:
            return cl
    return {}
    
cg = CoinGeckoAPI()
coinsList = cg.get_coins_list()

https://www.kitco.com/charts/live***.html
with open(FNAME_CRYPTO) as f:
  crypto = json.load(f)
  
totalCrypto = 0
for c in crypto:
#    coin = find(coinsList, 'symbol', c)
    gp = cg.get_price(c, 'usd')
    key = list(gp.keys())[0]
    price = gp[key]['usd']
    value = price*crypto[c]
    print(c, ': ', '${:0,.2f}'.format(float(value)), sep = '')
    totalCrypto += value

#"{:0,.2f}".format(float(your_numeric_value))
with open(FNAME_STOCKS) as f:
    stocks = json.load(f)
  
print('-'*10)        
print('total crypto:', '${:0,.2f}'.format(float(totalCrypto)))
print('-'*10)

totalStocks = 0
for s in stocks:
    price = yf.Ticker(s).history().tail(1)['Open'][0]
    value = price*stocks[s]
    print(s, ': ', '${:0,.2f}'.format(float(value)), sep = '')
    totalStocks += value
    
print('-'*10)        
print('total stocks:', '${:0,.2f}'.format(float(totalStocks)))
print('-'*10)



with open(FNAME_METALS) as f:
    metals = json.load(f)
    
totalMetals = 0
for m, types in metals.items():
    totalWeight = 0
    for t, q in types.items():
        totalWeight += q['quantity']*q['weight']
    
    url = METALS_URL.replace('***', m)
    htmlRead = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(htmlRead, 'html.parser')
    price = soup.find(id = 'sp-bid')
    price = float(price.contents[0].replace(',', ''))
    value = price*totalWeight
    print(m, ': ', '${:0,.2f}'.format(float(value)), sep = '')
    totalMetals += value

print('-'*10)        
print('total metals:', '${:0,.2f}'.format(float(totalMetals)))
print('-'*10)

total = totalCrypto + totalStocks + totalMetals
print('='*10)
print('total:', '${:0,.2f}'.format(float(total)))