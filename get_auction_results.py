from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from scraping_functions import *
import csv

### changing page load strategy 
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "normal"  # complete

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--proxy-server='direct://'");
# chrome_options.add_argument("--proxy-bypass-list=*");

### logging into MFA 
driver = webdriver.Chrome(desired_capabilities=caps, executable_path="/usr/lib/chromium-browser/chromedriver")
# driver = webdriver.Chrome(desired_capabilities=caps, executable_path="/usr/local/bin/chromedriver")
driver.get("http://www.askart.com/")

### go to directory of auction houses
driver.find_element_by_xpath('//*[@id="menu-item-3"]/a').click()
driver.find_element_by_xpath('//*[@id="menu-item-37"]/a').click()

# labels = ["idd", "city", "exhibition", "artist", "title", "price", "sold", "auction_fee", "avg_estimate", "signed", "area", \
# 				"volume", "year_created", "auction_lot", "auction_house", "auction_date", "rate_sold_before", \
# 				"avg_price_sold_before", "num_artworks", "avg_price_sold", "num_artists", "sale_rate", "img_url", \
# 				"volatility_before", "volatility", "skew_before", "skew"]

features = ["Artist:", "Title:", "Price*", "Low Estimate:", "High Estimate:", "Signature:", "Size:", \
				"Created:", "Auction Lot:", "Auction Date:", "Medium:"] 

labels = ["city", "auction_house", "exhibition", "image_url", "artist", "title", "price", "low_estimate", \
	"high_estimate", "signature", "size", "created", "auction_lot", "auction_date", "medium"]

# labels = ["city", "auction_house"exhibition_date, "exhibition", "image_url", "info_array"]

city = "paris"

key = "contemporary"

enter_city(driver, city)

### get page numbers
try:
	page_info = driver.find_element_by_xpath('//*[@id="paginator_top"]/a[4]').get_attribute('outerHTML').encode('ascii', 'ignore')
	num_page = int(page_info.split(" ")[1].split("=")[-1][:-1])
	extra = True # boolean indicating extra pages 

except:
	num_page = 1
	extra = False

auction_houses = get_auction_houses(driver)
total = len(auction_houses)
dest = "datasets/" +  "-".join(city.split()).lower() + "/" + "temp" + ".csv" # file destination

start = 0
end = total

with open(dest, "wb") as my_file:
	wr = csv.writer(my_file)
	wr.writerows([labels])

for j in range(num_page):

        if j == 0:
            start = 5

	for i in range(start, end):

		auction_houses = get_auction_houses(driver)
		auction_house = auction_houses[i]
		auction_house_name = auction_house.find_element_by_xpath('//*[@id="Container"]/div/table/tbody/tr[2]/td/table/tbody/tr[' + str(i+1) + ']/td[1]/a[1]').text.encode('ascii', 'ignore')

		print (auction_house_name)

		# open exhibitions for auction house 
		auction_house.find_element_by_xpath('//*[@id="Container"]/div/table/tbody/tr[2]/td/table/tbody/tr[' + str(i+1) + ']/td[1]/a[1]').click()
	        
	        try:	
		    # find auctions option
		    gallery_menu = driver.find_element_by_xpath('//*[@id="GalleryMenu"]')
		    options = gallery_menu.find_elements_by_class_name("dealermenu")
		    auction_index = [i for i in range(len(options)) if options[i].text == "Auctions"][0]
		    options[auction_index].click()

	        except:
	            # leave auction house
	            driver.find_element_by_xpath('//*[@id="RightColumn"]/table/tbody/tr/td/div/a').click()

	            # re enter city name
	            enter_city(driver, city)
	            continue

		auction_house_data = get_auction_house_data(features, key, driver, city, auction_house_name)

		# leave auction house
		driver.find_element_by_xpath('//*[@id="RightColumn"]/table/tbody/tr/td/div/a').click()

		# re enter city name
		enter_city(driver, city)

		with open(dest, "a") as my_file:
			wr = csv.writer(my_file)
			wr.writerows(auction_house_data)

	if j == num_page - 1: # last page
		break

	# if extra pages, go to the next page 
	if extra:
		driver.find_element_by_xpath('//*[@id="paginator_top"]/a[4]').click()




