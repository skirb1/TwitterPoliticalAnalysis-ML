from pymongo import MongoClient
import csv
import string
import numpy

#get feature list
features = {}
cread = csv.reader(open("features2.csv", 'r', newline=''))
index = 0
for row in cread:
	features[row[0]] = index
	index += 1

num_features = len(features)
print(str(num_features))

#setup db
client = MongoClient()
db = client.twitterproj
coll_list = ["tweetsMAGA", "tweetsNMP"]

for collstr in coll_list:
	tweets_coll = db[collstr]
	filename = "data2_" + collstr + ".csv"
	cw = csv.writer(open(filename, 'w', newline=''))
	
	for tweet in tweets_coll.find({}).sort([("id",-1)]):
		feat_vec = numpy.zeros((num_features,), dtype=numpy.int)

		words = tweet["text_clean"].split(" ")
		for word in words:
			if(word in features):
				feat_vec[features[word]] += 1
		
		cw.writerow(feat_vec)