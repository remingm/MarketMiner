#!/usr/bin/python

# Ian Hammerstrom
# 02/02/16
#if down 1.5% over 30 minutes, buy
#then, once owned, if goes up by 0.75% over 15 minutes, sell 

from yahoo_finance import Share
# if yahoo_finance isn't installed, enter as a command: "[sudo] pip install yahoo-finance"
import time
import datetime
import sys
import csv

print "Starting"


def printNetWorth():
	print "Current balance: $" +str(myBalance)
	stocksTotalValue = 0

	for symbol in watchList:
		if(symbol.numShares > 0):
			try: 
				symbolValue = float(symbol.stock.get_price()) * symbol.numShares
				print "Value of "+str(symbol)+": $"+str(symbolValue)
				stocksTotalValue += float(symbolValue)
			except Exception as e:
				print e

	print "Current stock portfolio value: $" + str(stocksTotalValue)
	netWorth = myBalance + stocksTotalValue
	print "Total worth: $"+str(netWorth)

	if netWorth > startBalance:
		print "You've gained: $"+ str(netWorth-startBalance)
	else: 
		print "You've lost: $"+ str(startBalance-netWorth)

def printDayBegin():
	print "############TIME#TO#SIT#BACK#AND#RETIRE###################"
	printNetWorth()

	print ""
	print "STARTING EPOCH TIME: "+str(datetime.timedelta(seconds=startTime))
	print "STARTING MARKET TIME: "+str(watchList[0].stock.get_trade_datetime())
	print ""

	for symbol in watchList:
		print "Opening price of "+str(symbol)+": $"+ str(symbol.openPrice)
	print "###########################################################"

class MyStock:
	stock = None
	symbol = None
	priceHistory = None
	numShares = None
	openPrice = None

	def __init__ (self, symbol):
		self.stock = Share(symbol)
		self.symbol = symbol
		self.priceHistory=[]
		self.numShares=0
		self.openPrice = self.stock.get_open()

	def __str__ (self):
		return str(self.symbol +"("+str(self.numShares)+")")

	def buyOne(self):
		price = self.stock.get_price()
		global myBalance
		print "Buying a share of "+str(self.symbol)+" for $"+str(price)
		myBalance -= float(price)
		self.numShares += 1
		print self.stock.get_trade_datetime()
		printNetWorth()

	def sellAll(self):
		price = self.stock.get_price()
		global myBalance
		if self.numShares > 0:
			while (self.numShares > 0):
				print "Selling a share of "+str(self.symbol)+" for $"+str(price)
				myBalance += float(price)
				self.numShares -= 1
				print self.stock.get_trade_datetime()
		else:
			print "Can't sell, no shares owned." #shouldn't get here
		printNetWorth()


startBalance = 10000
myBalance = startBalance


# watchList is the collection of stocks we are allowing to be traded
watchList=[]

MyStock

#try: 
print "Loading 494(why only 494?) of the S&P500"
f = open('sp500.csv','rb')
reader = csv.reader(f)

i=0
for row in reader:
	i+=1
	watchList.append(MyStock(row[0]))
	print str(i) +") "+ str(row) 
	
	sys.stdout.flush()
