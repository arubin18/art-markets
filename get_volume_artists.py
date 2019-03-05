import numpy as np
import csv

def get_volume_artists(city):

	path = "datasets/" +  "-".join(city.split()).lower() + "/data.csv"
	
	with open(path) as f:
		reader = csv.reader(f)
		data = [row for row in reader]
	labels = data[0]

	artist_index = labels.index("artist")
	sold_index = labels.index("sold")

	artists = set()

	volume = {} # volume sold by that artist 

	for line in data[1:]:
		artist = line[artist_index]
		sold = line[sold_index]

		if artist not in volume:
			volume[artist] = 0
		
		if sold == "1":
			volume[artist] += 1

	return volume

