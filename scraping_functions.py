from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np

def find(my_string, item):
	return [i for i, x in enumerate(my_string) if x == item]

def enter_city(driver, city_name):
	city_field = driver.find_element_by_xpath('//*[@id="MainPageContent_txtCity"]')
	city_field.clear()
	city_field.send_keys(city_name)
	city_field.send_keys(Keys.RETURN)

def get_value(my_list, key):

	if True not in [key in line for line in my_list]:
		return "NA"

	value_line = [line for line in my_list if key in line][0]

	value = value_line.split(":")[1]

	# value is in the following line 
	if value == '': # got nothing
		index = [i+1 for i in range(len(my_list)) if key in my_list[i]][0]
		value = info[index]

	if value[0] == ' ': # space in front
		value = value[1:]

	return value.strip("\"")

def get_features(my_list, labels):

	features = []

	for label in labels:

		feature = get_value(my_list, label)
		features.append(feature)

	return features

def product (my_list):
	return reduce(lambda x, y: x*y, my_list)

def get_auction_house_data(key, driver, labels, features, city, auction_house):

	auction_house_data = []
	exhibitions = get_exhibitions(driver)
	total = len(exhibitions)

	for j in range(total):

		exhibitions = get_exhibitions(driver)
		exhibition = exhibitions[j]
		exhibition_name = exhibition.text.encode('ascii', 'ignore').lower().split("\n")[0]

		if key in exhibition_name and "2019" not in exhibition_name:

			# open exhibition
			driver.find_element_by_xpath('//*[@id="BottomContent"]/table[2]/tbody/tr[' + str(j+1) + ']/td[2]/a').click()
			auction_house_data += get_exhibition_data(driver, labels, features, city, auction_house, exhibition_name)

			# go back to exhibition selection
			driver.find_element_by_xpath('//*[@id="GalleryMenu"]/span/a').click()

	return auction_house_data

def get_exhibition_data(driver, labels, features, city, auction_house, exhibition):

	set_records_per_page(driver)

	num_page = get_page_numbers(driver) # number of pages
	current_page = 1

	exhibition_data = []

	### iterate through pages
	while current_page <= num_page:

		# search through auction records of the exhibition
		exhibition_data += get_auction_data(driver, labels, features, city, auction_house, exhibition) # concatenate lists
		
		# check if this is the last page 
		if current_page == num_page:
			break

		# go to the next page
		driver.find_element_by_xpath('//*[@id="paginator_top"]/a[3]').click()
		current_page += 1

	return exhibition_data

def get_artworks(driver):
	artwork_page = driver.find_element_by_class_name("ui-helper-clearfix")
	artworks = driver.find_elements_by_tag_name('tr')
	return artworks

