from pymongo import MongoClient

client = MongoClient()
db = client.twitterproj
coll_list = ["tweetsMAGA", "tweetsNMP"]

maga_indices = [4140, 3930, 3918, 4351]
nmp_misclass = [3590]
nmp_indices = [4111, 4748, 4599, 2068, 2463]

maga_ids = []
nmp_ids = []

maga_clean = []
nmp_clean = []

tweets_coll = db["tweetsMAGA"]
cursor = tweets_coll.find({}).sort([("id",-1)])
for index in maga_indices:
	tweet = cursor[index]
	maga_ids.append(tweet["id"])
	maga_clean.append(tweet["text_clean"])

tweets_coll = db["tweetsNMP"]
cursor = tweets_coll.find({}).sort([("id",-1)])
for index in nmp_indices:
	tweet = cursor[index]
	nmp_ids.append(tweet["id"])
	nmp_clean.append(tweet["text_clean"])

tweet = cursor[nmp_misclass[0]]
maga_ids.append(tweet["id"])
maga_clean.append(tweet["text_clean"])

#output tweets
file = open('toptweets.txt', 'w')
file.write("Top MAGA tweets:\n\n")
for i in range(len(maga_ids)):
	file.write(str(maga_ids[i]) + "\n")
	file.write(maga_clean[i] + "\n\n")

file.write("Top NMP tweets:\n\n")
for i in range(len(nmp_ids)):
	file.write(str(nmp_ids[i]) + "\n")
	file.write(nmp_clean[i] + "\n\n")

file.close()