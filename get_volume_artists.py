import numpy as np

def get_volume_artists(city):

	path = "datasets/" +  "-".join(city.split()).lower() + "/data.csv"
	data = np.array(open(path).readlines())

	labels = data[0].split(",")

	artist_index = labels.index("artist")
	sold_index = labels.index("sold")

	artists = set()

	volume = {} # volume sold by that artist 

	for line in data[1:]:
		artist = line.split(",")[artist_index]
		sold = line.split(",")[sold_index]

		if artist not in volume:
			volume[artist] = 0
		
		if sold == "1":
			volume[artist] += 1

	return volume

