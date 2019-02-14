from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import csv

def find(my_string, item):
	return [i for i, x in enumerate(my_string) if x == item]

f_name = "artist_info.csv"
contents = np.array(open(f_name).read().split("\n"))
names = contents[0].split(",")
names[-1] = names[-1].strip("\r")

### logging into MFA

driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
driver.get("http://www.askart.com/")

test_artist = names[0]

### search the artist 
clicker = driver.find_element_by_css_selector("#SearchBar_txtSearch")
clicker.send_keys(test_artist)
driver.find_element_by_css_selector("#SearchBar_searchButton").click()

# open auction records
driver.find_element_by_xpath("//*[@id='MainPageContent_ArtistTOCmain_fvArtistTOCmain']/tbody/tr/td/div/nav/div/div[3]/a[2]/div").click()

### filter auction information
# type of artwork
driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[2]/td[1]/div").click()
driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[2]/td[1]/div/div[2]/div/div[2]").click()
# records per page
driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[2]/td[2]/div").click()
driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[2]/td[2]/div/div[2]/div/div[5]").click()
# medium
driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[3]/td[2]/div").click()
driver.find_element_by_xpath("//*[@id='AuctionRecordFilter']/table/tbody/tr[3]/td[2]/div/div[2]/div/div[2]").click()
# year - only look at past works (pre 2019)
driver.find_element_by_xpath('//*[@id="AuctionRecordFilter"]/table/tbody/tr[5]/td[2]/div[3]').click()
driver.find_element_by_xpath('//*[@id="AuctionRecordFilter"]/table/tbody/tr[5]/td[2]/div[3]/div[2]/div/div[2]').click()

### get page numbers
page_info = driver.find_element_by_xpath('//*[@id="paginator_top"]/a[4]').get_attribute('outerHTML').encode('ascii', 'ignore')
num_page = int(page_info.split("\"")[1].split("=")[1])

# num_page = 1 # TEMPORARY

current_page = 1

labels = ["id", "title", "hammer", "auction_fee", "low_estimate", "high_estimate", "signed", "area", \
				"year_created", "auction_lot", "auction_house", "auction_date"]
artist_data = [labels] # list to hold all data for this artist 


def get_value(my_list, key):

	check = [key in line for line in my_list]

	if True not in check:
		return ""

	value = [line.split(":")[1] for line in my_list if key in line][0]

	# value is in the following line 
	if value == '': # got nothing
		index = [i+1 for i in range(len(my_list)) if key in my_list[i]][0]
		value = info[index]

	if value[0] == ' ': # space in front
		value = value[1:]

	return value.strip("\"")

### iterate through pages
while current_page <= num_page:

	# search through auction records
	auction_page = driver.find_element_by_class_name("ui-helper-clearfix")
	trs = driver.find_elements_by_tag_name('tr')
	
	### iterate through each artwork
	for tr in trs:
		artwork_data = []
		attribute_value = tr.get_attribute("style")
		if attribute_value == "vertical-align: top;":

			info = tr.text.encode('ascii', 'ignore').split("\n")
			info = [' '.join(line.split()) for line in info]

			title = get_value(info, "Title")
			price = get_value(info, "Hammer Price")

			if price == "":
				price = get_value(info, "Sales Price")

			auction_fee = [line for line in info if "include" in line or "Includes" in line][0]

			if "include" in auction_fee:
				auction_fee = 0 # does not include auction fee
			else:
				auction_fee = 1

			low_estimate = get_value(info, "Low Estimate")
			high_estimate = get_value(info, "High Estimate")
			signed = get_value(info, "Signature")
			area = get_value(info, "Size")
			width, length = area.split("x")
			width = float(width[:-2])
			length = float(length[1:])
			area = width*length 

			year_created = get_value(info, "Created")
			auction_lot = get_value(info, "Auction Lot")
			auction_house = get_value(info, "Auction House") 
			auction_date = get_value(info, "Auction Date")
			auction_date_year = auction_date.split("/")[2]

			# if auction_date.count("/") > 2:
			# 	auction_date_year = auction_date.split("/")[2].split("-")[0]
			
			# else:			
			# 	auction_date_year = int(auction_date.split("/")[2])

			# 	if auction_date_year < 80: # 2000-2018
			# 		auction_date_year = "20" + str(auction_date_year)
			# 	else: # 1980-1999
			# 		auction_date_year = "19" + str(auction_date_year)

			# auction_date = auction_date.split("/")[:2] + auction_date_year

			first, last = test_artist.split()
			initials = first[0] + last[0]
			idd = initials + auction_date_year + auction_lot

			artwork_data = [idd, title, price, auction_fee, low_estimate, high_estimate, signed, area, \
				year_created, auction_lot, auction_house, auction_date]

			artist_data.append(artwork_data)

	if current_page == num_page:
		break

	# go to the next page
	driver.find_element_by_xpath('//*[@id="paginator_top"]/a[3]').click()
	current_page += 1

with open("test.csv", "wb") as my_file:
	wr = csv.writer(my_file)
	wr.writerows(artist_data)









