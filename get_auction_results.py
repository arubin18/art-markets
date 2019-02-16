from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from scraping_functions import *
import csv

### changing page load strategy 
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "normal"  #  complete

### logging into MFA
driver = webdriver.Chrome(desired_capabilities=caps, executable_path="/usr/local/bin/chromedriver")
driver.get("http://www.askart.com/")

### go to directory of auction houses
driver.find_element_by_xpath('//*[@id="menu-item-3"]/a').click()
driver.find_element_by_xpath('//*[@id="menu-item-37"]/a').click()

labels = ["idd", "city", "exhibition", "artist", "title", "price", "sold", "auction_fee", "avg_estimate", "signed", "area", \
				"volume", "year_created", "auction_lot", "auction_house", "auction_date", "rate_sold_before", \
				"avg_price_sold_before", "num_artworks", "avg_price_sold", "num_artists", "sale_rate"]

features = ["Artist:", "Title:", "Price*", "Low Estimate:", "High Estimate:", "Signature:", "Size:", \
				"Created:", "Auction Lot:", "Auction Date:", "Medium:"] 

city = "New York"
enter_city(driver, city)

key = "contemporary"

city_data = [labels] # array to hold artwork data for a particular city
auction_houses = get_auction_houses(driver)
# total = len(auction_houses)
total = 1

for i in range(total):

	auction_houses = get_auction_houses(driver)
	auction_house = auction_houses[i]
	auction_house_name = auction_house.find_element_by_xpath('//*[@id="Container"]/div/table/tbody/tr[2]/td/table/tbody/tr[' + str(i+1) + ']/td[1]/a[1]').text.encode('ascii', 'ignore')

	# open exhibitions for auction house 
	auction_house.find_element_by_xpath('//*[@id="Container"]/div/table/tbody/tr[2]/td/table/tbody/tr[' + str(i+1) + ']/td[1]/a[1]').click()
	driver.find_element_by_xpath('//*[@id="GalleryMenu"]/a[1]').click()

	city_data += get_auction_house_data(key, driver, labels, features, city, auction_house_name)

	# leave auction house
	driver.find_element_by_xpath('//*[@id="RightColumn"]/table/tbody/tr/td/div/a').click()

	# re enter city name
	enter_city(driver, city)

print (city_data)

with open("_".join(city.split()) + ".csv", "wb") as my_file:
	wr = csv.writer(my_file)
	wr.writerows(city_data)









