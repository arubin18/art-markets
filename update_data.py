import numpy as np
from parse_data import *
from download_images import *
from update_prices import *
from add_features import *

labels = ["idd", "city", "exhibition", "artist", "title", "price", "sold", "avg_estimate", "signed", "area", \
				"volume", "year_created", "auction_lot", "auction_house", "auction_date", "rate_sold_before", \
				"avg_price_sold_before", "median_price_sold_before", "num_artworks", "avg_price_sold", "median_price_sold",\
				"num_artists", "sale_rate", "img_url", "volatility_before", "volatility", "skew_before", "skew", 
				"medium", "lots_per_artist", "num_artworks_ratio"]

cities = ["New York", "London", "Paris"]

for city in cities:
	print (city)
	parse_data(city, labels)
	update_prices(city)






