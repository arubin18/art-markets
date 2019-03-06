import csv
from selenium import webdriver
import time

with open("artists.csv") as f:
	reader = csv.reader(f)
	lines = [line for line in reader][1:]

artists = reduce(lambda x, y: x+y, lines)

def transform_name(name):

	# remove parentheses
	if "(" in name:
		return name.replace("(","").replace(")","")

	else:
		return name

names = map(lambda x: transform_name(x), artists)

#driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver") 
driver.get("http://www.askart.com/")

data = []

for name in names:

	try:
		name_field = driver.find_element_by_xpath('//*[@id="SearchBar_txtSearch"]')
		name_field.clear()
		name_field.send_keys(name)
		time.sleep(1.5)

		auto_complete_field = driver.find_element_by_xpath('//*[@id="ui-id-1"]').find_elements_by_tag_name("li")

		first = auto_complete_field[0].get_attribute('innerHTML').encode('ascii', 'ignore')

		# found matching names
		if first[1] != "d":
			auto_complete_field[0].find_element_by_tag_name("a").click()
		else:
			auto_complete_field[1].find_element_by_tag_name("a").click()

		# get date range
		dates = driver.find_element_by_xpath('//*[@id="MainPageContent_ArtistTOCmain_fvArtistTOCmain"]/tbody/tr/td/div/span').text.encode('ascii', 'ignore')
		dates = dates.strip(" ").strip("(").strip(")") # get rid of extra white space and parentheses

		# artist not dead
		if "born" in dates:
			birth_year = dates.split()[-1]
			death_year = ""

		else:
			birth_year, death_year = dates.split("-")
			birth_year = birth_year.strip(" ")
			death_year = death_year.strip(" ")

	except:
		birth_year, death_year = "", ""

	data.append([name, birth_year, death_year])

data = [["artist", "birth_year", "death_year"]] + data

dest = "dates.csv"

with open(dest, "w") as my_file:
	wr = csv.writer(my_file)
	wr.writerows(data)









