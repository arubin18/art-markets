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

span = 10

labels = [str(year) for year in range(2009-span,2019)]
start_date = labels[0]

driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
# driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
driver.get("http://www.askart.com/")

references = {}

data = []

# iterate through each artist
for name in names:

	for label in labels:
		references[label] = 0

	# initial values 
	total_ref = 0
	birth_year, death_year = "", ""
	ref_count = references.values() # reference counts

	# get birth and death date
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
		time.sleep(0.5)
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
		print ("hi")
		pass


	# artist has references 
	try:
		driver.find_element_by_xpath('//*[@id="MainPageContent_ArtistTOCmain_fvArtistTOCmain"]/tbody/tr/td/div/nav/div/div[5]/a[4]').click()

		# book references 
		try:
			table = driver.find_element_by_xpath('//*[@id="LeftColumn"]/table[2]/tbody')
			rows = table.find_elements_by_tag_name("tr")[2:]
			total_ref = len(rows) # assign count 
			for row in rows:
				date_element = row.find_elements_by_tag_name("div")[0]
				year = date_element.text.encode('ascii', 'ignore') # publication year
				if int(year) < int(start_date):
					break
				if year in references:
					references[year] += 1
		except:
			pass

		# magazine references 
		try:
			driver.find_element_by_xpath('//*[@id="GalleryMenu"]/a').click()
			table = driver.find_element_by_xpath('//*[@id="LeftColumn"]/table[2]/tbody')
			rows = table.find_elements_by_tag_name("tr")[3:]
			total_ref += len(rows)
			for row in rows:
				date_element = row.find_elements_by_tag_name("div")[2]
				year = date_element.split()[-1]
				if int(year) < int(start_date):
					break
				if year in references:
					references[year] += 1

		except:
			pass

	except:
		pass

	ref_count = [count[1] for count in sorted(references.items(), key=lambda x: int(x[0]))]

	references.clear() # clear counts 

	data.append([name, birth_year, death_year, total_ref] + ref_count)

header = [["artist", "birth_year", "death_year", "total"] + labels]
data = header + data

dest = "artist_info.csv"

with open(dest, "w") as my_file:
	wr = csv.writer(my_file)
	wr.writerows(data)









