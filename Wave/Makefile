# Makefile for MyWave project
# Nick Crews
# 2/25/16

run:
	python testwave.py
	afplay out.wav

test:
	python testwave.py unittest

clean:
	rm *.pyc *.html out.profile

document:
	pydoc -w mywave testwave unittest

playsrc:
	afplay src.wav

play:
	afplay out.wav

profile:
	python -m cProfile -o out.profile testwave.py

view:
	runsnake32 out.profile
