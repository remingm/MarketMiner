import csv
import urllib2

#f = open('sp500.csv','rb')
f = open('stockList.txt','rb')
reader = csv.reader(f)


#i = 0
for row in reader:
	
	symbol = row[0]
	#fileName = symbol +"dataEOD.csv"
	fileName = symbol +"fiveMinuteFiftyDay.csv"
	#i +=1 
	#if i > 481:
	#url = "https://www.quandl.com/api/v1/datasets/WIKI/"+symbol+".csv?column=4&sort_order=asc&trim_start=2011-02-12&trim_end=2016-2-12"
	url = 'http://www.google.com/finance/getprices?i=300&p=50d&f=d,o,h,l,c,v&df=cpct&q=' + symbol
	data = urllib2.urlopen(url)
	
	f = open(fileName,'w')
	f.write(data.read())
	f.close()


