import csv
import talib
import pandas as pd
import numpy as np

stockData = pd.read_csv('sp66yrs.csv').drop('Adj Close', axis=1)
#stockData = pd.read_csv('aaplTestHourly6month.csv')


#data = np.array([1.34589,1.33162,1.2234], numpy.float)
closeNdarray = np.array(stockData['Close'].values, np.float)

timeP = 14

stockData['RSI'] = talib.RSI(closeNdarray, timeperiod = timeP)
BBupper, garbage, BBlower = talib.BBANDS(closeNdarray, timeperiod = timeP)
stockData['BBandUpper'] = BBupper
stockData['BBandLower'] = BBlower
stockData['CMOData'] = talib.CMO(closeNdarray, timeperiod = timeP)
stockData['DMIData'] = talib.DX(high=stockData['High'].values,low=stockData['Low'].values, close=closeNdarray, timeperiod = timeP)
stockData['MFI'] = talib.MFI(high=stockData['High'].values,low=stockData['Low'].values, close=closeNdarray, volume=stockData['Volume'].values.astype(float), timeperiod = timeP)
stockData['MA'] = talib.MA(closeNdarray, timeperiod = timeP)
stockData['STDDEV'] = talib.STDDEV(closeNdarray, timeperiod = timeP)

stockData['TomorrowClose'] = stockData['Close'].shift(-1)

stockData['TomorrowDif'] = stockData['Close'].diff(-1)
stockData['TomorrowDif%'] = stockData['Close'].pct_change(-1) * -100.0

upDown = []
tomDif =  stockData['TomorrowDif']
for row in tomDif:
	if row > 0:
		upDown.append(1)
	else:
		upDown.append(-1)
stockData['upDown'] = np.array(upDown)

stockData = stockData[timeP:-1]

stockData.to_csv('sp66yrsNewCols.csv')

print stockData.describe()
#print stockData['RSI']


#couldn't find function for intraday momentum index
#money flow index
