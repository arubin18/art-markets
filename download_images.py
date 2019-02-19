import numpy as np
import urllib

path = "datasets/new-york/data.csv"

data = np.array(open(path).readlines())

size = len(data)

labels = data[0].split(",")

img_index = labels.index("img_url")

for i in range(18860,size):

	row = data[i].split(",")
	idd = row[0]
	url = row[img_index]

	dest = "images/new-york/" + idd + ".jpg"

	try:

		urllib.urlretrieve(url, dest)

	except:
		pass
