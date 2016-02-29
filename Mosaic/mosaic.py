'''
mosaic.py
Contains the Mosaic class and some testing of it.
Nick Crews
2/22/16
'''

from PIL import Image

class Mosaic:

	def __init__(self, width, height):
		self.width, self.height = width, height
		# initialize this other stuff to None, it must be set later
		self.chunk_width, self.chunk_height = None, None
		self.chunk = None
		self.extension = None
		self.image = None


	def setChunk(self, fileName):
		'''Set the tiled image as a PIL Image opened from the specified file'''
		self.chunk = Image.open(fileName)

	def setChunkSize(self, width, height):
		'''Set the actual dimensions in pixels of the tiled chunk'''
		self.chunk_width, self.chunk_height = width, height
		assert self.width % self.chunk_width == 0, 'Chunk width must divide width.'
		assert self.height % self.chunk_height == 0, 'Chunk height must divide width.'

	def setImageType(self, extension):
		'''Set the extension of the file that the image will be saved to.'''
		assert extension.lower() in ['png', 'jpg', 'jpeg', 'tiff', 'gif'], 'Illegal file extension.'
		self.extension = extension

	def drawMosaic(self):
		'''We have already set up our chunk image and the dimensions of the chunk. Create a pattern which we will tile by rotating the chunk and offsetting it. Repeat this pattern across our canvas and save it to self.image'''
		if self.chunk is None:
			raise ValueError("Must set chunk before generating a mosaic.")
		if self.chunk_width is None or self.chunk_height is None:
			raise ValueError("Must set chunk width and height before generating a mosaic.")

		# initialize our canvas and resize our chunk to be copy-and-pastable
		canvas = Image.new('RGB', (self.width, self.height))
		scaled = self.chunk.resize((self.chunk_width, self.chunk_height), Image.ANTIALIAS)

		# make our 4 tiles: topleft(tl), topright(tr), bottomleft(bl), bottomright(br)
		tl, tr, bl, br = scaled, scaled.rotate(270), scaled.rotate(90), scaled.rotate(180)
		# paste in these 4 tiles
		for x in range(0, self.width, 2*self.chunk_width):
			for y in range(0, self.height, 2*self.chunk_height):
				canvas.paste(tl, (x,y))
				canvas.paste(tr,(x+self.chunk_width, y))
				canvas.paste(bl,(x, y+self.chunk_height))
				canvas.paste(br,(x+self.chunk_width, y+self.chunk_height))
		# set our image to be this canvas
		self.image = canvas

	def saveMosaic(self, path):
		'''Save our already created self.image to the specified path with the already picked extension.'''
		if self.image is None:
			raise ValueError("Must generate a mosaic before saving it.")
		if self.extension is None:
			raise ValueError("Must set a file extension before saving mosaic.")
		self.image.save(path + '.' + self.extension)

# Create a new Mosaic object with specified width and height
my_mosaic = Mosaic(850, 650)

# Set the chunk image
my_mosaic.setChunk("chunk.png")

# Set other mosaic parameters
my_mosaic.setChunkSize(25,25)
my_mosaic.setImageType("png")

# Actually create the mosaic image
my_mosaic.drawMosaic()

# Save the generated mosaic image in a file called "beautiful_mosaic"
# The chosen image filetype will determine the file's extension
my_mosaic.saveMosaic("beautiful_mosaic")



