from __future__ import division
import csv
import numpy as np
import math
import random
import operator
import itertools
import pickle
import json
import sys

# THIS RECEIVES


num_users=1
users_to_recommend = [int(sys.argv[1:][0])]
num_recs = int(sys.argv[1:][1])
BETA = float(sys.argv[1:][2])
WALKS = int(sys.argv[1:][3])

print "Loading Data..."
with open('f_all_users.json', 'r') as f:
	all_users = json.load(f)

with open('f_item_names.json', 'r') as f:
	item_names = json.load(f)	

with open('f_item_averages.json', 'r') as f:
	item_averages = json.load(f)	


with open('f_item_edges.json', 'r') as f:
	item_edges = json.load(f)		

with open('f_user_edges.json', 'r') as f:
	user_edges = json.load(f)		

with open('items_liked_by_user.json', 'r') as f:
	items_liked_by_user = json.load(f)

with open('items_disliked_by_user.json', 'r') as f:
	items_disliked_by_user = json.load(f)

print "Done!"


def compute_user_to_item_edge_score(rating,item_average):	
	return 0.5*rating + 0.5*item_average

def compute_item_to_user_edge_score(rating,item_average):	
	return rating


def recommend(user,BETA,WALKS):
	recommendations = {}
	original_user = user
	if not user in user_edges:
		return recommendations
	already_ranked = [str(x[0]) for x in user_edges[original_user]]
	for i in xrange(WALKS):
		if random.random()>=BETA:
			user = original_user
		if user in user_edges:
			edges = user_edges[user]
			# Substract averages and keep only positive items (for the user)
			#edges = [(str(x[0]),compute_user_to_item(float(x[1]),item_averages[str(x[0])]) for x in edges if float(x[1])-(item_averages[str(x[0])])]
			edges = [(str(x[0]),compute_user_to_item_edge_score(float(x[1]),item_averages[str(x[0])])) for x in edges]
			# Convert to a list of items and weights
			[items,weights] = zip(*edges)
			# Convert weights to probabilities
			total_weight = np.sum(weights)
			probs = [p/total_weight for p in weights]
			item = np.random.choice(items,size=1,replace=True,p=probs)
			#theweight =item[1]
			item = item[0]
			if item not in already_ranked:
				#print "selected: ",item_names[item]," ",item
				if item not in recommendations:
					recommendations[item]=0
				recommendations[item]+=1
			if item in item_edges:
				edges = item_edges[item]
				# Substract averages and keep only positive items (for the user)
				edges = [(str(x[0]),compute_item_to_user_edge_score(float(x[1]),item_averages[item])) for x in edges]
				# Convert to a list of items and weights
				[users,weights] = zip(*edges)
				# Convert weights to probabilities
				total_weight = np.sum(weights)
				probs = [p/total_weight for p in weights]
				user = np.random.choice(users,size=1,replace=False,p=probs)
				user = user[0]
	sorted_items = sorted(recommendations.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_items

for user in users_to_recommend:
	user = str(user)
	if user in items_liked_by_user:
		good_items = items_liked_by_user[user]	
		print "recommending for user:",user
		liked_names = ",".join([item_names[str(item)] for item in good_items])
		print "***** The User Likes:",liked_names
	if user in items_disliked_by_user:
		bad_items = items_disliked_by_user[user]
		unliked_names = ",".join([item_names[str(item)] for item in bad_items])
		print "* The User Dislikes:",unliked_names
	recommended_items = recommend(user,BETA,WALKS)
	print "We recommend:"
	for item in recommended_items[0:num_recs]:
		name = item_names[str(item[0])]
		print item[0],name,item[1]
	print "----------------------"

