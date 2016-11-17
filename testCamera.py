#####################################
#
# ECE 5725 Final Project
# Moonyoung Lee (ml634), Peter Slater (pas324)
# Robot Arm Manipulator with Vision
#
#####################################


#==================================
#include packages
#==================================
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
import time
import cv2

import sys
import numpy as np

#==================================
#global variables
#==================================
global greenSkittleList, redSkittleList, state, armDoneSort

greenSkittleList = []
redSkittleList = []

state = 'IDLE'
armDoneSort = 1

#==================================
#class Skittles
#==================================
class Skittles(object):
	
	#common var accessible for all objects
	skittleCount = 0
	
	#initialize skittle object
	def __init__(self,x,y,color,isSorted):
		self.x = x
		self.y = y
		self.color = color
		self.isSorted = isSorted
		Skittles.skittleCount += 1
	
	# return x,y	
	def getPosition(self):
		return (self.x , self.y)
		
	#return color
	def getColor(self):
		return self.color
	
	#return sort boolean
	def getIsSorted(self):
		return self.isSorted
	
	def printSkittle(self):
		print ("color: %s | pos: %s | sort: %s" % (self.getColor(), self.getPosition(), self.getIsSorted()))
		
#==================================
#initialize camera
#==================================
def initCamera():
	global camera, rawCapture
	camera = PiCamera()
	camera.resolution = (640,480)
	camera.framerate = 15
	rawCapture = PiRGBArray(camera, size=(640,480))
	#warm up the camera sensor
	time.sleep(0.1)


#==================================
#while loop for image processing
#==================================
def imageProcess():
	
	#return list of detected skittle
	detectedSkittleList = [] 
	skittleColorCount = 0
	
	#capture video stream in Numpy object
	#opencv represents images in bgr
	for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True ):
		
		image = frame.array
		imageRaw = image.copy()
		
		#print (frame.array.shape[1],frame.array.shape[0])
		
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		#threshold by color
		mask = cv2.inRange(hsv, colorLB, colorUB)
		
		# morphlogical filter 
		mask = cv2.erode(mask, None, iterations = 2)
		mask = cv2.dilate(mask, None, iterations = 2)
			
		
		# find contours from threshold
		contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		

		# Image Algorithm
		# filter all objects detected by size, and circularity 
		for c in contours:
			
			# only big enough size as valid
			if cv2.contourArea(c) > 900:
			    # bound rectangle, w & h should be approx 1
			    
			    x,y,w,h = cv2.boundingRect(c)
			    ratio = float(w)/h
			    #print "ratio: " ,ratio
			    if( ratio > 0.9 and ratio < 1.1):

					#print "size is: " , cv2.contourArea(c)
					
					#get center
					M = cv2.moments(c)
					cX = int(M["m10"]/M["m00"])
					cY = int(M["m01"]/M["m00"])
					
					#print "X: " , cX, "Y: ", cY
					
					#draw circle
					cv2.drawContours(image, [c], -1, (0,255,255), 2)
					#draw center 
					cv2.circle(image, (cX, cY), 7, (255,255,255), -1)
					#write text
					cv2.putText(image, "x,y", (cX-20, cY-20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
					
					#create skittle object
					tempSkittle = Skittles(cX,cY,colorInput,0)
					skittleColorCount += 1
					detectedSkittleList.append(tempSkittle)					 
				    

		#display frame
		cv2.imshow("RAW", imageRaw)
		cv2.imshow("Threshold", mask)
		cv2.imshow("overlay",image)
		key = cv2.waitKey(1) & 0xFF
		
		
		rawCapture.truncate(0)
		
		if key == ord("q"):
			break
		
		# return 
		return detectedSkittleList


#==================================
# get input from keyboard
#==================================
def getColorInput():
	global colorInput, colorLB, colorUB
	
	greenLB = (29,86,6)
	greenUB = (64,255,255)
	redLB = (140,50,50)
	redUB = (200,255,255)
	
	print "Color Choices: [g,r]"
	
	colorInput = raw_input("Color: ")
	#print "selected: ", colorInput
	
	if(colorInput == 'g'):
		print "looking for GREEN skittles"
		#set threshold range for green
		colorLB = greenLB
		colorUB = greenUB
		colorInput = 'g'
		
	
	if(colorInput == 'r'):
		print "looking for RED skittles"
		#set threshold range for red
		colorLB = redLB
		colorUB = redUB
		colorInput = 'r'


#==================================
# print global skittle list
#==================================
def printSkittleList( inputList ):
	
	for obj in inputList:
		obj.printSkittle()

#==================================
# FSM 
#==================================
def FSM():
	
	global state
	
	#=======IDLE========#
	if state == 'IDLE':
		print "IDLE"
		
		#get valid input to move to INIT, else stay in IDLE
		getColorInput()
		
		#valid
		if ((colorInput is 'g') or (colorInput is 'r')):
			state = 'INIT'
		#invalid
		else:
			state = 'IDLE'
			
	#=======INIT========#	
	elif state == 'INIT':
		print "INIT"
		
		if (colorInput is 'g'):
			greenSkittleList = imageProcess()
			if(len(greenSkittleList) != 0):
				printSkittleList(greenSkittleList)
				state = 'SORT'
			
		elif (colorInput is 'r'):
			redSkittleList = imageProcess()
			if(len(redSkittleList) != 0):
				printSkittleList(redSkittleList)
				state = 'SORT'
			

	#=======SORT========#	
	elif state == 'SORT':
		print "SORT"
		
		tempSkittle = imageProcess()
		
		#change condition to include done state w/ ARM
		if ( (len(tempSkittle) == 0) and (armDoneSort) ):
			state = 'IDLE'
			
		else:
			state = 'SORT'
	

			
#==================================
# main loop
#==================================
def main():
	print "STARTING VISION CODE"
	initCamera()
	
	print "entering FSM"
	
	while(1):
		FSM()
	
	
if __name__ == "__main__": 
	
	main()





