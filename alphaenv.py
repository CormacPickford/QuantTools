import math
import random
from config import *
import copy

verbose = False
from mechanics import *


def tanh_reversion(ticker, history, day, i,portfolio):
    sell(ticker, history, day, portfolio)
    if day > 0:
        change = ((history[day] - history[day - 1]) / history[day - 1])
        try:
            direction = -1 * 1 / 2 * math.log((1 + change) / (1 - change), math.e)
        except:
            return

        direction = - change
        if direction > 0:
            buy(ticker,day,direction/8,'long',i,portfolio)
        else:
            buy(ticker,day,-direction/24,'short',i,portfolio)

def random_strategy(ticker,history,day,i,portfolio):
     ran = random.random()
     if ran < 0.15:
         buy(ticker,day,random.random()/100,'long',i,portfolio)
     elif ran > 1:
         buy(ticker, day, random.random() / 100, 'short',i,portfolio)
     if (ran < 0.7 )& (ran > 0.3):
         sell(ticker,history,day,portfolio)

def constricted_momentum(ticker,history,day,i,portfolio):
    if day == 0:
        return

    change = (history[day] - history[day - 1]) / history[day - 1]

    threshold = 0.01

    if change > threshold:
        buy(ticker,day,0.02,'long',i,portfolio)

    elif change < -threshold:
        buy(ticker,day,0.02,'short',i,portfolio)
    else:
        sell(ticker,history,day,portfolio)

def week_momentum(ticker,history,day,i,portfolio):
    if day < 6:
        return

    ma_short = sum(history[day-2:day+1]) / 3
    ma_long = sum(history[day-5:day+1]) / 6

    if ma_short > ma_long:
        sell(ticker,history,day,portfolio)

        buy(ticker,day,0.02,'long',i,portfolio)
    elif ma_short < ma_long:
        sell(ticker,history,day,portfolio)

        buy(ticker,day,0.02,'short',i,portfolio)


active = copy.deepcopy(constricted_momentum)