def get_auction_data(driver, labels, features, city, auction_house, exhibition):
	
	# auction_page = driver.find_element_by_class_name("ui-helper-clearfix")
	# trs = driver.find_elements_by_tag_name('tr')

	auctions_sold = 0 # counter for number of auctions sold before the current lot
	auctions_total = 0 # total price of auctions sold before the current lot
	auctions_average = 0 # average price of auctions sold before the current lot
	artwork_count = 1 # lots explored in the auction so far
	artist_counter = {}
	vol = 0 # volatility 
	total_vol = 0
	num_artworks = 0
	num_artists = 0
	sale_rate = 0
	avg_price_sold = 0
	
	### iterate through each artwork
	exhibition_data = []

	prices = [] # prices for artworks in exhbitiion

	artworks = get_artworks(driver)
	# total = len(artworks)

	for i, artwork in enumerate(artworks):

		# artwork = get_artworks(driver)[i]

		artwork_data = []
		attribute_value = artwork.get_attribute("style")
		if attribute_value == "vertical-align: top;":

			# clean up info list 
			info = artwork.text.encode('ascii', 'ignore').split("\n")
			info = [' '.join(line.split()) for line in info]

			# get features
			variables = get_features(info, features)

			if 'NA' in variables: # if missing value, skip the artwork
				continue

			artist, title, price, low_estimate, high_estimate, signed, area, \
			year_created, auction_lot, auction_date, medium = variables

			auction_lot = auction_lot.split()[0] # get rid of words following the lot number

			# not sold yet
			if "soon" in price:
				continue # skip this artwork 

			if "withdrawn" in price:
				continue

			# update dictionary with artist as key
			# if type(artist) == str:
			if artist not in artist_counter:
				artist_counter[artist] = 0
			artist_counter[artist] += 1

			auction_fee = [line for line in info if "include" in line or "Includes" in line][0]

			if "include" in auction_fee:
				auction_fee = 0 # does not include auction fee
			else:
				auction_fee = 1

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

			# check if the artwork sold
			if "not" in price:
				sold = 0
				price = "0"

			else:
				sold = 1

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
				dimensions = [float(d.strip(" ").strip("\"")) for d in dimensions]
				
				if len(dimensions) > 2: # more than two dimensions
					area = str(product(dimensions[:-1]))
					volume =  str(product(dimensions))
				
				else: 
					area = str(product(dimensions))
					volume = 0

			# letter at the end of auction lot
			if auction_lot[-1].isalpha():
				auction_lot = auction_lot[:-1]

			# get rid of more than one date
			if "-" in auction_date:
				auction_date = auction_date.split("-")[0]

			# get year
			auction_date_year = auction_date.split("/")[2]

			name_info = artist.split()
			first = name_info[0]
			last = name_info[-1]
			initials = first[0] + last[0]
			idd = initials + auction_date_year + auction_lot

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

			img_url = artwork.find_element_by_tag_name('img').get_attribute("src")

			artwork_data = [idd, city, exhibition, artist, title, price, sold, auction_fee, avg_estimate, signed, area, \
				volume, year_created, auction_lot, auction_house, auction_date, sold_before, \
				auctions_average, num_artworks, avg_price_sold, num_artists, sale_rate, img_url, \
				vol, total_vol]

			exhibition_data.append(artwork_data)

			# update sold counter
			if sold == 1:
				auctions_sold += 1
				auctions_total += int(price)
				prices.append(int(price))
				vol = np.std(prices) # volatility 

				auctions_average = float(auctions_total) / auctions_sold

			artwork_count += 1 # update total counter

			# dest = "images/" + "-".join(city.split()) + "/" + idd + ".jpg"
			# urllib.urlretrieve(url, dest)

			# # open picture 
			# driver.find_element_by_xpath('//*[@id="LeftColumn"]/div[2]/table/tbody/tr['+ str(2*(i+1)) + ']/td[1]/a[2]').click()
			# # close picture
			# driver.find_element_by_xpath('//*[@id="BottomContent"]/div/a[1]').click()

	largest_lot = int(auction_lot) # last lot in for loop 
	lot_index = labels.index("auction_lot")
	num_artworks_index = labels.index("num_artworks")
	artist_index = labels.index("artist")
	avg_price_sold_index = labels.index("avg_price_sold")
	num_artists_index = labels.index("num_artists")
	sale_rate_index = labels.index("sale_rate")
	total_vol_index = labels.index("volatility")

	num_artists = len(artist_counter.keys())

	sale_rate = float(auctions_sold) / artwork_count

	for i in range(0,len(exhibition_data)):

		exhibition_data[i][total_vol_index] = vol

		exhibition_data[i][sale_rate_index] = sale_rate

		exhibition_data[i][num_artists_index] = num_artists

		exhibition_data[i][avg_price_sold_index] = auctions_average

		lot_num = float(exhibition_data[i][lot_index])
		exhibition_data[i][lot_index] = lot_num / largest_lot

		artist = exhibition_data[i][artist_index]
		exhibition_data[i][num_artworks_index] = artist_counter[artist]

	return exhibition_data


def get_auction_houses(driver):
	auction_table = driver.find_element_by_xpath('//*[@id="Container"]/div/table/tbody/tr[2]/td/table')
	auction_houses = auction_table.find_elements_by_tag_name('tr')
	return auction_houses

def get_exhibitions(driver):
	exhibition_table = driver.find_element_by_xpath('//*[@id="BottomContent"]/table[2]')
	exhibitions = exhibition_table.find_elements_by_tag_name('tr')
	return exhibitions

def get_page_numbers(driver):
	
	page_info = driver.find_element_by_xpath('//*[@id="paginator_top"]/a[4]').get_attribute('outerHTML').encode('ascii', 'ignore')
	num_page = int(page_info.split("\"")[1].split("=")[1])

	return num_page

def set_records_per_page(driver):
	# set records per page to 100
	driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[2]/td[2]/div").click()
	driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[2]/td[2]/div/div[2]/div/div[5]").click()

