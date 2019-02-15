from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import csv

def find(my_string, item):
	return [i for i, x in enumerate(my_string) if x == item]

def get_value(my_list, key):

	# check = [key in line for line in my_list]

	# if True not in check:
	# 	return ""

	value_line = [line for line in my_list if key in line][0]

	# if ":" not in value_line:
	# 	return line.split()[1:]

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

f_name = "artist_info.csv"
contents = np.array(open(f_name).read().split("\n"))
names = contents[0].split(",")
names[-1] = names[-1].strip("\r")

### logging into MFA

driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
driver.get("http://www.askart.com/")

### get auction records
driver.find_element_by_xpath('//*[@id="menu-item-3"]/a').click()
driver.find_element_by_xpath('//*[@id="menu-item-37"]/a').click()

### iterate through auction houses
table_frame = driver.find_element_by_xpath('//*[@id="Container"]/div/table/tbody/tr[2]/td/table')
houses_tf = table_frame.find_elements_by_tag_name('tr')
i = 0
test_house = houses_tf[i] # test auction house

auction_house = test_house.find_element_by_xpath('//*[@id="Container"]/div/table/tbody/tr[2]/td/table/tbody/tr[' + str(i+1) + ']/td[1]/a[1]').text.encode('ascii', 'ignore')

print (auction_house)

test_house.find_element_by_xpath('//*[@id="Container"]/div/table/tbody/tr[2]/td/table/tbody/tr[' + str(i+1) + ']/td[1]/a[1]').click()

### iterate through exhibitions
driver.find_element_by_xpath('//*[@id="GalleryMenu"]/a[1]').click() # look through auctions 
exhibition_tf = driver.find_element_by_xpath('//*[@id="BottomContent"]/table[2]')
exhibitions = exhibition_tf.find_elements_by_tag_name('tr')
j = 0
test_exhibition = exhibitions[0]

exhibition_name = test_exhibition.text.encode('ascii', 'ignore').lower()

if "contemporary" in exhibition_name:
	print ("yes")

test_exhibition.find_element_by_xpath('//*[@id="BottomContent"]/table[2]/tbody/tr[' + str(j+1) + ']/td[2]/a').click()

### filter information
# driver.find_element_by_xpath('//*[@id="AuctionRecordFilter"]/table[2]/tbody/tr[2]/td[1]/div/div[1]').click()
# driver.find_element_by_xpath('//*[@id="AuctionRecordFilter"]/table[2]/tbody/tr[2]/td[1]/div/div[2]/div/div[6]').click()

# test_artist = names[0]

# ### search the artist 
# clicker = driver.find_element_by_css_selector("#SearchBar_txtSearch")
# clicker.send_keys(test_artist)
# driver.find_element_by_css_selector("#SearchBar_searchButton").click()

# # open auction records
# driver.find_element_by_xpath("//*[@id='MainPageContent_ArtistTOCmain_fvArtistTOCmain']/tbody/tr/td/div/nav/div/div[3]/a[2]/div").click()

# ### filter auction information
# # type of artwork
# driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[2]/td[1]/div").click()
# driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[2]/td[1]/div/div[2]/div/div[2]").click()
# # records per page

driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[2]/td[2]/div").click()
driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[2]/td[2]/div/div[2]/div/div[5]").click()

# # medium
# driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[3]/td[2]/div").click()
# driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[3]/td[2]/div/div[2]/div/div[2]").click()
# # year - only look at past works (pre 2019)
# driver.find_element_by_xpath('//*[@id="AuctionRecordFilter"]/table/tbody/tr[5]/td[2]/div[3]').click()
# driver.find_element_by_xpath('//*[@id="AuctionRecordFilter"]/table/tbody/tr[5]/td[2]/div[3]/div[2]/div/div[2]').click()

# ### get page numbers
page_info = driver.find_element_by_xpath('//*[@id="paginator_top"]/a[4]').get_attribute('outerHTML').encode('ascii', 'ignore')
num_page = int(page_info.split("\"")[1].split("=")[1])

num_page = 1 # TEMPORARY

current_page = 1

labels = ["idd", "artist", "title", "price", "auction_fee", "low_estimate", "high_estimate", "signed", "area", \
				"year_created", "auction_lot", "auction_house", "auction_date", "sold_before", \
				"avg_sold_before"]

features = ["Artist:", "Title", "Price", "Low Estimate", "High Estimate", "Signature", "Size", \
				"Created", "Auciton Lot", "Auction Date"] 

auction_data = [labels]

### iterate through pages
while current_page <= num_page:

	# search through auction records
	auction_page = driver.find_element_by_class_name("ui-helper-clearfix")
	trs = driver.find_elements_by_tag_name('tr')

	auctions_sold = 0 # counter for number of auctions sold before the current lot
	auctions_total = 0 # total price of auctions sold before the current lot
	auctions_average = 0 # average price of auctions sold before the current lot
	lot_count = 1 # lots explored in the auction so far
	artist_counter = {}
	
	### iterate through each artwork
	for tr in trs:
		artwork_data = []
		attribute_value = tr.get_attribute("style")
		if attribute_value == "vertical-align: top;":

			# clean up info list 
			info = tr.text.encode('ascii', 'ignore').split("\n")
			info = [' '.join(line.split()) for line in info]

			# get features
			artist, title, price, low_estimate, high_estimate, signed, area, \
			year_created, auction_lot, auction_date = get_features(info, features)

			# update dictionary with artist as key
			if type(artist) == str:
				if artist not in artist_counter:
					artist_counter[artist] = 0
				artist_counter[artist] += 1

			# includes auction fee
			# if price == "":
			# 	price = get_value(info, "Sales Price")

			auction_fee = [line for line in info if "include" in line or "Includes" in line][0]

			if "include" in auction_fee:
				auction_fee = 0 # does not include auction fee
			else:
				auction_fee = 1

			# remove euro conversions
			if "(" in price:
				price = price.split("(")[0][1:-1]

			if "(" in low_estimate:
				low_estimate = low_estimate.split("(")[0][1:-1]

			if "(" in high_estimate:
				high_estimate = high_estimate.split("(")[0][1:-1]

			# width, length = area.split("x")
			# width = float(width[:-2])
			# length = float(length[1:])
			# area = width*length 

			# get year
			auction_date_year = auction_date.split("/")[2]

			# name_info = artist.split()
			# first = name_info[0]
			# last = name_info[-1]
			# initials = first[0] + last[0]
			# idd = initials + auction_date_year + auction_lot
			idd = auction_date_year + auction_lot

			artwork_data = [idd, artist, title, price, auction_fee, low_estimate, high_estimate, signed, area, \
				year_created, auction_lot, auction_house, auction_date, float(auctions_sold) / int(lot_count), \
				auctions_average]

			auction_data.append(artwork_data)

			# update counts
			if "not" not in price:
				auctions_sold += 1
				auctions_total += int("".join(price.split(",")))
				auctions_average = float(auctions_total) / auctions_sold

			lot_count += 1

			print (info)

	if current_page == num_page:
		break

	# go to the next page
	driver.find_element_by_xpath('//*[@id="paginator_top"]/a[3]').click()
	current_page += 1

# with open("test.csv", "wb") as my_file:
# 	wr = csv.writer(my_file)
# 	wr.writerows(auction_data)









