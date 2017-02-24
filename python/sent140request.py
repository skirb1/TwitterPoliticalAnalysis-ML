import requests
from pymongo import MongoClient

url = "http://www.sentiment140.com/api/bulkClassifyJson?appid=skirb1@umbc.edu"

client = MongoClient()
db = client.twitterproj
db.tweet_sentiment.create_index("id", unique=True)

payload = {'data': [] }

#get tweets from most recent batch
#"id":{'$lt':808817993153212416}
for tweet in db.tweets.find({}).sort([("id",1)]).limit(500) :
	sentim_request = {'text': tweet["text"], 'query': 'Trump', 'id': tweet["id"]}
	payload['data'].append(sentim_request)

#send request
r = requests.post(url, json=payload)
print(r.status_code)

#store results
#db.tweet_sentiment is for storing results
if( r.status_code == requests.codes.ok):
	response_json = r.json()
	print(str(len(response_json["data"])))
	db.tweet_sentiment.insert_many(response_json["data"], ordered=False)
