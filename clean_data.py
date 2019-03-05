import numpy as np
import scipy.stats
import uuid

def product (my_list):
	return reduce(lambda x, y: x*y, my_list)

def clean_data(data, labels):

	auctions_sold = 0 # counter for number of auctions sold before the current lot
	auctions_total = 0 # total price of auctions sold before the current lot
	auctions_average = 0 # average price of auctions sold before the current lot
	auctions_median = 0
	artwork_count = 1 # lots explored in the auction so far
	largest_lot = 1
	artist_counter = {}
	vol = 0 # volatility 
	total_vol = 0
	skew = 0
	total_skew = 0
	num_artworks = 0
	num_artists = 0
	sale_rate = 0
	avg_price_sold = 0
	median_price_sold = 0
	lots_per_artist = 0
	num_artworks_ratio = 0
	
	### iterate through each artwork
	exhibition_data = []

	prices = [] # prices for artworks in exhbitiion

	for row in data:

		city, auction_house, exhibition, img_url = row[:4]

		info = row[4:]

		try:
			artist, title, price, low_estimate, high_estimate, signed, area, \
			year_created, auction_lot, auction_date, medium = info

		except:
			continue 

		auction_lot = auction_lot.split()[0] # get rid of words following the lot number

		if price == "SOLD":
			continue

		# not sold yet
		if "soon" in price:
			continue # skip this artwork 

		if "withdrawn" in price:
			continue

		if artist not in artist_counter:
			artist_counter[artist] = 0
		artist_counter[artist] += 1

		# remove dollar signs
		if "$" in price:
			price = price[1:]

		if "$" in high_estimate:
			high_estimate = high_estimate[1:]

		if "$" in low_estimate:
			low_estimate = low_estimate[1:]
		
		# remove euro conversions
		if "(" in price:
			price = price.split("(")[0][1:-1]

		if "(" in low_estimate:
			low_estimate = low_estimate.split("(")[0][1:-1]

		if "(" in high_estimate:
			high_estimate = high_estimate.split("(")[0][1:-1]

		# remove commas in numbers
		if "," in price:
			price = "".join(price.split(","))

		if "," in low_estimate:
			low_estimate = "".join(low_estimate.split(","))

		if "," in high_estimate:
			high_estimate = "".join(high_estimate.split(","))

		if len(price) == 0: # no price available 
			continue

		# check if the artwork sold
		if "not" in price.lower():
			sold = 0
			price = "0"

		else:
			sold = 1

		if len(low_estimate) == 0 or len(high_estimate) == 0:
			continue

		if not low_estimate[0].isdigit() and not high_estimate[0].isdigit():
			avg_estimate = 0.0

		elif not low_estimate[0].isdigit():
			avg_estimate = float(high_estimate)

		elif not high_estimate[0].isdigit():
			avg_estimate = float(low_estimate)

		else:
			avg_estimate = float(int(low_estimate) + int(high_estimate)) / 2

		if "not" in area:
			area = "NA"
			volume = 0

		else:
			dimensions = area.split("x")
			try:
				dimensions = [float(d.strip(" ").strip("\"")) for d in dimensions]
			except:
				continue
			
			if len(dimensions) > 2: # more than two dimensions
				area = str(product(dimensions[:-1]))
				volume =  str(product(dimensions))
			
			else: 
				area = str(product(dimensions))
				volume = 0

		# letter at the end of auction lot
		if auction_lot[-1].isalpha():
			auction_lot = auction_lot[:-1]

		try:
			auction_lot = float(auction_lot.lower().strip("bi").strip("te").strip("qu"))
			if auction_lot > largest_lot:
				auction_lot = int(auction_lot)
				largest_lot = auction_lot

		except:
			continue

		# get rid of more than one date
		if "-" in auction_date:
			auction_date = auction_date.split("-")[0]
		
		idd = uuid.uuid4().hex

		# clean up year created variable 

		if "-" in year_created:
			year_created = year_created.split("-")[0]

		if "/" in year_created:
			year_created = year_created.split("/")[0]

		if "c" in year_created:
			year_created = year_created[3:]

		if len(year_created) == 3:
			if year_created[0].isdigit():
				if int(year_created[0]) > 0:
					year_created = "1" + year_created
				else:
					year_created = "2" + year_created

		if len(year_created) == 2:
			if year_created[0].isdigit():
				if int(year_created) < 19:
					year_created = "20" + year_created
				else:
					year_created = "19" + year_created

		if "s" in year_created:
			year_created = year_created[:-1]

		if "not" in year_created:
			year_created = "NA"

		# convert range of signed into binary
		if "signed" in signed.lower():
			signed = 1
		else:
			signed = 0

		sold_before = float(auctions_sold) / int(artwork_count)

		artwork_data = [idd, city, exhibition, artist, title, price, sold, avg_estimate, signed, area, \
			volume, year_created, auction_lot, auction_house, auction_date, sold_before, \
			auctions_average, auctions_median, num_artworks, avg_price_sold, median_price_sold, num_artists, sale_rate, img_url, \
			vol, total_vol, skew, total_skew, medium, lots_per_artist, num_artworks_ratio]

		exhibition_data.append(artwork_data)

		# update sold counter
		if sold == 1:
			auctions_sold += 1
			try:
				auctions_total += int(price)

			except:
				continue

			prices.append(int(price))

			non_zero_prices = filter(lambda p: p != 0, prices)

			# empty 
			if len(non_zero_prices) == 0:
				vol = 0
				skew = 0
				auctions_median = 0
			
			else:
				vol = np.std(non_zero_prices) # volatility 
				skew = scipy.stats.skew(non_zero_prices)
				auctions_median = np.median(non_zero_prices)
			
			auctions_average = float(auctions_total) / auctions_sold

		artwork_count += 1 # update total counter

	lot_index = labels.index("auction_lot")
	num_artworks_index = labels.index("num_artworks")
	artist_index = labels.index("artist")
	avg_price_sold_index = labels.index("avg_price_sold")
	median_price_sold_index = labels.index("median_price_sold")
	num_artists_index = labels.index("num_artists")
	sale_rate_index = labels.index("sale_rate")
	total_vol_index = labels.index("volatility")
	total_skew_index = labels.index("skew")
	lots_per_artist_index = labels.index("lots_per_artist")
	num_artworks_ratio_index = labels.index("num_artworks_ratio")

	artist_counter.pop('NA', None)

	num_artists = len(artist_counter.keys())

	sale_rate = float(auctions_sold) / artwork_count

	for i in range(0,len(exhibition_data)):

		exhibition_data[i][total_skew_index] = skew

		exhibition_data[i][total_vol_index] = vol

		exhibition_data[i][sale_rate_index] = sale_rate

		exhibition_data[i][num_artists_index] = num_artists
		exhibition_data[i][lots_per_artist_index] = float(largest_lot) / num_artists

		exhibition_data[i][avg_price_sold_index] = auctions_average
		exhibition_data[i][median_price_sold_index] = auctions_median

		lot_num = float(exhibition_data[i][lot_index])
		exhibition_data[i][lot_index] = lot_num / largest_lot

		artist = exhibition_data[i][artist_index]
		exhibition_data[i][num_artworks_index] = artist_counter[artist]
		exhibition_data[i][num_artworks_ratio_index] = float(artist_counter[artist]) / largest_lot

	# skip line if missing values 
	exhibition_data = [line for line in exhibition_data if 'NA' not in line] # remove lines with NAs


	return exhibition_data