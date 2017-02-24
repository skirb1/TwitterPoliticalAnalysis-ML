# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from pymongo.errors import DuplicateKeyError
import re
from twython import Twython

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

APP_KEY = "CSihDpnEU1jPuU68ufQA5V3fI"
APP_SECRET = "jiHERTKUCy9eefmC45OwJGtmX15kVIXuSJh52q6u0wXJ43siuY"

OAUTH_TOKEN = "515075514-BPziv1qNt18HnmKEEf5jYLgHbfkZd0m6lyOSgy3u"
OAUTH_TOKEN_SECRET = "N4tUFioEF4FTKyNCV0acRG5KNhWSiykWuESqvg0wGJLYQ"

#connect
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

client = MongoClient()
db = client.twitterproj

db.tweetsMAGA.create_index("id", unique=True)

# url = "https://api.twitter.com/1.1/search/tweets.json?src=typd&q=trump&lang=en"

#first batch: until=2016-12-14

total_count = 0

#while(db.tweetsMAGA.count() < 2000):
count = 0
#max_id_tweet = db.tweets.find({}).sort([("id",1)]).limit(1)[0]
#max_id = max_id_tweet["id"]
#print(max_id)
url_max = "https://api.twitter.com/1.1/search/tweets.json?src=typd&q=%23MAGA&lang=en&count=100&until=2016-12-17"

query = "#MAGA -filter:retweets"
r = twitter.search(q=query, count=100, until=2016-12-17)
print(r)
print("count: " + str(r["search_metadata"]["count"]))
print(r["statuses"])
for tweet in r["statuses"]:
	print("tweet")
	try:
		result = db.tweetsMAGA.insert_one(tweet)
		count += 1
	except DuplicateKeyError:
		print("Duplicate")
		pass
print("Inserted: " + str(count))

total_count += count

print(total_count)
