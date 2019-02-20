from get_median_artists import *
from get_volume_artists import *
from get_lots_sold_artists import *
import csv

def add_features(city):

	medians = get_median_artists(city)
	volumes = get_volume_artists(city)
	rates_sold = get_lots_sold_artists(city)

	path = "datasets/" +  "-".join(city.split()).lower() + "/data.csv"
	data = np.array(open(path).readlines())
	labels = data[0].split(",")
	labels[-1] = labels[-1].strip("\n").strip("\r")
	new_labels = ["artist_median_price", "artist_volume", "artist_lots_sold"]
	labels += new_labels

	artist_index = labels.index("artist")
	artist_median_price_index = labels.index("artist_median_price")
	artist_volume_index = labels.index("artist_volume")
	artist_lots_sold_index = labels.index("artist_lots_sold")

	new_data = [labels]

	length = len(data)

	for i in range(1,length):

		sale = data[i].split(",")
		sale[-1] = sale[-1].strip("\n").strip("\r")
		artist = sale[artist_index]

		if artist not in medians:
			median = 0
		else:
			median = medians[artist]
		
		volume = volumes[artist]
		r_sold = rates_sold[artist]

		sale += [median, volume, r_sold]

		new_data.append(sale)

	with open(path, "wb") as my_file:
		wr = csv.writer(my_file)
		wr.writerows(new_data)



