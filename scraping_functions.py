from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

def get_auction_house_data(features, key, driver, city, auction_house):

	auction_house_data = []
	exhibitions = get_exhibitions(driver)
	total = len(exhibitions)

	for j in range(total):

		exhibitions = get_exhibitions(driver)
		exhibition = exhibitions[j]
		exhibition_name, exhibition_date = exhibition.text.encode('ascii', 'ignore').lower().split("\n")[:2]

		# 5 years
		# if "2013" in exhibition_date:
		# 	break

		if "2008" in exhibition_date:
			break

		if key in exhibition_name and "2019" not in exhibition_date:

			# open exhibition
			driver.find_element_by_xpath('//*[@id="BottomContent"]/table[2]/tbody/tr[' + str(j+1) + ']/td[2]/a').click()
			auction_house_data += get_exhibition_data(features, driver, city, auction_house, exhibition_name)

			# go back to exhibition selection
			driver.find_element_by_xpath('//*[@id="GalleryMenu"]/span/a').click()

	return auction_house_data

def get_exhibition_data(features, driver, city, auction_house, exhibition):

	set_records_per_page(driver)

	num_page = get_page_numbers(driver) # number of pages
	current_page = 1

	exhibition_data = []

	### iterate through pages
	while current_page <= num_page:

		# search through auction records of the exhibition
		exhibition_data += get_auction_data(features, driver, city, auction_house, exhibition) # concatenate lists
		
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

def get_auction_data(features, driver, city, auction_house, exhibition):
	
	### iterate through each artwork
	exhibition_data = []

	artworks = get_artworks(driver)

	for i in range(len(artworks)):

		artworks = get_artworks(driver)
		artwork = artworks[i]

		artwork_data = []
		
		try:

			if artwork.get_attribute("style") == "vertical-align: top;":

				# clean up info list 
				info = artwork.text.encode('ascii', 'ignore').split("\n")
				info = [' '.join(line.split()) for line in info]

				# get features
				variables = get_features(info, features)

				if 'NA' in variables: # if missing value, skip the artwork
					continue

				img_url = artwork.find_element_by_tag_name('img').get_attribute("src").encode('ascii', 'ignore')

				artwork_data = [city, auction_house, exhibition, img_url] + variables

				exhibition_data.append(artwork_data)

		except:
			pass



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




	

