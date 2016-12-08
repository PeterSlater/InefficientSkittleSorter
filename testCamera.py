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
import math

#include for control and serial
import mearm.control as arm
import atexit
import time

#==================================
#global variables
#==================================
global greenSkittleList, redSkittleList, yellowSkittleList, state, armDoneSort, clawX, clawY
global tempRedSkittleListPos, tempRedIncrement, medianPositions
global serial
global deltaX, deltaY

# Create the arm serial port
serial = arm.init()
	
greenSkittleList = []
redSkittleList = []
yellowSkittleList = []
tempRedIncrement = 0

deltaX = 0
deltaY = 0

#defines
clawGreenPixelSize = 100
skittlePixelSize = 150 
medianSize = 5
numRedSkittle = 3 #CHANGE FOR DEMO
close2Object = 10 #pixel radius

#temp global var to hold live video update values
tempRedSkittleListPos = [ [(0,0) for x in range(medianSize)] for y in range(numRedSkittle) ]
medianPositions = [ [(0,0)] for y in range(numRedSkittle) ]  #[ (x,y) , (x,y) ]

state = 'IDLE'
armDoneSort = 1

#initiailize claw Position
clawX = 290
clawY = 360


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
# Always close the serial port on exit
#==================================
def close():
	arm.close(serial)
atexit.register(close)

		
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
	time.sleep(0.5)


