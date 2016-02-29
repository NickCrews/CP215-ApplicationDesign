'''
test_Wave.py
unit tests for the myWave class
Nick Crews
2/23/16
'''
from mywave import MyWave
import sys

def main():

	C = 523.25
	D = 587.33
	E = 659.25
	F = 698.46
	G = 783.99
	A = 880
	B = 987.77

	mwC = MyWave()
	mwC.gen_wave(.75, C, .25)
	mwD = MyWave()
	mwD.gen_wave(.75, D, .25, typ='SINE')
	mwE = MyWave()
	mwE.gen_wave(.75, E, .25, typ='SINE')
	mwF = MyWave()
	mwF.gen_wave(.75, F, .25, typ='SINE')
	mwG = MyWave()
	mwG.gen_wave(.75, G, .25, typ='SINE')
	mwA = MyWave()
	mwA.gen_wave(.75, A, .25, typ='SINE')
	mwB = MyWave()
	mwB.gen_wave(.75, B, .25, typ='SINE')
	mwC2 = MyWave()
	mwC2.gen_wave(.75, 2*C, .25, typ='SINE')


	scale = mwC.copy()
	scale.append(mwD).append(mwE).append(mwF).append(mwG).append(mwA).append(mwB).append(mwC2)
	scale.plot()


	scale.echo(.5, .3)
	scale.plot()

	scale.repeat(2.5)
	scale.plot()

	scale.save('out.wav')

	

	# added = mwC + mwE + mwG
	# added.plot()
	# added.repeat(5)
	# added.plot()
	# added.save('out.wav')

	# sqr = MyWave()
	# sqr.gen_wave(.75, 4, 1, typ='SQUARE')
	# sqr.plot()
	# inv = -sqr
	# inv.plot()

	# result = sqr - sqr
	# result.plot()

	# sqr -= sqr
	# sqr.plot()
	# sqr.save('out.wav')

	# scale.chipmunkify(2)

	# scale.save('out.wav')



def unittest():
	pass






if __name__ == '__main__':
	try:
		if sys.argv[1] == 'unittest':
			unittest()
	except:
		main()



