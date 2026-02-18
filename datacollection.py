import numpy as np
import pandas
import requests
import pickle
import yfinance as yf
import pandas as pd

from config import *


class ticker:
        name = ''
        historyRaw = []
        financialsRaw = []

        def __init__(self,name,data):
            self.financialsRaw = []
            self.name = name
            self.historyRaw = data[name].tolist()


        def history(self,day):
            return self.historyRaw[day]


download = False
data = []
try:
    f = open(data_path,'rb')
    allthing = pickle.load(f)
    f.close()
    for i in range(len(allthing)):
        for j in range(len(allthing[i].historyRaw)):
            value = allthing[i].historyRaw[j]
            flag = isinstance(value,float) and value > 0
            download = not flag
except:
    download = True



if download:
    data = yf.download(sp500b, start=start_date, end=end_date, auto_adjust='true')
    data = data['Close']
    everything = []
    for each in universe:
        everything.append(ticker(each, data))
        print(each)
    f = open(data_path, 'wb')
    pickle.dump(everything, f)
    f.close()














