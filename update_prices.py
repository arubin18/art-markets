from get_cpi import *
import csv

def update_cpi(price_past, cpi_current, cpi_past):
	return int(price_past * (cpi_current / cpi_past))

def update_prices(city):
	""" update prices by cpi """

	path = "datasets/" +  "-".join(city.split()).lower() + "/data.csv"

	with open(path) as f:
		reader = csv.reader(f)
		data = [row for row in reader]
	labels = data[0]

	price_index = labels.index("price")
	avg_estimate_index = labels.index("avg_estimate")
	avg_price_sold_before_index = labels.index("avg_price_sold_before")
	avg_price_sold_index = labels.index("avg_price_sold")
	auction_date_index = labels.index("auction_date")

	cpi_by_year = get_cpi()

	length = len(data)

	cpi_current = float(cpi_by_year['2018'][-1]) # december of 2018

	new_data = [labels]

	for i in range(1,length):

		# get past prices
		sale = data[i]
		try:
			price_past = float(sale[price_index])
		except:
			print (sale)
			continue
			
		avg_estimate_past = float(sale[avg_estimate_index])
		avg_price_sold_before_past = float(sale[avg_price_sold_before_index])
		avg_price_sold_past = float(sale[avg_price_sold_index])

		# get year and month
		auction_date = sale[auction_date_index][:]
		date_info = auction_date.split("/")
		month = date_info[0]
		year = date_info[-1]

		cpi_past = float(cpi_by_year[year][int(month)-1])

		# get current prices
		price_current = update_cpi(price_past, cpi_current, cpi_past)
		avg_estimate_current = update_cpi(avg_estimate_past, cpi_current, cpi_past)
		avg_price_sold_before_current = update_cpi(avg_price_sold_before_past, cpi_current, cpi_past)
		avg_price_sold_current = update_cpi(avg_price_sold_past, cpi_current, cpi_past)

		# update list with current prices
		sale[price_index] = int(price_current)
		sale[avg_estimate_index] = int(avg_estimate_current)
		sale[avg_price_sold_before_index] = int(avg_price_sold_before_current)
		sale[avg_price_sold_index] = int(avg_price_sold_current)

		sale[-1] = sale[-1].strip("\n").strip("\r")
		new_data.append(sale)

	new_data[0][-1] = new_data[0][-1].strip("\n").strip("\r")

	with open(path, "wb") as my_file:
		wr = csv.writer(my_file)
		wr.writerows(new_data)







