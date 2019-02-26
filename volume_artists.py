import numpy as np

path = "datasets/whole_data.csv"
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

top_volume = sorted(volume.items(), key=lambda x: x[1], reverse=True)[:10]
print (top_volume)
top_artists = [element[0] for element in top_volume]

print (top_artists)