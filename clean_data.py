import numpy as np
import scipy.stats
import uuid

def product (my_list):
	return reduce(lambda x, y: x*y, my_list)

def clean_data(data, labels):

	auctions_sold = 0 # counter for number of auctions sold before the current lot
	auctions_total = 0 # total price of auctions sold before the current lot
	auctions_average = 0 # average price of auctions sold before the current lot
	auctions_median = 0 # mean price of auction sold before the current lot 
	artwork_count = 1 # lots explored in the auction so far
	largest_lot = 1 # will be used to record the largest lot recorded at auction 
	artist_counter = {} # dictionary measuring the number of appearances for each artist 
	vol_returns = 0 # volatility = standard deviation of log returns
	mean_returns = 0 # mean of log returns 
	skew = 0 # skew of prices
	num_artworks = 0 # number of artworks by artist 
	num_artists = 0 # number of artists in auction 
	sale_rate = 0 # sale rate before the current lot in auction 
	lots_per_artist = 0
	num_artworks_ratio = 0
	
	### iterate through each artwork
	exhibition_data = []

	log_returns = [] # log returns based on average estimate 
	log_prices = [] # log transformation of prices 
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

		## clean prices 

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

		# clean average estimate

		if len(low_estimate) == 0 or len(high_estimate) == 0:
			continue

		if not low_estimate[0].isdigit() and not high_estimate[0].isdigit():
			continue

		elif not low_estimate[0].isdigit():
			avg_estimate = float(high_estimate)

		elif not high_estimate[0].isdigit():
			avg_estimate = float(low_estimate)

		else:
			avg_estimate = (float(low_estimate) + float(high_estimate)) / 2

		# estimated to sell for free or for negative money
		if avg_estimate <= 0.0:
			continue

		# clean area and volume 

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

		year_created = year_created.strip(".") # get rid of period 
		year_created = year_created.strip("'") # get rid of final quote

		if "&" in year_created:
			year_created = year_created.split("&")[0].strip(" ")

		elif " " in year_created:
			year_created = year_created.split(" ")[-1] # get rid of ca as a prefix 

		elif "." in year_created:
			year_created = year_created.split(".")[-1] 

		else:
			pass

		# check if price is numerical
		try: 
			price = float(price)

		except:
			continue

		# sold for free 
		if sold == 1 and price == 0.0:
			continue

		artwork_data = [idd, city, exhibition, artist, title, price, sold, avg_estimate, signed, area, \
			volume, year_created, auction_lot, auction_house, auction_date, \
			auctions_average, auctions_median, num_artworks, num_artists, sale_rate, img_url, \
			vol_returns, mean_returns, skew, medium, lots_per_artist, num_artworks_ratio]

		exhibition_data.append(artwork_data) # append artwork data to exhibition data

		artwork_count += 1 # increment total counter

		# update variables 
		if sold == 1:
			
			auctions_sold += 1 # increment sold counter 

			sale_rate = float(auctions_sold) / artwork_count # rate of auctions sold before current lot

			# prices and log prices
			prices.append(price)
			log_prices.append(np.log(price))

			# returns on average estimate 
			sale_return = float(price - avg_estimate) / avg_estimate

			# transform return on average estimate
			if sale_return == 0:
				log_return = 1

			else:
				sign = sale_return / abs(sale_return)
				sale_return = abs(sale_return)
				log_return = sign * np.log(sale_return)

			log_returns.append(log_return)
			
			# descriptions of log returns 
			vol_returns = np.std(log_return) # volatility = standard deviation of log returns
			mean_returns = np.mean(log_returns)

			# descriptions of prices and log prices 
			skew = scipy.stats.skew(prices) # skew of prices 
			auctions_average = np.mean(log_prices) # mean of log prices 
			auctions_median = np.median(prices) # median of prices 

	lot_index = labels.index("auction_lot")
	num_artworks_index = labels.index("num_artworks")
	artist_index = labels.index("artist")
	num_artists_index = labels.index("num_artists")
	lots_per_artist_index = labels.index("lots_per_artist")
	num_artworks_ratio_index = labels.index("num_artworks_ratio")

	artist_counter.pop('NA', None)

	num_artists = len(artist_counter.keys())

	for i in range(len(exhibition_data)):

		exhibition_data[i][num_artists_index] = num_artists
		exhibition_data[i][lots_per_artist_index] = float(artwork_count) / num_artists

		lot_num = float(exhibition_data[i][lot_index])
		exhibition_data[i][lot_index] = lot_num / largest_lot

		artist = exhibition_data[i][artist_index]
		exhibition_data[i][num_artworks_index] = artist_counter[artist]
		exhibition_data[i][num_artworks_ratio_index] = float(artist_counter[artist]) / artwork_count

	# skip line if missing values 
	# exhibition_data = [line for line in exhibition_data if 'NA' not in line] # remove lines with NAs

	return exhibition_data



	