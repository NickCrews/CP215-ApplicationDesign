'''
extractimages.py
Extracts all of the images from the supplied url and places them in the imgs folder
Nick Crews
2/26/16
'''
import sys
import urllib2
import HTMLParser
import os
from urlparse import urljoin


class ImageParser(HTMLParser.HTMLParser):
	'''Finds and downloads all images from html's'''
	def __init__(self, html):
		HTMLParser.HTMLParser.__init__(self)
		# the text of the html file that will be parsed
		self.html = html
		# list of image urls
		self.image_urls = []

	def handle_starttag(self, tag, attributes):
		'''Overrides method in parent HTMLParser, called repeatedly in feed()'''
		# we don;t care unless this is an img tag
		if tag != 'img': 
			return
		# find the src of this image
		for key, value in attributes:
			if key == 'src':
				self.image_urls.append(value)
				# dont need to keep going
				break

	def get_image_urls(self):
		'''Process the html text and return a list of image urls'''
		# looks through self.html text, and handle_startage will get repeatedly called, adding all image urls to self.images
		self.feed(self.html)
		return self.image_urls

def main(src):
	'''Download all the images in src url or file'''
	# get the urls for all the images and normalize them to absolute paths
	text = get_text(src)
	prsr = ImageParser(text)
	image_urls = prsr.get_image_urls()
	normalized = [urljoin(src, image_url) for image_url in image_urls]

	print zip(image_urls, normalized)

	# the folder that the images will be saved to
	folder = 'extracted_images'
	clean(folder)
	save(normalized, folder)

def clean(folder):
	'''Remove all .jpg images from the specified folder'''
	for f in os.listdir(folder):
		path = folder + os.sep + f
		print 'removing ' + path
		os.remove(path)

def get_text(src):
	'''Get the raw text of the html from the specified url or file'''
	# try to open as a url
	try:
		return urllib2.urlopen(src).read()
	except urllib2.URLError:
		# we couldn't open the src as a url, try it as a file
		try:
			return open(src).read()
		except IOError:
			# uh oh!
			print 'Could not open as a url or as a file: {}'.format(src)
			exit()

def save(imgs, folder):
	'''Download and save all of the images from the urls saved'''
	image_number = 0
	for url in imgs:
		# try to download the image
		try:
			data = urllib2.urlopen(url).read()
		except urllib2.URLError:
			print 'Could not retrieve image from ' + url
			# don't make a file for this image, go on to the next one
			continue

		# now try to save it
		try:
			output_path = folder + os.sep + str(image_number) + '.' + url.split('.')[-1]
			# if we couldn't download the image, then we never create a file
			f = open(output_path, 'w')
			f.write(data)
			f.close

			print 'Saved ' + url + ' as ' + output_path
			image_number += 1
		except IOError:
			print 'Could not save image to ' + output_path 


if __name__ == '__main__':
	'''Get command line arguments and pass them on to main'''
	try:
		src = sys.argv[1]
		main(src)
	except IndexError:
		print 'usage: extractimages src'
		exit()


