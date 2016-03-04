import csv
import talib
import pandas as pd
import numpy as np

stockData = pd.read_csv('sp66yrsNewCols.csv')
futureDif = stockData['futureDif']

predicting = 'futureDif%'
pred = stockData['PRED:'+predicting]
actual = stockData[predicting]
rsi = stockData['RSI']

#predTomorrowDif = stockData['PRED:TomorrowDif']
#predTomorrowDifP = stockData['PRED:TomorrowDif%']
closePrices = stockData['Close']
#dates = closePrices['Date']

longSuccesses = 0
totalLongs = 0

shortSuccesses = 0
totalShorts = 0

transactSuccesses = 0
totalTransacts = 0

cash = 0
shares = 0
tempBoughtCost = 0
lossTotal = 0
gainTotal = 0
minCash = cash

netWorth = 0 
minNetWorth = 0
maxNetWorth = 0

size = len(closePrices)
for i in range (1, size):
	#if ((predTomorrowDif[i] + closePrices[i])/closePrices[i])  > 1.001: #predicts up by 0.5% by tomorrow


	if pred[i] > 0.05:
	#if float(closePrices[i])/float(closePrices[i-1]) < .97:
	#if rsi[i] < 30:
		cash -= closePrices[i]
		shares += 1

		tempBoughtCost += closePrices[i]

		if minCash > cash:
			minCash = cash
		#tempBoughtCost += closePrices[i]
		#cash += futureDif[i] * pred[i] * 100.0
		#shares-=

		if futureDif[i] > 0:
			longSuccesses += 1
		totalLongs +=1



	elif shares > 0 and pred[i] < -0.03:
	#elif shares > 0 and float(closePrices[i])/float(closePrices[i-1]) > 1.007:
	#elif shares > 0 and rsi[i] > 70:

		if tempBoughtCost < closePrices[i] * shares:
			transactSuccesses += 1
			print "profitable", closePrices[i]*shares -tempBoughtCost, i
			print shares
			gainTotal += closePrices[i]*shares - tempBoughtCost
		else:
			print "not profitable", closePrices[i]*shares -tempBoughtCost, i
		totalTransacts += 1

		cash += closePrices[i] * shares
		shares = 0
		tempBoughtCost = 0


	netWorth = cash + closePrices[i] * shares
	if netWorth < minNetWorth:
		minNetWorth = netWorth
	elif netWorth > maxNetWorth:
		maxNetWorth = netWorth

		#print str(cash) +" : "+str(futureDif[i]), (predTomorrowDif[i] + closePrices[i])/closePrices[i]
		#print str(cash) +" : "+str(actual[i]), pred[i]*100

	# elif ((predTomorrowDif[i] + closePrices[i])/closePrices[i])  < .995: #predicts down by 0.5% by tomorrow

	# 	if shares > 0:

	# 		# cash += closePrices[i]*shares
	# 		# if closePrices[i]*shares > tempBoughtCost:
	# 		# 	transactSuccesses+=1
	# 		# totalTransacts+=1
	# 		# shares = 0
	# 		# tempBoughtCost = 0


	# 	if futureDif[i] < 0:
	# 		shortSuccesses +=1
	# 	totalShorts +=1

	# if i==0:
	# 	print str(cash) +" : "+str(closePrices[i]*shares)

cash += closePrices[i]*shares #sell all
shares = 0
print cash
print "minCash", minCash
print "minNetWorth", minNetWorth
print "maxNetWorth", maxNetWorth
print "max/min worth:", maxNetWorth/minNetWorth * -1 
print "minCash/netWorth", minCash/netWorth * -1

print "	   gains | losses"
print "total |", gainTotal, cash-gainTotal
print "avg   |", gainTotal/transactSuccesses, (cash-gainTotal)/(totalTransacts-transactSuccesses)

print ""
print "Total longs: "+ str(totalLongs) +", %successful: "+ str(float(longSuccesses)/totalLongs*100.0)
#print "Total shorts: "+ str(totalShorts) + ", %successful: "+ str(float(shortSuccesses)/totalShorts)
print "Total transactions: "+ str(totalTransacts) + ", %successful: "+ str(float(transactSuccesses)/totalTransacts*100.0)
print "Total successful:", transactSuccesses
#print stockData.describe()
#print stockData['RSI']


#couldn't find function for intraday momentum index
#money flow index
