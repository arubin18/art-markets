import numpy as np
from clean_data import clean_data
import csv

def parse_data(city, labels):

	path = "datasets/" +  "-".join(city.split()).lower() + "/" +  "_".join(city.split()).lower() + ".csv"

	contents = np.array(open(path).readlines())

	exhibitions = set()
	auction_houses = set()

	start = 0

	new_contents = []

	def get_sales_for_exhibition(exhibition, contents):
		return [content for content in contents if content[2] == exhibition]

	for line in contents:
		sale = line.strip("\n").split(",")
		city = sale[0]

		first_quote = 1

		# print (sale)

		if "\"" == sale[1][0]:
			first_quote = 1
			second_quote = [i for i in range(first_quote+1,len(sale)) if "\"" in sale[i]][0]
			third_quote = second_quote+1
			auction_house = "".join(sale[first_quote:second_quote+1]).strip("\"")
			# print (auction_house)
		
		else: # no quotes
			auction_house = sale[1]
			third_quote = 2

		if "\"" == sale[third_quote][0]:
			fourth_quote = [i for i in range(third_quote+1,len(sale)) if "\"" in sale[i]][0]
			exhibition = "".join(sale[third_quote:fourth_quote+1]).strip("\"")
			img_index = fourth_quote+1

		else:
			exhibition = sale[third_quote]
			img_index = third_quote+1


		exhibitions.add(exhibition)
		auction_houses.add(auction_house)

		new_contents.append([city, auction_house, exhibition, sale[img_index], sale[img_index+1:]])

	size = len(labels)

	city_data = [labels]

	while len(exhibitions) != 0:

		exhibition = exhibitions.pop()

		sales = get_sales_for_exhibition(exhibition, new_contents)

		vals = [sale for sale in sales]

		exhibition_data = clean_data(sales, labels)

		city_data += exhibition_data

	with open("datasets/" +  "-".join(city.split()).lower() + "/" + "data.csv", "wb") as my_file:
		wr = csv.writer(my_file)
		wr.writerows(city_data)
