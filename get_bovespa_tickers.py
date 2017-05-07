import string
import bs4 as bs
import requests
import pickle

def get_bovespa_tickers():
	print ("Saving All BOVESPA tickers...")

	for letter in range(24):
		#	Goes from 0 to 24 because there are no brazilian stocks beginning
		#	with Y or Z (weird, right? Took me 10 minutes to find out what was
		#	wrong)
		resp = requests.get('https://br.advfn.com/bolsa-de-valores/bovespa/'+string.ascii_uppercase[letter])
		soup = bs.BeautifulSoup(resp.text, "lxml")
		table = soup.find('table', {'class':'atoz-link-bov'})
		tickers = []
		for row in table.findAll('tr')[1:]:
			ticker = row.findAll('td')[1].text
			if ticker[-2] != '3' and ticker[-1] != '4':
				tickers.append(ticker+'.SA')
				print(ticker)

	with open("BOVESPA_All_tickers.pickle", "wb") as f:
		pickle.dump(tickers,f)
		print("File BOVESPA_All_tickers.pickle created")	# Just for Debug
	return tickers



bovespa_tickers = get_bovespa_tickers()
