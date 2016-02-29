"""
ScarfWeaver.py
Emulates a loom, with warp and weft threads. Given a pattern of warp threads, draw an image based on the pattern. 
This uses elementary cellular automata to generate each row pattern. I used the model at http://mathworld.wolfram.com/ElementaryCellularAutomaton.html.

Nick Crews
Feb 16, 2016
"""

from PIL import Image, ImageDraw
import sys

# some docomunetation stuff
__author__ = "Nick Crews"
__version__ = 1.0

# Where our output image is written
OUTPUT_PATH = 'scarf.png'
# how many pixels wide is each thread?
THREAD_SIZE = 8

# what are the dimensions in threads?
WIDTH = 201
assert WIDTH%2==1
HEIGHT = 300

#rgb tuples for the thread colors
WARP = (255,0,0)
WEFT = (55,55,55)

# What kind of elementary cellular automata is this scarf going to be?
try:
	RULE_NUMBER = int(sys.argv[1])
except:
	RULE_NUMBER = 150
assert RULE_NUMBER>=0 and RULE_NUMBER<256

def nextRow(row, rule):
	'''Uses rule to compute the next row using rules for elementary cellular automata. 
	row is a list of bits of at least length 2. 
	rule is a list of 8 bits which encodes the rule number. 
	For boundary conditions, I assumed everything past the edge was 0.'''
	assert len(row)>=2
	assert len(rule)==8

	# initialize the next row
	nextRow = [0]*WIDTH

	# deal withleft edge condition

	# get the 3 cells around element 0, with wraparound
	cells = [row[-1]] + row[:2]
	# which pattern of cells is this?
	pattern = getPattern(cells)
	# set the state of the cell in the next row
	nextRow[0] = rule[pattern]

	for i in range(1, WIDTH-1):
		# get the 3 cells around i
		cells = row[i-1:i+2]
		# which pattern of cells is this?
		pattern = getPattern(cells)
		# set the state of the cell in the next row
		nextRow[i] = rule[pattern]

	# deal withleft edge condition

	# get the 3 cells around element 0, with wraparound
	cells = row[-2:] + [row[0]]
	# which pattern of cells is this?
	pattern = getPattern(cells)
	# set the state of the cell in the next row
	nextRow[WIDTH-1] = rule[pattern]

	return nextRow



def drawThread(image, x, y, color):
	"""Draw the block at (x,y) in our image to be color"""
	assert x>=0 and x<WIDTH and y>=0 and y<HEIGHT
	# Create a "draw" object to use to draw shapes onto the image
	draw = ImageDraw.Draw(image)
	draw.rectangle((x*THREAD_SIZE, y*THREAD_SIZE, (x+1)*THREAD_SIZE, (y+1)*THREAD_SIZE), fill=color)

def getPattern(cells):
	'''Which of the eight patterns is this series of 3 cells?'''
	return cells[0]*4 + cells[1]*2 + cells[2]

def drawRow(image, y, pattern):
	'''Draw the pattern at row y to the image'''
	# go through the row, drawing each thread
	for i in range(len(pattern)):
		color = WARP if pattern[i] else WEFT
		drawThread(image, i, y, color)

def generateRule(number):
	'''Given a rule number (0,255) for an elementary cellular automata, generate the 8 bit rule list'''
	result = []
	i = 1
	while i <= number:
		bit = 1 if i & number else 0
		result.append(bit)
		i <<= 1

	# pad the result with 0s so there are always 8
	result += [0]*(8-len(result))
	return result

def randomSeed():
	'''Generate a random but symmetric seed row'''
	import random
	half = [random.randint(0,1) for i in range(WIDTH/2)]
	rev = half[:]
	rev.reverse()
	return half + [random.randint(0,1)] + rev

def standardSeed():
	'''Generate the standard seed row, with all 0s except for a 1 in the center'''
	return [0]*(WIDTH/2) + [1] + [0]*(WIDTH/2)

def specialSeed():
	'''Get a seed which will make a cool pattern with rule 150'''
	seed = [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
	assert WIDTH==len(seed)
	return seed

def main(seed, rule_number):
	'''Initialize our rule and seed row, then step through generations, drawing in our image as we go'''

	# make a new image object
	im = Image.new("RGB", (WIDTH*THREAD_SIZE, HEIGHT*THREAD_SIZE))

	# setup our rule for the automata and our starting row
	rule = generateRule(rule_number)

	# loop through the rows, each row being the child of the row before
	pattern = seed
	for y in range(HEIGHT):
		drawRow(im, y, pattern)
		pattern = nextRow(pattern, rule)

	# save the image to a file
	im.save(OUTPUT_PATH)




if __name__ == '__main__':
	main(specialSeed(), RULE_NUMBER)

