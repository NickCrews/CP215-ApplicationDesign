'''
datamining.py
Contains all the functions to mine the Tweet dataset.
Nick Crews
2/19/16
'''
from tweet import Tweet
import string
import sys
import time

def avg_len(tweets):
	'''What is the average length of the text of these tweets?'''
	lengths = [len(t.txt) for t in tweets]
	# make sure we don't just do integer division
	return sum(lengths) / float(len(tweets))

def pct_hashtag(tweets):
	'''What percentage of the Tweets have hashtags?'''
	num_with_hashtag = sum(1 for t in tweets if "#" in t.txt)
	return 100.0 * num_with_hashtag / len(tweets)

def pct_atsign(tweets):
	'''What percentage of the Tweets have @'s?'''
	num_with_atsign = sum(1 for t in tweets if "@" in t.txt)
	return 100.0 * num_with_atsign / len(tweets)

def most_positive_words(tweets, num):
	'''Separate Tweets into positive and negative. What are the words that are in the top 100 most common positive Tweet words that are not in the top 100 most common negative Tweet words?'''
	# pwo = positive word occurences
	# nwo = negative word occurences
	pwo = {}
	nwo = {}
	for tweet in tweets:
		# if positive, add it to positive word count
		if tweet.polarity == 4:
			for word in tweet.txt.split():
				if word in pwo:
					pwo[word] += 1
				else:
					pwo[word] = 1
		# else if the tweet is negative, add it to the negative word count
		elif tweet.polarity == 0:
			for word in tweet.txt.split():
				if word in nwo:
					nwo[word] += 1
				else:
					nwo[word] = 1

	# now we have our two occurence dicts, get the top num in each
	top_positive = sorted(pwo.keys(), key=lambda k: pwo[k], reverse=True)[:num]
	top_negative = sorted(nwo.keys(), key=lambda k: nwo[k], reverse=True)[:num]
	return [word for word in top_positive if word not in top_negative]


def most_common_words(tweets, num):
	'''What are the num most common words used in Tweets?'''
	# wo = word ocurrences
	wo = {}
	for tweet in tweets:
		for word in tweet.txt.split():
			if word in wo:
				wo[word] += 1
			else:
				wo[word] = 1
	return sorted(wo.keys(), key=lambda k: wo[k], reverse=True)[:num]

def pct_containing(tweets, word):
	'''What percentage of the Tweets mention a given word(token separated by spaces)?'''
	num_with_word = sum(1 for t in tweets if word in t.txt.split())
	return 100.0 * num_with_word / len(tweets)

def pct_no_punc(tweets):
	'''What percentage of the Tweets use no punctuation whatsoever?'''
	# count of tweets with no puntuation
	count = 0
	for tweet in tweets:
		# add 1 if there is not any punctuation in the Tweet
		has_punc = any(c in string.punctuation for c in tweet.txt)
		count += 1 if not has_punc else 0 
	return 100.0 * count / len(tweets)


def longest_word(tweets):
	'''What is the longest word contained in all of the tweets?'''
	longest = ''
	for t in tweets:
		candidate_words = t.txt.split() + [longest]
		longest = max(candidate_words, key=lambda word: len(word))
	return longest

def most_active_user(tweets):
	'''Which user has the most Tweets in the dataset?'''
	tpu = {}
	for t in tweets:
		if t.usr in tpu:
			tpu[t.usr] += 1
		else:
			tpu[t.usr] = 1
	# return the user (key) with largest number of tweets (value)
	return max(tpu.keys(), key=lambda k: tpu[k])

def avg_tweets_per_user(tweets):
	'''What is the average number of Tweets per user?'''
	# tpu = tweets per user
	tpu = {}
	for t in tweets:
		if t.usr in tpu:
			tpu[t.usr] += 1
		else:
			tpu[t.usr] = 1
	return sum(tpu.values()) / float(len(tpu))


def busiest_hour(tweets):
	'''What single hour had the most Tweets? Returns a number [0, 23]'''
	# all date strings are of format "Mon Apr 06 22:19:49 PDT 2009"
	# reference http://strftime.org/
	format = '%a %b %d %X PDT %Y'

	# tph = tweets per hour
	# initialize the counts for each of the hours
	tph = {h:0 for h in range(24)}
	for t in tweets:
		# convert the date string into a time tuple and then retrieve the hour field
		hour = time.strptime(t.date, format)[3]
		tph[hour] += 1

	# find the hour with the most tweets
	return max(tph.keys(), key=lambda k: tph[k])


def load_tweets():
	'''Returns a list of Tweet objects loaded from the path specified in the first sys argument'''
	try:
		filepath = sys.argv[1]
	except:
		print("usage: datamining.py filepath")
		quit()
	return Tweet.fromFile(filepath)

def main():
	'''Load the Tweets from file and then find some stats about them!'''
	t = load_tweets()
	print('Average length of Tweet: {} characters'.format(avg_len(t)) )
	print("Percent of Tweets containing a '#': {}".format(pct_hashtag(t)) )
	print("Percent of Tweets containing a '@': {}".format(pct_atsign(t)) )
	N = 100
	print('Most common positive words in Tweets: {}'.format(most_positive_words(t, N)) )
	N = 100
	print('Top {} most common words: {}'.format(N, most_common_words(t, N)) )
	s = 'test'
	print('Percent of Tweets containing the word "{}": {}'.format(s, pct_containing(t, 'test')) )
	print('Percent of Tweets containing no punctuation: {}'.format(pct_no_punc(t)) )
	print('Longest word in any Tweet: {}'.format(longest_word(t)) )
	print('Most active user: {}'.format(most_active_user(t)) )
	print('Average number of Tweets per user: {}'.format(avg_tweets_per_user(t)) )
	print('Busiest hour: {}'.format(busiest_hour(t)) )




if __name__ == '__main__':
	main()

