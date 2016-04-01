from Robinhood import Robinhood
import getpass

my_trader = Robinhood()

my_username = raw_input("Robinhood Username: ")
my_password = getpass.getpass(prompt='Password: ')

my_trader.login(username=my_username, password=my_password)

buySell = raw_input("Would you like to buy or sell? (Enter 'buy' or 'sell'): ")
symbol = raw_input("Symbol: ")


stock_instrument = my_trader.instruments(symbol)[0]

print my_trader.get_quote(symbol)

print stock_instrument

print buySell
if buySell == "buy":
	#Place a buy order (uses market bid price)
	buy_order = my_trader.place_buy_order(stock_instrument, 1)
elif buySell == "sell":
	# #Place a sell order
	sell_order = my_trader.place_sell_order(stock_instrument, 1)
else: 
	print "Didn't enter 'buy' or 'sell', exiting."