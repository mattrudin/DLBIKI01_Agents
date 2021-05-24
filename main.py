import SMAVectorBacktester as SMA
import MRVectorBacktester as MR

symbol = 'GLD'
from_date = '2010 1 1'
to_date = '2021 05 21'
smabt = SMA.SMAVectorBacktester(symbol, 42, 252, from_date, to_date)

#smabt.run_strategy()
#smabt.plot_results()
smabt.optimize_parameters((30, 50, 1), (200, 300, 1))
smabt.plot_results()

mrbt = MR.MRVectorBacktester(symbol, from_date, to_date, 10000, 0.001)
mrbt.run_strategy(smabt.SMA1, 3.5)
mrbt.plot_results()
