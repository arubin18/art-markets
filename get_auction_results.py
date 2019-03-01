from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from scraping_functions import *
import csv

### changing page load strategy 
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "normal"  # complete

### logging into MFA 
driver = webdriver.Chrome(desired_capabilities=caps, executable_path="/usr/lib/chromium-browser/chromedriver")
driver.get("http://www.askart.com/")

### go to directory of auction houses
driver.find_element_by_xpath('//*[@id="menu-item-3"]/a').click()
driver.find_element_by_xpath('//*[@id="menu-item-37"]/a').click()

features = ["Artist:", "Title:", "Price*", "Low Estimate:", "High Estimate:", "Signature:", "Size:", \
				"Created:", "Auction Lot:", "Auction Date:", "Medium:"] 

labels = ["city", "auction_house", "exhibition", "image_url", "artist", "title", "price", "low_estimate", \
	"high_estimate", "signature", "size", "created", "auction_lot", "auction_date", "medium"]

city = "paris"

key = "contemp" # Contemporain for french and contemporary for english

enter_city(driver, city)
driver.find_element_by_xpath('//*[@id="paginator_top"]/a[4]').click()

auction_houses = get_auction_houses(driver)
total = len(auction_houses)

start = 0
end = total

dest = "datasets/" +  "-".join(city.split()).lower() + "/" + "temp" + ".csv" # file destination
with open(dest, "wb") as my_file:
	wr = csv.writer(my_file)
	wr.writerows([labels])

for i in range(start, end):

	auction_houses = get_auction_houses(driver)
	auction_house = auction_houses[i]
	auction_house_name = auction_house.find_element_by_xpath('//*[@id="Container"]/div/table/tbody/tr[2]/td/table/tbody/tr[' + str(i+1) + ']/td[1]/a[1]').text.encode('ascii', 'ignore')

	print (auction_house_name, i)

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
            driver.find_element_by_xpath('//*[@id="paginator_top"]/a[4]').click()
            continue

	auction_house_data = get_auction_house_data(features, key, driver, city, auction_house_name)

	# leave auction house
	driver.find_element_by_xpath('//*[@id="RightColumn"]/table/tbody/tr/td/div/a').click()

	# re enter city name
	enter_city(driver, city)
	driver.find_element_by_xpath('//*[@id="paginator_top"]/a[4]').click()

	with open(dest, "a") as my_file:
		wr = csv.writer(my_file)
		wr.writerows(auction_house_data)




