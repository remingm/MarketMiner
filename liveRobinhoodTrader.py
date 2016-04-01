#!/bin/python
from Robinhood import Robinhood
import getpass
import time
import csv
import sys

class Stock:
	symbol = None
	priceHistory = []
	shareHistory = []
	shares = 0
	tempBoughtCost = 0

	def __init__ (self, symbol):
		self.symbol = symbol
		self.priceHistory = []
		self.shareHistory = []
		self.shares = 0
		self.tempBoughtCost = 0
	def __str__ (self):
		return str(self.symbol) +", Shares: "+str(self.shares)+", tempBoughtCost: "+str(self.tempBoughtCost)+", Price: " +str(self.priceHistory[len(self.priceHistory)-1])

f = open('sp500constituents.csv','rb')
#f = open('stockList.txt','rb')
reader = csv.reader(f)
#reader.next() #if needed

possibleStockList = []
print "Preparing Stocks..."
for row in reader:
	print "Adding to watchList: "+ row[0]
	possibleStockList.append(Stock(row[0]))

transactSuccesses = 0
totalTransacts = 0

cash = 0
minCash = cash

netWorth = 0 
minNetWorth = 0
maxNetWorth = 0

cashHistory = []
netHistory = []
shareHistory = []


#Setup
my_trader = Robinhood();
#login

print "\n\nWelcome to MarketMiner\n"
print time.asctime() ,"\n"
#username = raw_input("Robinhood Username: ")
#password = getpass.getpass(prompt='Password: ')

#my_trader.login(username="YOUR_USERNAME", password="YOUR_PASSWORD")

sys.stdout.flush()



 
start_time = time.time()

watchList = []
for stock in possibleStockList:
	try: 
		# print stock.symbol
		stock.priceHistory.append(float(my_trader.get_quote(stock=stock.symbol)))
		#print stock

		if stock.priceHistory[0] < 200:
			print "Including:", stock 
			watchList.append(stock) #adding to new list instead of only having one list to avoid altering list while iterating
		else:
			print "Not including:", stock 
	except Exception as e:
		print e,
		print "--- not including stock: "+stock.symbol
print "Not including", len(possibleStockList)-len(watchList), "stocks."
elapsed_time = time.time() - start_time
print "Time to pull price data for "+str(len(possibleStockList))+" stocks: " +str(elapsed_time) +"\n\n"
sys.stdout.flush()


# because i == 2
print "Second price grab..."
for stock in watchList:
	try: 
		# print stock.symbol
		stock.priceHistory.append(float(my_trader.get_quote(stock=stock.symbol)))
	except Exception as e:
		print e




stopLoss = 5 # sell all shares of stock if current value of shares has decreased by $5 from when bought

print "Beginning live trading with "+str(len(watchList))+" stocks..."
print "Start time: ", time.asctime(), "\n"
i=2
while True:
	start_time = time.time()

	roundCash = 0

	print "Round: #" +str(i)+ ", ", time.asctime()
	print "Analyzing price data for "+str(len(watchList))+" stocks..."
	sys.stdout.flush()
	for stock in watchList:
		try:
			stock.priceHistory.append(float(my_trader.get_quote(stock=stock.symbol)))
			# print stock
			# print i
			# print stock.priceHistory[i]
			# print stock.priceHistory[i-1]

			if roundCash > -400 and cash > -400 and float(stock.priceHistory[i])/float(stock.priceHistory[i-1]) < .995 and float(stock.priceHistory[i])/float(stock.priceHistory[i-2]) < .998:

				cash -= stock.priceHistory[i]
				roundCash -= stock.priceHistory[i]

				stock.shares += 1


				stock.tempBoughtCost += stock.priceHistory[i]

				if minCash > cash:
					minCash = cash
				print "1 Share bought: ", stock

			#elif shares > 0 and pred[i] < -0.007:
			elif stock.shares > 0 and (stock.tempBoughtCost - (stock.priceHistory[i] * stock.shares) > stopLoss or float(stock.priceHistory[i])/float(stock.priceHistory[i-1]) > 1.001):
			#elif stock.shares > 0 and (stock.tempBoughtCost - (stock.priceHistory[i] * stock.shares) > stopLoss or stock.rsi[i] > 65):
				if stock.tempBoughtCost < stock.priceHistory[i] * stock.shares:
					transactSuccesses += 1
					print "Profitable", stock.priceHistory[i]*stock.shares - stock.tempBoughtCost
				# else:
					print "Not profitable", stock.priceHistory[i]*stock.shares -stock.tempBoughtCost
				totalTransacts += 1

				print stock.shares, #... shares sold: ..

				cash += stock.priceHistory[i] * stock.shares
				roundCash += stock.priceHistory[i] * stock.shares
				stock.shares = 0
				stock.tempBoughtCost = 0 

				print "shares sold: ", stock

		except Exception as e:
			print e
		sys.stdout.flush()

	stockWorth = 0
	sharesTotal = 0
	for stock in watchList:
		if stock.shares > 0:
			stockWorth += stock.priceHistory[i] * stock.shares
			sharesTotal += stock.shares

	netWorth = cash + stockWorth
	if netWorth < minNetWorth:
		minNetWorth = netWorth
	elif netWorth > maxNetWorth:
		maxNetWorth = netWorth

	shareHistory.append(sharesTotal)
	cashHistory.append(cash)
	netHistory.append(netWorth)

	elapsed_time = time.time() - start_time

	print str(i), "netWorth:", netWorth
	print "Time to pull price data for "+str(len(watchList))+" stocks: " +str(elapsed_time)
	print time.asctime()
	if 300-elapsed_time > 0:
		print "Sleeping for", 300-elapsed_time,"seconds..."
		sys.stdout.flush()
		time.sleep(300-elapsed_time)
	print "\n\n"

	

	i+=1

	sys.stdout.flush()


# my_trader.get_quote("AAPL")
# #Get stock information
#     #Note: Sometimes more than one instrument may be returned for a given stock symbol
# stock_instrument = my_trader.instruments("GEVO")[0]

# print stock_instrument
# #Get a stock's quote
# my_trader.print_quote("AAPL")

# #Prompt for a symbol
# my_trader.print_quote();

# #Print multiple symbols
# my_trader.print_quotes(stocks=["BBRY", "FB", "MSFT"])

# #View all data for a given stock ie. Ask price and size, bid price and size, previous close, adjusted previous close, etc.
# quote_info = my_trader.quote_data("GEVO")
# print(quote_info);

# #Place a buy order (uses market bid price)
# buy_order = my_trader.place_buy_order(stock_instrument, 1)

# #Place a sell order
# sell_order = my_trader.place_sell_order(stock_instrument, 1)
