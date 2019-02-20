import numpy as np

path = "datasets/new-york/data.csv"

data = np.array(open(path).readlines())

size = len(data)

labels = data[0].split(",")

artist_index = labels.index("artist")

artists = set()

volume = {}

for line in data[1:]:
	artist = line.split(",")[artist_index]

	if artist not in volume:
		volume[artist] = 0
	volume[artist] += 1

print (volume)

