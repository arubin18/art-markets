import numpy as np

def get_lots_sold_artists(city):

	path = "datasets/" +  "-".join(city.split()).lower() + "/data.csv"
	data = np.array(open(path).readlines())

	labels = data[0].split(",")

	artist_index = labels.index("artist")
	sold_index = labels.index("sold")

	works_sold = {}

	for line in data[1:]:
		artist = line.split(",")[artist_index]
		sold = int(line.split(",")[sold_index])

		if artist not in works_sold:
			works_sold[artist] = []
		works_sold[artist].append(sold)

	rates_sold = {}

	for artist in works_sold.keys():

		lots = works_sold[artist]
		num_sold = sum(lots)
		total = len(lots)
		r_sold = float(num_sold) / total
		rates_sold[artist] = r_sold

	return rates_sold