# watchList.append(MyStock("AAPL")) 
# watchList.append(MyStock("GOOG"))
# watchList.append(MyStock("IBM"))
# watchList.append(MyStock("AMZN"))
# watchList.append(MyStock("F"))
# watchList.append(MyStock("TSLA"))
# watchList.append(MyStock("MSFT"))
# watchList.append(MyStock("EBAY"))
# watchList.append(MyStock("NFLX"))
# watchList.append(MyStock("XOM"))
# watchList.append(MyStock("WMT"))
# watchList.append(MyStock("GE"))
# watchList.append(MyStock("JPM"))
# watchList.append(MyStock("CVX"))
# watchList.append(MyStock("VZ"))
# watchList.append(MyStock("FB"))
# watchList.append(MyStock("KO"))
# watchList.append(MyStock("T"))
# watchList.append(MyStock("ORCL"))
# watchList.append(MyStock("BAC"))
# watchList.append(MyStock("MMM"))
# watchList.append(MyStock("HPE"))
# watchList.append(MyStock("PYPL"))
# watchList.append(MyStock("GM"))
# watchList.append(MyStock("FFIV"))
# watchList.append(MyStock("V"))
# watchList.append(MyStock("ORLY"))
# watchList.append(MyStock("NDAQ"))
# watchList.append(MyStock("DPS"))
# watchList.append(MyStock("EXPD"))
# watchList.append(MyStock("CBS"))
# watchList.append(MyStock("LUV"))
# watchList.append(MyStock("CSCO"))
# watchList.append(MyStock("COST"))
# watchList.append(MyStock("NKE"))
# watchList.append(MyStock("HD"))
# watchList.append(MyStock("T"))
# watchList.append(MyStock("INTC"))
# watchList.append(MyStock("DIS"))
# watchList.append(MyStock("SNDK"))
# watchList.append(MyStock("WFM"))
startTime =time.time()
printDayBegin()

#except Exception as e: #This should only happen if error recieving data from Yahoo
# 	print e

sys.stdout.flush()

cycles = 0
priceRequests = 0
timeConst = 6 #change along with sleep time

while cycles < 98: # only run for 6.5 hours (best to start at 6:30AM here, 9:30AM Eastern Time. (98 if sleep is 240) (390 if 60) 
	i=0
	cycles+=1
	print ""
	print "cycle #"+str(cycles)+", Time elapsed since start: "+str(datetime.timedelta(seconds=time.time()-startTime))

	for symbol in watchList:
		try: 
			i+=1
			symbol.stock.refresh()#get new data
			currPrice = symbol.stock.get_price()
			symbol.priceHistory.append(currPrice)#append this data to price history

			

			if len(symbol.priceHistory) > timeConst: # 6 if sleep time is 240, 30 if sleep time is 60 
				print str(i) +") Price of "+ str(symbol)+ ": $"+ str(currPrice) + " currPrice/30 minutes ago = ("+str("%.2f" % (float(currPrice)/float(symbol.priceHistory[len(symbol.priceHistory)-timeConst])))+"%)"
				#if down 1.5% over 30 minutes, buy #changed 30 to 6 when using 4(5) minute sleep time
				if float(currPrice)/float(symbol.priceHistory[len(symbol.priceHistory)-timeConst]) < .985:
					print "Buying: Compared current price("+str(currPrice)+") to price 30 minutes ago("+str(symbol.priceHistory[len(symbol.priceHistory)-timeConst])+")"
					symbol.buyOne()
					print "Shares owned of "+str(symbol)+": " +str(symbol.numShares)

				if symbol.numShares > 0: 
					#once owned, if goes up by 0.75% over 15 minutes, sell #changed 15 to 3 (15/5)=3
					if float(currPrice)/float(symbol.priceHistory[len(symbol.priceHistory)-timeConst/2]) > 1.0075:
						print "Selling: Compared current price("+str(currPrice)+") to price 15 minutes ago("+str(symbol.priceHistory[len(symbol.priceHistory)-timeConst/2])+")"
						symbol.sellAll()
						print "Shares owned of "+str(symbol)+": " +str(symbol.numShares)
			else:
				print str(i) +") Price of "+ str(symbol)+ ": $"+ str(currPrice)
		except Exception as e: #This should only happen if error recieving data from Yahoo
			print e

	priceRequests += len(watchList)
	print "Total number of price requests: "+str(priceRequests)
	print "--------"
	sys.stdout.flush()
	#time.sleep(60)# have sleep as 60 seconds for the algorithm's minute count to work properly. 
	time.sleep(240)#using 4 minute sleep time + 1 minute assumed load prices time when portfolio size is large. 
	# change timeConst to 6 if sleep is 240, if sleep is 60 change timeConst to 30
	# (probably more than 1 minute load time realistically for 490+ stocks)
	# this probably also helps keep yahoo off our backs

printNetWorth()
sys.stdout.flush()
