# RWRecommender
Random Walks for Recommender Systems

## Installation

1. Get the Movie-Lens 20M dataset from https://grouplens.org/datasets/movielens/
2. Put the dataset inside a "data" folder so you should be able to access data/ml-20m/ratings.csv
3. Run rw_pre_process_ratings.py, this will read the ratings and build some .json data structures that are used by the recommender.
4. Run the Recommender

## Recommending

1. You can run a recommender for a specific user using:

    python.py rw_reco_by_user.py USERID NUM_ITEMS BETA WALKS

* USERID: Is the ID of the User to recommend (for example 8614)
* NUM_ITEMS: Is the number of items to recommend
* BETA: A parameter that regulates re-starts in the graph (try values from 0.2 to 0.85)
* WALKS: Number of random walks to run (from 1000 to 10000 should be ok try different values)

Note: The recommender takes some time loading the graph.

1. You can run a recommender demo using:

    python.py rw_reco_by_user.py NUM_USERS NUM_ITEMS BETA WALKS

This will run the recommender for a given random number of NUM_USERS
