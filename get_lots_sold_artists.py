import numpy as np
import csv

def get_lots_sold_artists(city):

	path = "datasets/" +  "-".join(city.split()).lower() + "/data.csv"

	with open(path) as f:
		reader = csv.reader(f)
		data = [row for row in reader]
	labels = data[0]

	artist_index = labels.index("artist")
	sold_index = labels.index("sold")

	works_sold = {}

	for line in data[1:]:
		artist = line[artist_index]
		sold = int(line[sold_index])

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



