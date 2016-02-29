'''
mywave.py
A custom class which wraps the builtin Wave class
Nick Crews
2/23/16
'''
import wave
import struct
import math

class MyWave:

	def __init__(self, frames = []):
		'''Initialize a new Wave object.  Use load to read in an existing file.'''

		# all the params
		self.nchannels = 1
		self.sampwidth = 2
		self.framerate = 8000
		self.comptype = 'NONE'
		self.compname = 'not compressed'

		# a list of floats or ints for each frame value
		self.frames = frames


	def load(self, wavefilename):
		'''Load in a wave file given by wavfilename.'''
		w = wave.open(wavefilename, 'r')

		self.set_params(w.getparams())
			
		raw_frames = w.readframes(w.getnframes())
		format = self._unpack_format(w.getnframes())
		self.frames = list(struct.unpack(format, raw_frames))

	def max_frame(self):
		'''Return the largest wave value in the file.'''
		return max(self.frames)

	def min_frame(self):
		'''Return the smalled wave value in the file.'''
		return min(self.frames)

	def adjust_volume(self, multiplier):
		'''Multiply all the frames by the specified amount'''
		self.frames = map(lambda f: self._clamp(f*multiplier), self.frames)

	def normalize_volume(self):
		'''Adjust the volume so that the max or min frame frame is at the limit of what can be expressed with the current sample width.'''
		M = self.max_frame()
		m = self.min_frame()
		if M == 0 and m == 0:
			return
		elif m == 0:
			scale = float(self.max_poss_val()) / M
		elif M == 0:
			scale = float(self.min_poss_val()) / m
		else:
			scale = min(float(self.max_poss_val()) / M, float(self.min_poss_val()) / m)

		self.adjust_volume(scale)

	def save(self, filename):
		'''Save the wave file to the path filename'''
		# set up our write object
		w = wave.open(filename, 'w')
		params = (self.nchannels, self.sampwidth, self.framerate, 
			len(self), self.comptype, self.compname)
		w.setparams(params)

		# make sure we are constrained if any of our values are out of bound
		if self.max_frame() > self.max_poss_val() or self.min_frame() < self.min_poss_val():
			self.normalize_volume()

		# write the frames
		for f in self.frames:
			format = self._pack_format()
			raw_data = struct.pack(format, int(f))
			w.writeframes(raw_data)

		# save to disk
		w.close()

	def set_sample_width(self, newwidth):
		'''Set sample width, and adjust the volume so it sounds normal'''
		assert newwidth in [1,2,4,8]
		scale = 2**((newwidth - self.sampwidth)*8)
		self.sampwidth = newwidth
		# was this redundant?
		if scale == 1:
			return
		self.adjust_volume(scale)

	def set_framerate(self, newrate):
		'''Change the framerate to the specified amount. When downsampling, loss of quality is expected'''
		assert newrate > 0
		scale = self.framerate / float(newrate)
		self.adjust_speed(scale)
		self.framerate = newrate

	def get_params(self):
		'''Get all the object's params packaged as a nice tuple.'''
		return (self.nchannels, self.sampwidth, self.framerate, self.comptype, self.compname)

	def set_params(self, tup):
		'''Set this object's parameters from a nice tuple. Can handle 5tuples from other MyWave objects, and 6tuples from builtin Wave_read objects'''
		if len(tup) == 6:
			self.nchannels, sw, fr, _, self.comptype, self.compname = tup
		else:
			# its a 5 tuple
			self.nchannels, sw, fr, self.comptype, self.compname = tup
		self.set_sample_width(sw)
		self.set_framerate(fr)

	def copy(self):
		'''Makes a deep copy of this object'''
		clone = new_like(self)
		clone.frames = self.frames[:]
		return clone

	def append(self, other):
		'''Append the other MyWave object to the end of this one'''
		assert self.is_compatible_with(other)
		self.frames += other.frames
		# returns self for chaining
		return self

	def repeat(self, times):
		'''Repeat this waveform a number of times. Does not need to be an integer'''
		frac_part, int_part = math.modf(times)
		print frac_part, int_part
		self.frames *= int(int_part)
		self.frames += self.frames[:int(frac_part*len(self))]
		print len(self), int(frac_part*len(self))


	def gen_wave(self, loudness, freq, dur, typ='SINE'):
		'''Delete any existing frames, and generate a new set with these parameters.loudness is between 0 and 1, feq in hz, dur in seconds'''
		assert loudness >= 0 and loudness <=1
		assert dur > 0
		assert freq > 0
		# do they just want a blank wave?
		if loudness == 0:
			self.frames = [0] * dur*self.framerate
			return
		amp = loudness*self.max_poss_val()
		if typ == 'SINE':
			to_theta = lambda i: i*2.0*math.pi*freq/self.framerate
			self.frames = [amp*math.sin(to_theta(i)) for i in range(int(dur*self.framerate))]
		elif typ == 'SQUARE':
			to_theta = lambda i: i*2.0*math.pi*freq/self.framerate
			self.frames = [math.copysign(amp, math.sin(to_theta(i))) for i in range(int(dur*self.framerate))]
		elif typ == 'TRIANGLE':
			raise ValueError('Unsupported wave type: {}'.format(typ))
		elif typ == 'SAWTOOTH':
			# frames per cycle
			fpc = int(self.framerate/float(freq))
			value = lambda i: amp * (((i+fpc/2)%fpc)-fpc/2)
			self.frames = [value(i) for i in range(int(dur*self.framerate))]
		else:
			raise ValueError('Unsupported wave type: {}'.format(typ))

	def echo(self, delay, decay):
		'''Echos with specified delay (in seconds), decaying by decay at each cycle, until silence'''
		assert len(self) > 0
		# what we somewhat arbitrarily define as silence
		SILENCE = self.max_poss_val() / 1000
		# if our wave is silent, just dont worry about it
		if math.fabs(self.max_frame()) < SILENCE:
			return

		# frames per cycle
		fpc = int(self.framerate * delay)
		# initialize our result and counters
		echoed = self.frames[:fpc]	
		i = fpc
		frames_of_silence = 0
		# while the result hasn't decayed
		while frames_of_silence < fpc:
			# create a base value
			val = self[i] if i<len(self) else 0
			# add in the echo from the past
			val += decay*echoed[i-fpc]
			echoed.append(val)

			frames_of_silence = frames_of_silence+1 if math.fabs(val)<SILENCE else 0
			i += 1
		self.frames = echoed
	

	def chipmunkify(self,scale):
		'''Changes pitch (ie speed) by a factor scale'''
		self.adjust_speed(scale)

	def adjust_speed(self, scale):
		'''changes speed by a factor of scale'''
		assert scale > 0
		self.frames = [self[int(i)] for i in frange(0, len(self), scale)]

	def max_poss_val(self):
		'''What is the largest possible value that can be stored in a frame?'''
		return 2**(self.sampwidth*8-1)-1

	def min_poss_val(self):
		'''What is the smallest possible value that can be stored in a frame?'''
		return -2**(self.sampwidth*8-1)

	def is_compatible_with(self, other):
		'''Does this wave have the same parameters as the other?'''
		return self.get_params() == other.get_params()

	def plot(self):
		try:
			import matplotlib.pyplot as plt
			plt.plot(self.frames, label = self.get_params())
			plt.ylabel('amplitude')
			plt.xlabel('frame')
			plt.legend()
			plt.show()
		except:
			print 'plot() command not supported.'

	def _clamp(self, num):
		'''Clamps a number to the acceptable range for this sample width'''
		M = self.max_poss_val()
		m = self.min_poss_val()
		return max(min(M, num), m)

	def _pack_format(self):
		'''Get the proper format string for packing a frame of data'''
		sw = self.sampwidth
		if sw == 1:
			return '<b'
		elif sw == 2:
			return '<h'
		elif sw == 4:
			return '<l'
		elif sw == 8:
			return '<q'
		else:
			raise ValueError('Not a valid sample width: {}'.format(sw))

	def _unpack_format(self, numframes):
		'''Get the proper format string for unpacking the entire file's worth of data'''
		sw = self.sampwidth
		if sw == 1:
			return '<{}c'.format(numframes)
		elif sw == 2:
			return '<{}h'.format(numframes)
		elif sw == 4:
			return '<{}l'.format(numframes)
		elif sw == 8:
			return '<{}q'.format(numframes)
		else:
			raise ValueError('Not a valid sample width: {}'.format(sw))

	def __str__(self):
		return 'MyWave:' + str(self.frames)

	def __len__(self):
		return len(self.frames)

	def __eq__(self, other):
		'''Are the two MyWaves equal in terms of parameters and values?'''
		if type(other) != type(self):
			return False
		if not self.is_compatible_with(other):
			return False
		return self.frames == other.frames

	def __getitem__(self, index):
		'''Get the respective frame'''
		return self.frames[index]

	def __setitem__(self, index, value):
		'''Set the value of the respective frame'''
		m, M = self.min_poss_val(), self.max_poss_val()
		if value <m  or value > M:
			raise ValueError("Value must be be between {} and {}. Got {}".format(m, M, value))
		self.frames[index] = value

	def __getslice__(self, i1, i2):
		'''This is pretty self explanatory, nothing complicated needs to happen'''
		return self.frames[i1:i2]

	def __add__(self, other):
		'''Add together two wave forms and return a new object (with same parameters as self) that is the combination.'''
		if type(other) != type(self):
			raise TypeError("Can only add two MyWave objects.")
		if not self.is_compatible_with(other):
			raise ValueError("Waves must have same parameters!")

		result = new_like(self)
		result.frames = [sum(x) for x in zip(self.frames, other.frames)]
		# now one or the other might have had more frames, make sure we tack those on
		len_dif = len(self) - len(other)
		if len_dif > 0:
			result.frames += self.frames[-len_dif:]
		elif len_dif < 0:
			result.framerate += other.frames[len_dif:]
		return result

	def __sub__(self, other):
		'''subtract two wave forms and return a new object (with same parameters as self) that is the combination.'''
		result = self.copy()
		result += -other
		return result

	def __neg__(self):
		result = self.copy()
		result.frames = map(lambda f: -f, result.frames)
		return result

def frange(x, y, jump):
	'''A version of the range function which works with floats. Gotten from StackExchange'''
	while x < y:
		yield x
		x += jump

def new_like(oldwave):
	'''Make a new empty Wave object with same params as old one'''
	w = MyWave()
	w.set_params(oldwave.get_params())
	return w


