import csv
import talib
import pandas as pd
import numpy as np

stockData = pd.read_csv('sp66yrs.csv').drop('Adj Close', axis=1)
#stockData = pd.read_csv('aaplTestHourly6month.csv')


#data = np.array([1.34589,1.33162,1.2234], numpy.float)
closeNdarray = np.array(stockData['Close'].values, np.float)

# Global Parameters
timeStats = 7
predFuture = 1
high = stockData["High"].values
low = stockData["Low"].values
close = stockData["Close"].values
open = stockData["Open"].values
volume = stockData["Volume"].values.astype(float)

#Indicators
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


#Momentum Indicators
#http://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
stockData['ADX'] = talib.ADX(high, low, close, timeperiod=14)
stockData['ADXR'] = talib.ADXR(high, low, close, timeperiod=14)
stockData['APO'] =talib.APO(close,  fastperiod=12, slowperiod=26, matype=0)
aroondown, aroonup = talib.AROON(high, low, timeperiod=14)
stockData['aroondown'] = aroondown
stockData['aroonup'] = aroonup
stockData["aroonosc"]= talib.AROONOSC(high, low, timeperiod=14)
stockData['BOP']= talib.BOP(open, high, low, close)
stockData['CCI'] = talib.CCI(high, low, close, timeperiod=14)
stockData['CMO'] = talib.CMO(close, timeperiod=14)
stockData['DX'] = talib.DX(high, low, close, timeperiod=14)
macd, macdsignal, macdhist = talib.MACDFIX(close, signalperiod=9)
stockData['macd'] = macd
stockData['macdsignal'] = macdsignal
stockData['MFI'] = talib.MFI(high, low, close, volume, timeperiod=14)
stockData["minus_di"] = talib.MINUS_DI(high, low, close, timeperiod=14)
stockData["minus_dm"] = talib.MINUS_DM(high, low, timeperiod=14)
stockData["momentum"] = talib.MOM(close, timeperiod=10)
stockData["plus_di"] = talib.PLUS_DI(high, low, close, timeperiod=14)
# stockData["plus_dm"] = talib.PLUS_DM(high, low, close, timeperiod=14) #Getting error with this one
stockData["PPO"] = talib.PPO(close, fastperiod=12, slowperiod=26, matype=0)
stockData['ROC'] = talib.ROC(close, timeperiod=10)
stockData['ROCP'] = talib.ROCP(close, timeperiod=10)
stockData['ROCR'] = talib.ROCR(close, timeperiod=10)
stockData['RSI'] = talib.RSI(close, timeperiod = timeStats)
slowk, slowd = talib.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
stockData['stoch_slowk'] = slowk
stockData['stoch_slowd'] = slowd
fastk, fastd = talib.STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
stockData['stoch_fastk'] = fastk
stockData['stoch_fastd'] = fastd
fastk, fastd = talib.STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
stockData['stochrsi_fastk'] = fastk
stockData['stochrsi_fastd'] = fastd
stockData['TRIX'] = talib.TRIX(close, timeperiod=30)
stockData['ULTOSC'] = talib.ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
stockData['WILLR'] = talib.WILLR(high, low, close, timeperiod=14)


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
