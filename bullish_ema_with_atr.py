import talib
import pandas as pd
import statistics

from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover


class AtrWithEma(Strategy):
    def init(self):
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.ema = self.I(talib.EMA, self.data.Close, 15)
        self.median_atr = statistics.median(self.atr)

    def next(self):
        if crossover(self.data.Close, self.ema): 
            self.buy()
        elif crossover(self.ema, self.data.Close) and self.atr > self.median_atr:
            self.position.close()

bt = Backtest(GOOG, AtrWithEma, cash = 10_000)
stats = bt.run()
print(stats)
bt.plot()
