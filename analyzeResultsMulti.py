import csv
import talib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time 

longSuccesses = 0
totalLongs = 0

shortSuccesses = 0
totalShorts = 0

transactSuccesses = 0
totalTransacts = 0

cash = 0
lossTotal = 0
gainTotal = 0
minCash = cash

netWorth = 0 
minNetWorth = 0
maxNetWorth = 0
totalShares = 0

cashHistory = []
netHistory = []
shareHistory = []
totalShareSum = []
maxLen = 0

class Stock:
	symbol = None
	closeHistory = []
	shareHistory = []
	shares = 0
	rsi = []
	tempBoughtCost = 0

	def __init__ (self, symbol, closeHistory, rsi):
		self.symbol = symbol
		self.closeHistory = closeHistory
		self.shareHistory = []
		self.shares = 0
		self.rsi = rsi
		self.tempBoughtCost = 0

watchList = []
closeHist = []

possibleStocks = 0
print "Preparing Stocks..."
for filename in os.listdir(os.getcwd()):
	if "newCols" in filename:
		possibleStocks +=1
		stockData = pd.read_csv(filename)
		

		# predicting = 'futureDif%'
		# pred = stockData['PRED:'+predicting]
		# actual = stockData[predicting]
		rsi = stockData['RSI']

		#predTomorrowDif = stockData['PRED:TomorrowDif']
		#predTomorrowDifP = stockData['PRED:TomorrowDif%']
		closeHist = stockData['Close']
		#dates = closeHistory['Date']
		if len(closeHist) > 500 and closeHist[0] < 200 and closeHist[0] > 0:
			#print "Including:", filename
			watchList.append(Stock(filename, closeHist, rsi))
		else:
			pass
			#print "Not Including", filename

		if len(closeHist) > maxLen:
			maxLen = len(closeHist)
print "Not including", possibleStocks-len(watchList), "/",len(watchList), "stocks."


roundCash = 0
stopLoss = 5
lookBackPeriod = 1

print "Beginning Trading..."
i = lookBackPeriod

while i < maxLen:
	roundCash = 0
	for stock in watchList:
		#if ((predTomorrowDif[i] + closeHistory[i])/closeHistory[i])  > 1.001: #predicts up by 0.5% by tomorrow
		if i < len(stock.closeHistory):

			#if pred[i] > 0.03:
			if roundCash > -100 and cash > -100 and float(stock.closeHistory[i])/float(stock.closeHistory[i-lookBackPeriod]) < .985 and float(stock.closeHistory[i])/float(stock.closeHistory[i-lookBackPeriod]) > 0.94:
			#if cash > -100 and stock.rsi[i] < 10:
				cash -= stock.closeHistory[i]
				roundCash -= stock.closeHistory[i]

				stock.shares += 1
				totalShares += 1
				stock.tempBoughtCost += stock.closeHistory[i]

				if minCash > cash:
					minCash = cash

			#elif shares > 0 and pred[i] < -0.007:
			elif stock.shares > 0 and (stock.tempBoughtCost - (stock.closeHistory[i] * stock.shares) > stopLoss or float(stock.closeHistory[i])/float(stock.closeHistory[i-lookBackPeriod]) > 1.001):
			#elif stock.shares > 0 and (stock.tempBoughtCost - (stock.closeHistory[i] * stock.shares) > stopLoss or stock.rsi[i] > 70):
				if stock.tempBoughtCost < stock.closeHistory[i] * stock.shares:
					transactSuccesses += 1
					# print "profitable", stock.closeHistory[i]*stock.shares - stock.tempBoughtCost, i
					gainTotal += stock.closeHistory[i]*stock.shares - stock.tempBoughtCost
				# else:
					# print "not profitable", stock.closeHistory[i]*stock.shares -stock.tempBoughtCost, i
				totalTransacts += 1

				cash += stock.closeHistory[i] * stock.shares
				roundCash += stock.closeHistory[i] * stock.shares
				stock.shares = 0
				stock.tempBoughtCost = 0

		elif stock.shares > 0:
			cash += stock.closeHistory[len(stock.closeHistory)-1]*stock.shares #sell all
			stock.shares = 0

	stockWorth = 0
	numShares = 0
	for stock in watchList:
		if stock.shares > 0:
			stockWorth += stock.closeHistory[i] * stock.shares
			numShares += stock.shares

	netWorth = cash + stockWorth
	if netWorth < minNetWorth:
		minNetWorth = netWorth
	elif netWorth > maxNetWorth:
		maxNetWorth = netWorth


	shareHistory.append(numShares)
	cashHistory.append(cash)
	netHistory.append(netWorth)
	totalShareSum.append(totalShares)

	#print i, len(netHistory)
	# if i > 160 and i < 220:
	# 	print i, float(netHistory[i-1])/float(netHistory[i-2])
	# 	time.sleep(0.3)
	# if i > 10 and float(netHistory[i-1])/float(netHistory[i-2]) < .97:
	# 	print "skipping 10", i, float(netHistory[i-1])/float(netHistory[i-2])
	# 	#time.sleep (2)
	# 	temp = i + 10
	# 	while i< temp:
	# 		cashHistory.append(cash)
	# 		netHistory.append(netWorth)
	# 		i+=1
	i += lookBackPeriod

	if i%35 == 0:
		print str(i)+"/"+str(maxLen)+":", netWorth
			#closeHistory.append(closeHistory[i])
			#shareHistory.append(shares)

			#print str(cash) +" : "+str(futureDif[i]), (predTomorrowDif[i] + closeHistory[i])/closeHistory[i]
			#print str(cash) +" : "+str(actual[i]), pred[i]*100

	# elif ((predTomorrowDif[i] + closeHistory[i])/closeHistory[i])  < .995: #predicts down by 0.5% by tomorrow

	# 	if shares > 0:

	# 		# cash += closeHistory[i]*shares
	# 		# if closeHistory[i]*shares > tempBoughtCost:
	# 		# 	transactSuccesses+=1
	# 		# totalTransacts+=1
	# 		# shares = 0
	# 		# tempBoughtCost = 0


	# 	if futureDif[i] < 0:
	# 		shortSuccesses +=1
	# 	totalShorts +=1

	# if i==0:
	# 	print str(cash) +" : "+str(closeHistory[i]*shares)


