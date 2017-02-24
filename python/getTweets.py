# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from pymongo.errors import DuplicateKeyError
import re

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "CSihDpnEU1jPuU68ufQA5V3fI"
CONSUMER_SECRET = "jiHERTKUCy9eefmC45OwJGtmX15kVIXuSJh52q6u0wXJ43siuY"

OAUTH_TOKEN = "515075514-BPziv1qNt18HnmKEEf5jYLgHbfkZd0m6lyOSgy3u"
OAUTH_TOKEN_SECRET = "N4tUFioEF4FTKyNCV0acRG5KNhWSiykWuESqvg0wGJLYQ"

## Function from: https://thomassileo.name/blog/2013/01/25/using-twitter-rest-api-v1-dot-1-with-python/
def get_oauth():
	oauth = OAuth1(CONSUMER_KEY,
				client_secret=CONSUMER_SECRET,
				resource_owner_key=OAUTH_TOKEN,
				resource_owner_secret=OAUTH_TOKEN_SECRET)
	return oauth

### MAIN CODE ####
print("main code:"+ "\n")

client = MongoClient()
db = client.twitterproj
coll = db["tweetsNMP"]
coll.create_index("id", unique=True)

if __name__ == "__main__":
	oauth = get_oauth()

	total_count = 0
	while(coll.count() < 5000):
		count = 0
		dup_count = 0
		max_id_tweet = coll.find({}).sort([("id",1)]).limit(1)[0]
		max_id = max_id_tweet["id"]
		print(max_id)

		#MAGA query = "-%23NotMyPresident%20%23MAGA%20-filter%3Aretweets%20-filter%3Areplies"
		#NMP
		query = "%23NotMyPresident%20-%23MAGA%20-filter%3Aretweets%20-filter%3Areplies"
		url_max = "https://api.twitter.com/1.1/search/tweets.json?src=typd&q=" + query + "&lang=en&count=100"
		#url_max = url_max + "&until=2016-12-15"
		url_max = url_max + "&max_id=" + str(max_id)

		r = requests.get(url= url_max, auth=oauth)

		if(r.status_code == requests.codes.ok):
			print(len(r.json()["statuses"]))

			for tweet in r.json()["statuses"]:
				searchObj = re.search(r' RT ', tweet["text"])
				if searchObj:
					continue
				try:
					result = coll.insert_one(tweet)
					count += 1
				except DuplicateKeyError:
					dup_count += 1
					pass
			print("Duplicates: " + str(dup_count))
			print("Inserted: " + str(count))
		else:
			print(r.text)
		total_count += count

	print(total_count)

		# try:
		# 	result = db.tweets.insert_many(r.json()["statuses"], ordered=False)
		# 	print("inserted: " + str(len(result.inserted_ids)))
		# except BulkWriteError:
		# 	pass
		