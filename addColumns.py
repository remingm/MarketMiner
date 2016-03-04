import csv
import talib
import pandas as pd
import numpy as np

stockData = pd.read_csv('sp66yrs.csv').drop('Adj Close', axis=1)
#stockData = pd.read_csv('aaplTestHourly6month.csv')


#data = np.array([1.34589,1.33162,1.2234], numpy.float)
closeNdarray = np.array(stockData['Close'].values, np.float)

timeStats = 7
predFuture = 1

stockData['RSI'] = talib.RSI(closeNdarray, timeperiod = timeStats)
BBupper, garbage, BBlower = talib.BBANDS(closeNdarray, timeperiod = timeStats)
stockData['BBandUpper'] = BBupper
stockData['BBandLower'] = BBlower
stockData['CMOData'] = talib.CMO(closeNdarray, timeperiod = timeStats)
stockData['DMIData'] = talib.DX(high=stockData['High'].values,low=stockData['Low'].values, close=closeNdarray, timeperiod = timeStats)
stockData['MFI'] = talib.MFI(high=stockData['High'].values,low=stockData['Low'].values, close=closeNdarray, volume=stockData['Volume'].values.astype(float), timeperiod = timeStats)
stockData['MA'] = talib.MA(closeNdarray, timeperiod = timeStats)
stockData['STDDEV'] = talib.STDDEV(closeNdarray, timeperiod = timeStats)

stockData['futureClose'] = stockData['Close'].shift(-predFuture)

stockData['futureDif'] = stockData['Close'].diff(-predFuture) * -1
stockData['futureDif%'] = stockData['Close'].pct_change(-predFuture) * -1


# -1 if down, 1 if up
upDown = []
tomDif =  stockData['futureDif']
for row in tomDif:
	if row > 0:
		upDown.append(1)
	else:
		upDown.append(-1)
stockData['upDown'] = np.array(upDown)





stockData = stockData[timeStats:-predFuture]

stockData.to_csv('sp66yrsNewCols.csv')

print stockData.describe()
#print stockData['RSI']


#couldn't find function for intraday momentum index
#money flow index
