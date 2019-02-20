import numpy as np

def get_cpi():

	path = "datasets/cpi_data.txt"

	data = np.array(open(path).readlines())

	months = data[1].split("\t")[1:13]

	cpi_by_year = {}

	for i in range(2,len(data)):

		line = data[i].split("\t")
		year = line[0]
		year_data = line[1:13]
		cpi_by_year[year] = year_data

	return cpi_by_year