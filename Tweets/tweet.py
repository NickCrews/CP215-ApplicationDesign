'''
tweet.py
Holds the implementation of the Tweet Class
Nick Crews
2/19/16
'''
import csv

class Tweet:

	def __init__(self, usr, txt, date, polarity):
		# username string of author
		self.usr = usr
		# string of actual Tweet text
		self.txt = txt
		# all dates are represented as strings in format "Mon Apr 06 22:19:49 PDT 2009"
		self.date = date
		# The polarity represents whether the Tweet has a positive message (4), a neutral message (2), or a negative message (0)
		self.polarity = int(polarity)

	@staticmethod
	def fromString(string):
		'''Returns a new Tweet object made from a raw input string from tweets.csv'''
		r = csv.reader([string.strip()])
		fields = list(r)[0]
		return Tweet(*Tweet._parseFields(fields))

	@staticmethod
	def fromFile(filename):
		'''Returns a list of Tweet objects parsed from a file with name filename. Returns None on failure'''
		with open(filename, 'r') as f:
			return [Tweet(*Tweet._parseFields(line)) for line in csv.reader(f)]
		return None

	@staticmethod
	def _parseFields(line):
		'''Given a tuple or list of all the fields in one line of the csv file, return a tuple with only the required fields for a tweet'''
		polarity, ID, date, query, usr, txt = line
		return (usr, txt, date, polarity)


	def __str__(self):
		return "Tweet object: user={}, text='{}', date={}, polarity={}" \
			.format(self.usr, self.txt, self.date, self.polarity)

		