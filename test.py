import numpy as np

city = "New York"
path = "datasets/" +  "-".join(city.split()).lower() + "/data.csv"
data = np.array(open(path).readlines())

auction_date_index = data[0].split(",").index("auction_date")

years = set()

for i in range(1,len(data)):
	sale = data[i].split(",")
	date_info = sale[auction_date_index]
	year = date_info.split("/")[-1]
	years.add(year)

print (years)