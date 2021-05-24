#
# Python Module with Class
# for Vectorized Backtesting
# of Momentum-Based Strategies
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class MomVectorBacktester(object):
    ''' Class for the vectorized backtesting of
    momentum-based trading strategies.
    Attributes
    ==========
    symbol: str
    RIC (financial instrument) to work with
    start: str
    start date for data selection
    end: str
    end date for data selection
    amount: int, float
    amount to be invested at the beginning
    tc: float
    proportional transaction costs (e.g., 0.5% = 0.005) per trade
    Methods
    =======
    get_data:
    retrieves and prepares the base data set
    run_strategy:
    runs the backtest for the momentum-based strategy
    plot_results:
    plots the performance of the strategy compared to the symbol
    '''

    def __init__(self, symbol, start, end, amount, tc):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.amount = amount
        self.tc = tc
        self.results = None
        self.get_data()

    def get_data(self):
        ''' Retrieves and prepares the data.
        '''
        from_mili = f'{self.start.timestamp():.0f}'
        to_mili = f'{self.end.timestamp():.0f}'
        url = 'https://query1.finance.yahoo.com/v7/finance/download/' + self.symbol + '?period1=' + from_mili + '&period2=' + to_mili + '&interval=1d&events=history&includeAdjustedClose=true'
        raw = pd.read_csv(url, index_col=0, parse_dates=True).dropna()
        raw = pd.DataFrame(raw['Adj Close'])
        raw = raw.loc[self.start:self.end]
        raw.rename(columns={'Adj Close': 'price'}, inplace=True)
        raw['return'] = np.log(raw / raw.shift(1))
        self.data = raw

    def run_strategy(self, momentum=1):
        ''' Backtests the trading strategy.
        '''
        self.momentum = momentum
        data = self.data.copy().dropna()
        data['position'] = np.sign(data['return'].rolling(momentum).mean())
        data['strategy'] = data['position'].shift(1) * data['return']
        # determine when a trade takes place
        data.dropna(inplace=True)
        trades = data['position'].diff().fillna(0) != 0
        # subtract transaction costs from return when trade takes place
        data['strategy'][trades] -= self.tc
        data['creturns'] = self.amount * data['return'].cumsum().apply(np.exp)
        data['cstrategy'] = self.amount * \
                            data['strategy'].cumsum().apply(np.exp)
        self.results = data
        # absolute performance of the strategy
        aperf = self.results['cstrategy'].iloc[-1]
        # out-/underperformance of strategy
        operf = aperf - self.results['creturns'].iloc[-1]
        # gross performance of the underlying
        uperf = self.results['creturns'].iloc[-1]
        return round(aperf, 2), round(operf, 2), round(uperf, 2)

    def plot_results(self):
        ''' Plots the cumulative performance of the trading strategy
        compared to the symbol.
        '''
        if self.results is None:
            print('No results to plot yet. Run a strategy.')
        title = '%s | TC = %.4f' % (self.symbol, self.tc)
        self.results[['creturns', 'cstrategy']].plot(title=title,
                                                     figsize=(10, 6))
        plt.show()
