'''
FaceBlurrer.py
Takes a video file (or uses the webcam if none is specified) and displays it, blurring out all the faces detected
Nick Crews
2/17/16
'''

import cv2
import sys

# declare this once so we don't have to every frame
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def blurredFaces(frame):
	'''Returns the image frame, but with all the faces blurred out'''
	# convert frame to gray
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces and blur them all out
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for face_bb in faces:
		blurFace(frame, face_bb)

	return frame

def blurFace(img, bb):
	'''Blur the image img in the region defined by bounding box bb'''
	# get x and y coord and width and height
	x,y,w,h = bb
	# get the part of the image which is the face and blur it
	ROI = img[y:y+h, x:x+w]
	blurredROI = cv2.blur(ROI, (19,19))
	# reinsert the blurred rectangle
	img[y:y+h, x:x+w] = blurredROI

def main():
	'''Open a new movie file(or webcam), then display the feed with all the faces blurred out'''
	try:
		# From a movie file
		cap = cv2.VideoCapture(sys.argv[1]) 
	except: 
		# From the webcam   
		cap = cv2.VideoCapture(0)              

	while(cap.isOpened()):
		# get the next frame and resize it
		_, frame = cap.read()
		frame = cv2.resize(frame, (528,300))

		# blur out the faces
		blurred = blurredFaces(frame)

		# show the frame
		cv2.imshow('With faces blurred out', blurred)
		# quit if q is pressed
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# close everything
	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()



