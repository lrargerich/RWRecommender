from __future__ import division
import csv
import numpy as np
import math
import random
import operator
import itertools
import pickle
import json

item_averages = {}
item_ratings = {}
item_names = {}
item_edges = {}
user_edges = {}
items_liked_by_user = {}
items_disliked_by_user = {}


def load_items(filename):
	total_items = 0
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		# Skip header
		next(csvreader)
		for row in csvreader:
			if not int(row[0]) in item_names:
				item_names[int(row[0])] = row[1]
				total_items+=1
	print "Loaded:"+str(total_items)+" items"


# Load the ML dataset 
# or any other dataset in the
# same format
# userid, itemid, rating, timestamp
def load_ratings(filename):
	total_ratings = 0
	unknown_items = 0
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		# Skip header
		next(csvreader)
		for row in csvreader:
			userid = int(row[0])
			itemid = int(row[1])
			rating = float(row[2])			
			if not itemid in item_ratings:
				item_ratings[itemid] = []
			item_ratings[itemid].append(rating)
			if not itemid in item_edges:
				item_edges[itemid]=[]
			if not userid in user_edges:
				user_edges[userid]=[]
			item_edges[itemid].append((userid,rating))
			user_edges[userid].append((itemid,rating))
			if rating==5:
				if not userid in items_liked_by_user:
					items_liked_by_user[userid]=[]
				items_liked_by_user[userid].append(itemid)
			if rating==1:
				if not userid in items_disliked_by_user:
					items_disliked_by_user[userid]=[]
				items_disliked_by_user[userid].append(itemid)
	return


print "Loading Items"
load_items('data/ml-20m/movies.csv')
with open('f_item_names.json', 'w') as f:
    json.dump(item_names, f)

print "Loading Ratings"
load_ratings('data/ml-20m/ratings.csv')
print "Done!"
f_all_users = user_edges.keys()

for item in item_ratings:
	item_averages[item]=np.mean(item_ratings[item])

with open('f_item_averages.json', 'w') as f:
    json.dump(item_averages, f)

with open('f_all_users.json', 'w') as f:
    json.dump(f_all_users, f)

with open('f_item_edges.json', 'w') as f:
    json.dump(item_edges, f)

with open('f_user_edges.json', 'w') as f:
    json.dump(user_edges, f)

with open('items_liked_by_user.json', 'w') as f:
    json.dump(items_liked_by_user, f)

with open('items_disliked_by_user.json', 'w') as f:
    json.dump(items_disliked_by_user, f)


print "All ratings and items processed"