#==================================
#while loop for image processing
#==================================
def imageProcess():
	
	global clawX, clawY
		
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

		#threshold by color for skittle and claw
		mask = cv2.inRange(hsv, colorLB, colorUB)
		maskClaw = cv2.inRange(hsv, greenLB, greenUB)
		
		
		# morphlogical filter 
		mask = cv2.erode(mask, None, iterations = 2)
		mask = cv2.dilate(mask, None, iterations = 2)
		
		maskClaw = cv2.erode(maskClaw, None, iterations = 2)
		maskClaw = cv2.dilate(maskClaw, None, iterations = 2)	
		
		#update clawX,Y with new or same coordinates
		if (maskClaw is not None):
			getCenter(maskClaw)
			#print "clawX: ", clawX,  "clawY: ", clawY
		

		# find contours of skittle from threshold
		contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		

		# Image Algorithm
		# filter all objects detected by size, and circularity 
		for c in contours:
			
			# only big enough size as valid
			if cv2.contourArea(c) > skittlePixelSize:
			    # bound rectangle, w & h should be approx 1
			    
			    x,y,w,h = cv2.boundingRect(c)
			    ratio = float(w)/h
			    #print "ratio: " ,ratio
			    if( ratio > 0.25 and ratio < 2):

					#print "size is: " , cv2.contourArea(c)
					
					#get center
					M = cv2.moments(c)
					cX = int(M["m10"]/M["m00"])
					cY = int(M["m01"]/M["m00"])
					
					#print "X: " ,cX, "Y: ", cY
					
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
# return center (x,y) from Mat input 
#==================================
def getCenter( maskedFrame ):
	
	global clawX, clawY
	
	contours = cv2.findContours(maskedFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	
	#only update clawX,Y if 2 green spots detected
	if (len(contours) >= 2):
		
		#temp var to recalculate
		X = 0
		Y = 0
		
		for c in contours:	
			# only big enough size as valid
			#
			if cv2.contourArea(c) > clawGreenPixelSize:
				# bound rectangle, w & h should be approx 1
				
				x,y,w,h = cv2.boundingRect(c)
				ratio = float(w)/h
				#print "ratio: " ,ratio
				if( ratio > 0.8 and ratio < 1.2):

					#print "size is: " , cv2.contourArea(c)
					
					#recalculate  center 
					M = cv2.moments(c)
					X += int(M["m10"]/M["m00"])
					Y += int(M["m01"]/M["m00"])	
					
		#get average for middle		
		newClawX = X/2
		newClawY = Y/2
		
		#compare with global value and update only if similar, else return same
		if( ( abs(newClawX-clawX) + abs(newClawY-clawY) )  < 1000 ): #unused now
			clawX =  newClawX
			clawY =  newClawY
			
		else:
			pass
		
	else:
		print "no claw detected"


#==================================
# get input from keyboard
#==================================
def getColorInput():
	global colorInput, colorLB, colorUB, greenLB, greenUB
	
	#CLAW value
	greenLB = (50,100,0)
	greenUB = (100,255,140)
	
	yellowLB = (10,50,100)
	yellowUB = (80,230,230)
	
	redLB = (169,136,103)
	redUB = (179,225,206)

	
	print "Color Choices: [g,r,y ]"
	
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
		
	if(colorInput == 'y'):
		print "looking for YELLOW skittles"
		#set threshold range for yellow
		colorLB = yellowLB
		colorUB = yellowUB
		colorInput = 'y'
		


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
	
	global state, redSkittleList, yellowSkittleList, tempRedSkittleList, tempRedIncrement, medianPositions
	global deltaX, deltaY
	global clawX, clawY
	
	#=======IDLE========#
	if state == 'IDLE':
		print "IDLE"
		
		# Send arm to the home posistion
		arm.home(serial)
		time.sleep(1)
		
		#get valid input to move to INIT, else stay in IDLE
		getColorInput()
		
		#valid
		if ( (colorInput is 'g') or (colorInput is 'r') or (colorInput is 'y')):
			state = 'INIT'
		#invalid
		else:
			state = 'IDLE'
			
	#=======INIT========#	
	elif state == 'INIT':
		print "INIT"
		
		if ( (colorInput is 'r') ):
			redSkittleList = imageProcess()
			#printSkittleList(redSkittleList)
			
			
			if(len(redSkittleList) != 0):
				print "detected: ", len(redSkittleList), " red skittle"
				
				printSkittleList(redSkittleList)
				state = 'DETECT'
			
			else:
				print "detected: 0 red skittle"
				state = 'IDLE'
		
		if ( (colorInput is 'y') ):
			yellowSkittleList = imageProcess()
		
			
			if(len(yellowSkittleList) != 0):
				print "detected: ", len(yellowSkittleList), " yellow skittle"
				
				printSkittleList(yellowSkittleList)
				state = 'DETECT'
			
			else:
				print "detected: 0 yellow skittle"
				state = 'IDLE'

		if ( (colorInput is 'g') ):
			greenkittleList = imageProcess()
			#printSkittleList(redSkittleList)
			

	#=======DETECT========#	
	elif state == 'DETECT':
		#print "DETECT"
		
		tempSkittleList = imageProcess()
	
		#store history of previous positions of detected red skittle
		for i in range (len(tempSkittleList)):
			tempRedSkittleListPos[i][tempRedIncrement % 5] = tempSkittleList[i].getPosition()
			
			#print "temp Pos" , tempRedSkittleListPos[i][tempRedIncrement % 5]	
			#print "temp list" , tempRedSkittleListPos[i] 
			
			#sort to choose the median value
			medianPositions[i] = sorted(tempRedSkittleListPos[i])[2]
			#print "filtered val: " , medianPositions[i] 
			
		#update for next frame
		tempRedIncrement += 1	
		
		## calculate deltaX,Y from 1st object detected (whichever has lowest y or closest to the arm in y)
		
		##dynamic: median filter skittle during run-time
		#moveToPos = medianPositions[0]  
		#print "skittle at: ", moveToPos
		
		if(  (colorInput is 'r') ):
			#static: no median filter, just on first capture
			moveToPos = redSkittleList[0].getPosition()
			#print "skittle at: ", moveToPos[0], moveToPos[1]
		
		elif(  (colorInput is 'y') ):
			#static: no median filter, just on first capture
			moveToPos = yellowSkittleList[0].getPosition()
			#print "skittle at: ", moveToPos[0], moveToPos[1]
			
		
		deltaX = int(moveToPos[0]) - int(clawX)  
		deltaY = int(clawY) - int(moveToPos[1])
		
		distanceClaw2Obj = int(math.sqrt(deltaX*deltaX + deltaY*deltaY))
		
		print "State: %s | deltaX: %d | deltaY: %d | distance: %d" % (state, deltaX, deltaY, distanceClaw2Obj) 
		#print "abs dist: ", distanceClaw2Obj
		
		#determine next state to keep closing in on target
		if ( distanceClaw2Obj < close2Object): 
			print "claw arrived at skittle"
			state = 'MOVEOBJ'
			
		else:
			state = 'MOVETO'
		
			
		
	
	#=======MOVETO========#	
	elif state == 'MOVETO':
		#print "MOVETO"
		
		#print "deltaX: %d deltaY: %d" % (deltaX, deltaY) 
		if(deltaX > 0 and deltaY > 0):
			print "State: %s | command: move rightup" % (state) 
			#print "move rightup"
			arm.stepX(serial, 3)
			arm.stepY(serial, 3)
			
		elif(deltaX > 0 and deltaY < 0):
			print "State: %s | command: move rightdown" % (state) 
			#print "move rightdown"
			arm.stepX(serial, 3)
			arm.stepY(serial, -3)
			
		elif(deltaX < 0 and deltaY > 0):
			print "State: %s | command: move leftup" % (state) 
			#print "move leftup"
			arm.stepX(serial, -3)
			arm.stepY(serial, 3)
			
		elif(deltaX < 0 and deltaY < 0):
			print "State: %s | command: move leftdown" % (state) 
			#print "move leftdown"
			arm.stepX(serial, -3)
			arm.stepY(serial, -3)
		
		else: print " delta is 0"
			
		#always return to detect state after incremental movement
		state = 'DETECT'


	#=======MOVEOBJ========#	
	elif state == 'MOVEOBJ':
		print "MOVEOBJ"
		
		print "GRABBING SKITTLE!"
		#increase radius for better grasp
		arm.stepR(serial, 5)
		sleep(1)
		#move down z
		arm.setZ(serial, -25)
		sleep(1)
		#close claw
		arm.setC(serial, 0)
		sleep(1)
		#move up z
		arm.setZ(serial, 0)
		sleep(1)
		
		#move to home
		arm.setZ(serial, 30)
		arm.setR(serial, 80)
		arm.setTheta(serial, 90)
		sleep(1)
		
		#move to sort basket
		if( (colorInput is 'r') ):
			arm.setTheta(serial, 15)
			sleep(1)
		elif( (colorInput is 'y') ):
			arm.setTheta(serial, 190)
			sleep(1)
				
		#open claw
		arm.setC(serial, 50)
		sleep(1)
		
		#move to home
		arm.setZ(serial, 30)
		arm.setR(serial, 75)
		arm.setTheta(serial, 90)
		sleep(1)
		
		#reset values to recalculate 
		tempRedSkittleListPos[0] = [(0,0), (0,0), (0,0),(0,0),(0,0)]
		clawX = 290
		clawY = 360
		state = 'IDLE'
		


		
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





