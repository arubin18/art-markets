import numpy as np
from clean_data import clean_data
import csv

def parse_data(city, labels):

	path = "datasets/" +  "-".join(city.split()).lower() + "/" +  "_".join(city.split()).lower() + ".csv"

	with open(path) as f:
		reader = csv.reader(f)
		contents = [row for row in reader]

	exhibitions = set()
	auction_houses = set()

	def get_sales_for_exhibition(exhibition, contents):
		return [row for row in contents if row[2] == exhibition]

	for row in contents:
		auction_houses.add(row[1])
		exhibitions.add(row[2])

	size = len(labels)

	city_data = [labels]

	while len(exhibitions) != 0:

		exhibition = exhibitions.pop()

		sales = get_sales_for_exhibition(exhibition, contents)

		exhibition_data = clean_data(sales, labels)

		# print (len(sales) - len(exhibition_data))

		city_data += exhibition_data

	with open("datasets/" +  "-".join(city.split()).lower() + "/" + "data.csv", "wb") as my_file:
		wr = csv.writer(my_file)
		wr.writerows(city_data)
