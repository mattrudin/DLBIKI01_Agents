import datetime

import LRVectorBacktester as LR
import ScikitVectorBacktester as SCI

# Underlying Settings
symbol = 'GLD'
from_dt = datetime.datetime(2010, 1, 1)
to_dt = datetime.datetime(2021, 5, 24)
# Backtest Settings
is_print = False
is_plot = False
initial_credit = 10000
transaction_costs = 0.001  # 0.1%
related_underlying_performance = 0
from_dt_training = from_dt
to_dt_training = datetime.datetime(2015, 12, 31)
from_dt_eval = datetime.datetime(2016, 1, 1)
to_dt_eval = to_dt
is_training_and_eval_same = False

# Linear Regression Backtests
best_regression_performance = 0
best_regression_lags = 0
lrbt = LR.LRVectorBacktester(symbol, from_dt_training, to_dt_eval, initial_credit, transaction_costs)
for i in range(1, 50, 1):
    if is_training_and_eval_same:
        lr_performance = lrbt.run_strategy(from_dt_training, to_dt_eval, from_dt_training, to_dt_eval, i)
    else:
        lr_performance = lrbt.run_strategy(from_dt_training, to_dt_training, from_dt_eval, to_dt_eval, i)
    strategy_performance = round(lr_performance[0] / initial_credit, 2)
    underlying_performance = round(lr_performance[2] / initial_credit, 2)
    if is_plot:
        lrbt.plot_results()
    if strategy_performance > best_regression_performance:
        best_regression_performance = strategy_performance
        best_regression_lags = i
        related_underlying_performance = underlying_performance
print('============= Linear Regression Backtest Results =============')
print('Best Strategy Performance Relative: ' + str(best_regression_performance))
print('Underlying Performance Relative: ' + str(related_underlying_performance))
print('Best Strategy Lags: ' + str(best_regression_lags))

# Classification Backtests
best_classification_performance = 0
best_classification_lags = 0
related_underlying_performance = 0
scibt = SCI.ScikitVectorBacktester(symbol, from_dt_training, to_dt_eval,
                                   initial_credit, transaction_costs)
for i in range(1, 100, 1):
    if is_training_and_eval_same:
        sc_performance = scibt.run_strategy(from_dt_training, to_dt_eval, from_dt_training, to_dt_eval, i)
    else:
        sc_performance = scibt.run_strategy(from_dt_training, to_dt_training, from_dt_eval, to_dt_eval, i)
    strategy_performance = round(sc_performance[0] / initial_credit, 2)
    underlying_performance = round(sc_performance[2] / initial_credit, 2)
    if is_plot:
        scibt.plot_results()
    if strategy_performance > best_classification_performance:
        best_classification_performance = strategy_performance
        best_classification_lags = i
        related_underlying_performance = underlying_performance
print('=============  Classification Backtest Results =============')
print('Best Strategy Performance Relative: ' + str(best_classification_performance))
print('Underlying Performance Relative: ' + str(related_underlying_performance))
print('Best Strategy Lags: ' + str(best_classification_lags))
