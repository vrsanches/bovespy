import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

#	Using the examples taught by sentdex from his youtube channel


def save_sp500_tickers():
	print ("Saving the S&P500 tickers...")	#	Just for debug
	resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = bs.BeautifulSoup(resp.text, "lxml")
	table = soup.find('table', {'class':'wikitable sortable'})
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text
#	Treating these two companies for this character exception
#	From the wiki they are shown as a '.' and you need to use the
#	'-' to pull data from Yahoo Finance
		if ticker == 'BRK.B':
			ticker = 'BRK-B'
		if ticker == 'BF.B':
			ticker = 'BF-B'
		tickers.append(ticker)

	with open("sp500tickers.pickle", "wb") as f:
		pickle.dump(tickers, f)
		print("File sp500tickers.pickle created")	# Just for Debug

	return tickers


#save_sp500_tickers() - nao vamos mais usar

def get_data_from_yahoo(reload_sp500=True):

	if reload_sp500:
		tickers = save_sp500_tickers()
	else:
		with open("sp500tickers.pickle","rb") as f:
			tickers = pickle.load(f)

	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')

	start = dt.datetime(2000,1,1)	#	These dates can change
	end = dt.datetime(2016,12,31)

	for ticker in tickers: #	[:10]: Este indice do ticker
	#	Deve ser modificado se quero pegar a lista inteira
	#	No caso, estou usando os 10 primeiros para poder
	#	testar

	#	That ticker index can be changed so you dont need to wait for all 
	#	the #500 companies to be pulled (it should take some 10-20 minutes
	#	depending on your computer)
		print(ticker+'...ready')	#	Just for debug
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			df = web.DataReader(ticker,'yahoo',start,end)
			df.to_csv('stock_dfs/{}.csv'.format(ticker))
		else:
			print('Already have {} file'.format(ticker)) #	Sentdex debug

#get_data_from_yahoo()

def compile_data():

	with open("sp500tickers.pickle","rb") as f:
		tickers = pickle.load(f)
		print('loaded tickers to compile')	#	Just for debug
	#tickers = save_sp500_tickers()
	main_df = pd.DataFrame()

	for count,ticker in enumerate(tickers): #	[:10]: - see comment above
		print('reading '+ticker)	#just for debug
		df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
		df.set_index('Date', inplace=True)
 
		df.rename(columns = {'Adj Close' : ticker}, inplace=True)
		df.drop(['Open','High','Low','Close','Volume'], 1, inplace=True)

		if main_df.empty:
			main_df = df
		else:
			main_df = main_df.join(df, how='outer')

		if count % 10 == 0:
			print(count)	#	just for debug, counting each 10 companies
							#	processed
		print(ticker+' compiled. Next...')	#	just for debug

	print (main_df.head())
	print('Saving sp500_joined_closes.csv file...')	# 	just for debug
	main_df.to_csv('sp500_joined_closes.csv')

#get_data_from_yahoo()
#compile_data()

def visualize_data():
	df = pd.read_csv('sp500_joined_closes.csv')
#	df['MMM'].plot()
#	print('Plotting...')
#	plt.show()
	df_corr = df.corr()			#	creating correlation table
#	print(df_corr.head())		#	this line is not necessary

	data = df_corr.values		#	get only the values, ignore header
								#	and index
	fig = plt.figure()			#	creating the graphic
	ax = fig.add_subplot(1,1,1)

	heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)	#	setting up the heatmap

	fig.colorbar(heatmap)	#	put heat color scale (legenda) to the side
	ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
	ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
	ax.invert_yaxis()	#	inverting the yaxis so it doesnt have any 
						#	empty space on top
	ax.xaxis.tick_top()	#	Move the X ticks to the top

	column_labels = df_corr.columns #	get the names from the tickers
	row_labels = df_corr.index 		#	get the names from the tickers

	ax.set_xticklabels(column_labels) #	Set the names for the axis
	ax.set_yticklabels(row_labels)	  #	set the names for the axis as well
	plt.xticks(rotation=90)			 #	rotate the graphic to be shown down 
									# and to the right
	heatmap.set_clim(-1,1)	#	Define the range
	plt.tight_layout()	#	show the data tightly
	plt.show()




#	If this is the first time running, please run first these two:

#get_data_from_yahoo()
#compile_data()

#	To create all related files and spreadsheets


visualize_data()

#	This code has until the 8th video of sentdex playlist 'Python for 
#	finance' videos from youtube


