# for stock in watchList:
# 	#if ((predTomorrowDif[i] + closeHistory[i])/closeHistory[i])  > 1.001: #predicts up by 0.5% by tomorrow
# 	i = len(stock.closeHistory)-1
# 	#if pred[i] > 0.03:
# 	if stock.shares > 0:
# 	#elif stock.shares > 0 and (stock.tempBoughtCost - (stock.closeHistory[i] * stock.shares) > stopLoss or stock.rsi[i] > 80):
# 		if stock.tempBoughtCost < stock.closeHistory[i] * stock.shares:
# 			transactSuccesses += 1
# 			# print "profitable", stock.closeHistory[i]*stock.shares - stock.tempBoughtCost, i
# 			gainTotal += stock.closeHistory[i]*stock.shares - stock.tempBoughtCost
# 		# else:
# 			# print "not profitable", stock.closeHistory[i]*stock.shares -stock.tempBoughtCost, i
# 		totalTransacts += 1

# 		cash += stock.closeHistory[i] * stock.shares
# 		roundCash += stock.closeHistory[i] * stock.shares
# 		stock.shares = 0
# 		stock.tempBoughtCost = 0

# 	for stock in watchList:
# 	if stock.shares > 0:
# 		stockWorth += stock.closeHistory[i] * stock.shares
# 		numShares += stock.shares

# 	netWorth = cash + stockWorth
# 	if netWorth < minNetWorth:
# 		minNetWorth = netWorth
# 	elif netWorth > maxNetWorth:
# 		maxNetWorth = netWorth


# 	shareHistory.append(numShares)
# 	cashHistory.append(cash)
# 	netHistory.append(netWorth)
# 	totalShareSum.append(totalShares)


print netWorth
print "minCash", minCash
print "minNetWorth", minNetWorth
print "maxNetWorth", maxNetWorth
print "max/min worth:", maxNetWorth/minNetWorth * -1 
print "minCash/netWorth", minCash/netWorth * -1

print "	   gains | losses"
print "total |", gainTotal, cash-gainTotal
print "avg   |", gainTotal/transactSuccesses, (cash-gainTotal)/(totalTransacts-transactSuccesses)

print ""
#print "Total shorts: "+ str(totalShorts) + ", %successful: "+ str(float(shortSuccesses)/totalShorts)
print "Total transactions: "+ str(totalTransacts) + ", %successful: "+ str(float(transactSuccesses)/totalTransacts*100.0)
print "Total successful:", transactSuccesses
#print stockData.describe()
#print stockData['RSI']

#couldn't find function for intraday momentum index
#money flow index


fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot(xrange(0,len(netHistory)), shareHistory, c='r', label='shareHistory')
ax2.set_title('shareHistory')
fig2.savefig('shareHistory.png')

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot(xrange(0,len(cashHistory)), cashHistory, c='r', label='cashHistory')
ax2.set_title('cashHistory')
fig2.savefig('cashHistory.png')

fig3 = plt.figure()
ax2 = fig3.add_subplot(111)
ax2.plot(xrange(0,len(totalShareSum)), totalShareSum, c='r', label='totalShareSum')
ax2.set_title('totalShareSum')
fig3.savefig('totalShareSum.png')

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(xrange(0,len(netHistory)), netHistory, c='b', label='netHistory')
#ax1.plot(xrange(0,len(netHistory)), cashHistory, c='r', label='cashHistory')
#ax1.plot(xrange(0,len(netHistory)), closeHistory, c='g', label='closeHistory')

# x_net = xrange(0,len(netHistory))
# y_net = netHistory
# p = ax.plot(x_net, y_net, 'b')
ax1.set_xlabel('Periods since 0')
ax1.set_ylabel('USD')
ax1.set_title('Price vs net')
fig.savefig('netHistory.png')


