from pymongo import MongoClient
import csv
import string

client = MongoClient()
db = client.twitterproj
coll_list = ["tweetsMAGA", "tweetsNMP"]

word_dict = {}

#get list of all words for first 1000 pos tweets
for collstr in coll_list:
	tweets_coll = db[collstr]
	
	for tweet in tweets_coll.find({}).sort([("id",-1)]).limit(2000):
		#parse text
		words = tweet["text_clean"].split(" ")
		for word in words:
			if(len(word) < 3):			#get rid of short words
				continue

			if(word in word_dict):
				word_dict[word] += 1
			else:
				word_dict[word] = 1

#save set to csv
cw = csv.writer(open("features.csv", 'w', newline=''))
for word in sorted(word_dict, key=word_dict.get, reverse=True):
	cw.writerow([word, word_dict[word]])