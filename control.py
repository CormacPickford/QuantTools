import datetime
from math import isnan
from datetime import date

import dbinterface
from metrics import Portfolio
from alphaenv import verbose
import pandas as pd
from dbinterface import *
from config import *
from alphaenv import active,sellall,getdata
from datacollection import *
from optim import EnsembleOptimiser

period = 0
equity_count = 0

for every in allthing:
    flagged = False
    for each in every.historyRaw:
        if isnan(each):
            flagged = True
    if flagged:
        if verbose == True: print(every.name)
        allthing.remove(every)

choice = input('Run active alpha or load alpha? r/l ')
if choice == 'l':
    idx = int(input('ID? '))
    active, _ = read_alpha_and_entry(idx)

period_max = (formatted_end_date - formatted_start_date).days
equity_max = len(allthing)

passed = False
while not passed:
    passed = True
    period= int(input('How many days to run the test for? '))
    equity_count = int(input('How many stock tickers to run over? '))
    if period > period_max:
        period = period_max
    if equity_count > equity_max:
        equity_count = equity_max
    try:
        if period in range(0,period_max+1) and equity_count in range(0,equity_max+1):
            pass
        else:
            print('Provide positive integers')
            passed = False
    except:
        print('Provide positive integers')
        passed = False


portfolio  = Portfolio()
for day in range(0, period):

    if verbose == True: print(day)
    for i in range(0,equity_count):
        active(allthing[i].name,allthing[i].historyRaw[:day+1],day,i,portfolio)
    portfolio.p_update(allthing,day)

sellall(len(allthing[0].historyRaw)-1,portfolio)
print(list(map(lambda x: round(float(x), 5), portfolio.p_report)))
print(f' You made a return of {((portfolio.p_report[-1]-1)*100):.3f} %')
portfolio.calc_daily_sharpe()
print(f' Daily sharpe_ratio was {portfolio.daily_sharpe_ratio:.4f}')
portfolio.calc_real_sharpe()
print(f' Per-trade sharpe_ratio was {portfolio.real_sharpe:.4f}')


save = input('Would you like to save alpha? y/n ')
if save == 'y':
    name = input('With name? ')
    dbinterface.writeAlpha(name,portfolio.daily_sharpe_ratio,portfolio.real_sharpe,portfolio.p_report,active)

optim = input('Recalc optimised ensemble? y/n ')
if optim == 'y':
    conn = sqlite3.connect('alphaDB.db')
    cur = conn.cursor()
    cur.execute('SELECT MAX(ID) FROM alphadb')
    max_id_row = cur.fetchone()
    last_id = max_id_row[0]
    alpha_space = pd.DataFrame(columns=['id','name','dsharpe','rsharpe','report'])
    for i in range(1,last_id+1):
        _, row = read_alpha_and_entry(i)
        alpha_space.loc[len(alpha_space)] = {'id': i,'name': row[1],'dsharpe': row[2],'rsharpe': row[3],'report' : json.loads(row[4])}
    returns = list(alpha_space['report'])
    for a in range(len(returns)):
        for b in range(len(returns[a])):
            returns[a][b] -=1
    starting_weights = [1/last_id for j in range(last_id)]
    model = EnsembleOptimiser(returns,starting_weights)
    for i in range(4000):
        model.update_weights()
        if verbose: print(model.sharpe)
    print(model.weights)



