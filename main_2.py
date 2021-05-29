import datetime

import SMAVectorBacktester as SMA
import MomVectorBacktester as MV
import MRVectorBacktester as MR
import LRVectorBacktester as LR
import ScikitVectorBacktester as SCI

# Underlying Settings
symbol = 'GLD'
from_dt = datetime.datetime(2010, 1, 1)
to_dt = datetime.datetime(2021, 5, 24)
# Backtest Settings
is_print = False
is_plot = False

# SMA Backtest
print('============= SMA Backtest Results =============')
smabt = SMA.SMAVectorBacktester(symbol, from_dt, to_dt)
smabt.optimize_parameters((1, 100, 1), (101, 300, 1))
sma_performance = smabt.run_strategy()
if is_print:
    print('Symbol: ' + symbol)
    print('From: ' + from_dt.strftime("%d %b, %Y"))
    print('To: ' + to_dt.strftime("%d %b, %Y"))
if is_plot:
    smabt.plot_results()
print('Strategy Performance Relative: ' + str(sma_performance[0]))
print('Underlying Performance Relative: ' + str(sma_performance[2]))
print('Best Strategy SMA1: ' + str(smabt.SMA1))
print('Best Strategy SMA2: ' + str(smabt.SMA2))

# Momentum Backtest
initial_credit = 10000
transaction_costs = 0.001  # 0.1%
best_momentum_performance = 0
best_momentum_window = 0
related_underlying_performance = 0
mvbt = MV.MomVectorBacktester(symbol, from_dt, to_dt, initial_credit, transaction_costs)
for i in range(1, 50, 1):
    mv_performance = mvbt.run_strategy(i)
    strategy_performance = round(mv_performance[0] / initial_credit, 2)
    underlying_performance = round(mv_performance[2] / initial_credit, 2)
    if is_print:
        print('')
        print('============= Momentum Backtest =============')
        print('Symbol: ' + symbol)
        print('From: ' + from_dt.strftime("%d %b, %Y"))
        print('To: ' + to_dt.strftime("%d %b, %Y"))
        print('Initial Credit: ' + str(initial_credit))
        print('Rolling window with size: ' + str(i))
        print('Strategy Performance Absolute: ' + str(mv_performance[0]))
        print('Strategy Performance Relative: ' + str(strategy_performance))
        print('Strategy Out-/Underperformance: ' + str(mv_performance[1]))
        print('Underlying Performance Absolute: ' + str(mv_performance[2]))
        print('Underlying Performance Relative: ' + str(underlying_performance))
    if is_plot:
        mvbt.plot_results()
    if strategy_performance > best_momentum_performance:
        best_momentum_performance = strategy_performance
        best_momentum_window = i
        related_underlying_performance = underlying_performance
print('============= Momentum Backtest Results =============')
print('Best Strategy Performance Relative: ' + str(best_momentum_performance))
print('Underlying Performance Relative: ' + str(related_underlying_performance))
print('Best Strategy Window: ' + str(best_momentum_window))

# Mean Reversion Backtest
best_reversion_performance = 0
best_reversion_sma = 0
best_reversion_threshold = 0
related_underlying_performance = 0
mrbt = MR.MRVectorBacktester(symbol, from_dt, to_dt, initial_credit, transaction_costs)
for i in range(1, 50, 1):
    for j in range(1, 20, 1):
        sma = i  # simple moving average (SMA) as a proxy for a “trend path”
        threshold = j  # distance between the current stock price and the SMA, which signals a long or short position.
        mr_performance = mrbt.run_strategy(i, j)
        strategy_performance = round(mr_performance[0] / initial_credit, 2)
        underlying_performance = round(mr_performance[2] / initial_credit, 2)
        if is_print:
            print('============= Mean Reversion Backtest =============')
            print('Symbol: ' + symbol)
            print('From: ' + from_dt.strftime("%d %b, %Y"))
            print('To: ' + to_dt.strftime("%d %b, %Y"))
            print('Initial Credit: ' + str(initial_credit))
            print('Current SMA / Threshold: ' + str(sma) + ' / ' + str(threshold))
            print('Strategy Performance Absolute: ' + str(mr_performance[0]))
            print('Strategy Performance Relative: ' + str(strategy_performance))
            print('Strategy Out-/Underperformance: ' + str(mr_performance[1]))
            print('Underlying Performance Absolute: ' + str(mr_performance[2]))
            print('Underlying Performance Relative: ' + str(underlying_performance))
        if is_plot:
            mrbt.plot_results()
        if strategy_performance > best_reversion_performance:
            best_reversion_performance = strategy_performance
            best_reversion_sma = sma
            best_reversion_threshold = threshold
            related_underlying_performance = underlying_performance
print('============= Mean Reversion Backtest Results =============')
print('Best Strategy Performance Relative: ' + str(best_reversion_performance))
print('Underlying Performance Relative: ' + str(related_underlying_performance))
print('Best Strategy SMA: ' + str(best_reversion_sma))
print('Best Strategy Threshold: ' + str(best_reversion_threshold))
