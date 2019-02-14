import csv
import matplotlib.pyplot as plt

f_name = "cnp_artists.txt"

contents = open(f_name).readlines()

contents = [item.strip("\n") for item in contents]

indices = [i for i in range(len(contents)) if "artworks" in contents[i]]
artists = [contents[i-2] for i in indices]

info = [contents[i-1] for i in indices]

for i, artist in enumerate(artists): # remove middle names
	if len(artist.split(" ")) == 3:
		artists[i] = artist.split(" ")[0] + " " + artist.split(" ")[2]

nations = [i.split(",")[0] for i in info] # nationalities

for i in range(len(nations)): # check if nationality not in info list
	if "," not in info[i]:
		nations[i] = "NA" # not available

dates = [] # date of birth - death date

for i in info:
	if "born" in i:
		ind = i.index("born")
		dates.append(i[ind+5:])
	else:
		ind = i.index("-")
		dates.append(i[ind-5:ind-1] + "-" + i[ind+2:ind+7])

### plot histogram of the nationalities
nation_count = {}

for nation in nations:
	if nation not in nation_count:
		nation_count[nation] = 0
	nation_count[nation] += 1

names = sorted(nation_count, key=lambda x: nation_count[x], reverse=True)[:7]
values = [nation_count[name] for name in names]

centers = range(len(names))
plt.bar(centers, values, align='center', tick_label=names)
plt.show()

### save the data
with open("artist_info.csv", "wb") as my_file:
	wr = csv.writer(my_file,quoting=csv.QUOTE_NONE)
	wr.writerow(artists)
	wr.writerow(nations)
	wr.writerow(dates)




