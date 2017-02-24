import re
from pymongo import MongoClient
import string

client = MongoClient()
db = client.twitterproj

coll_list = ["tweetsMAGA", "tweetsNMP"]

bad_chars = [u'\u2019', u"\u22EF", "'", u"\u203C", "\"\"", "\"", u"\u2026", "#", u"\u000A", u"\u201C", u"\u201D", u"\u0009"]

#REMOVE RTs
# for tweet in coll.find({}):
# 	searchObj = re.search(r' RT ', tweet["text"])
# 	if searchObj:
# 		coll.remove({"id":tweet["id"]})

for collstr in coll_list:
	tweets_coll = db[collstr]
	count = 0
	for tweet in tweets_coll.find({}):
		text = tweet['text']
		#get rid of unicode
		text = text.encode('ascii','ignore').decode('utf-8')

		#get rid of emojis
		emojis = re.compile(u"[\U0001F600-\U0001F64F] | [\U0001F300-\U0001F5FF] | [\U0001F680-\U0001F6FF] | [\U0001F1E0-\U0001F1FF]", re.VERBOSE)
		text = re.sub(emojis, '', text)

		text = re.sub(r'@\S+', '', text)	#remove usernames
		#get rid of punctuation
		for c in string.punctuation:
			text = text.replace(c,"")
		for un in bad_chars:
			text = text.replace(un,"")
		
		text = text.lower()		#convert to lowercase
		text = text.replace("notmypresident", "")	#remove NMP and MAGA hashtags
		text = text.replace("maga", "")
		text = re.sub(r'http\S+', '', text)	#remove links
		text = re.sub(r' +',' ',text)	#remove double spaces

		#print(str(tweet["id"]))
		#print(text)
		result = tweets_coll.update_one({"id":tweet["id"]}, {'$set':{"text_clean":text}}, upsert=False)
		count += result.modified_count
	print(str(count))