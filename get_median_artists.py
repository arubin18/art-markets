import numpy as np

def get_median_artists(city):

	path = "datasets/" +  "-".join(city.split()).lower() + "/data.csv"
	data = np.array(open(path).readlines())

	labels = data[0].split(",")

	price_index = labels.index("price")
	artist_index = labels.index("artist")
	sold_index = labels.index("sold")

	prices = {}

	for line in data[1:]:
		artist = line.split(",")[artist_index]
		price = int(line.split(",")[price_index])
		sold = line.split(",")[sold_index]

		if artist not in prices:
			prices[artist] = []

		if sold == "1":
			prices[artist].append(price)

	medians = {} # median price of sold works by that artist 

	for artist in prices.keys():

		artist_prices = prices[artist]

		if len(artist_prices) > 0:
			medians[artist] = np.median(artist_prices)

	return medians

