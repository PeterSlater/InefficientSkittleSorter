# meArm.py - York Hack Space May 2014
# A motion control library for Phenoptix meArm using Adafruit 16-channel PWM servo driver

import Adafruit_PWM_Servo_Driver
from Adafruit_PWM_Servo_Driver import PWM
import kinematics
import time
from math import pi

##TEST SERVO BASE
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwmB = GPIO.PWM(18, 50)
pwmB.start(7.5)

##TEST SERVO Shoulder
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
pwmS = GPIO.PWM(12, 50)
pwmS.start(7.5)


##TEST SERVO Elbow
GPIO.setup(23, GPIO.OUT)
pwmE = GPIO.PWM(23, 50)
pwmE.start(7.5)

basePWM = 0 
shoulderPWM = 0
elbowPWM = 0
    	
class meArm():
    def __init__(self, sweepMinBase = 145, sweepMaxBase = 49, angleMinBase = -pi/4, angleMaxBase = pi/4,
    			 sweepMinShoulder = 118, sweepMaxShoulder = 22, angleMinShoulder = pi/4, angleMaxShoulder = 3*pi/4,
    			 sweepMinElbow = 144, sweepMaxElbow = 36, angleMinElbow = pi/4, angleMaxElbow = -pi/4,
    			 sweepMinGripper = 75, sweepMaxGripper = 115, angleMinGripper = pi/2, angleMaxGripper = 0):
        """Constructor for meArm - can use as default arm=meArm(), or supply calibration data for servos."""
    	self.servoInfo = {}
    	self.servoInfo["base"] = self.setupServo(sweepMinBase, sweepMaxBase, angleMinBase, angleMaxBase)
    	self.servoInfo["shoulder"] = self.setupServo(sweepMinShoulder, sweepMaxShoulder, angleMinShoulder, angleMaxShoulder)
    	self.servoInfo["elbow"] = self.setupServo(sweepMinElbow, sweepMaxElbow, angleMinElbow, angleMaxElbow)
    	self.servoInfo["gripper"] = self.setupServo(sweepMinGripper, sweepMaxGripper, angleMinGripper, angleMaxGripper)
    	
    # Adafruit servo driver has four 'blocks' of four servo connectors, 0, 1, 2 or 3.
    def begin(self, block = 0, address = 0x40):
        """Call begin() before any other meArm calls.  Optional parameters to select a different block of servo connectors or different I2C address."""
        self.pwm = PWM(address) # Address of Adafruit PWM servo driver
    	self.base = block * 4
    	self.shoulder = block * 4 + 1
    	self.elbow = block * 4 + 2
    	self.gripper = block * 4 + 3
    	self.pwm.setPWMFreq(60)
    	self.openGripper()
    	self.goDirectlyTo(0, 100, 50)
    	
    def setupServo(self, n_min, n_max, a_min, a_max):
        """Calculate servo calibration record to place in self.servoInfo"""
    	rec = {}
    	n_range = n_max - n_min
    	a_range = a_max - a_min
    	if a_range == 0: return
    	gain = n_range / a_range
    	zero = n_min - gain * a_min
    	rec["gain"] = gain
    	rec["zero"] = zero
    	rec["min"] = n_min
    	rec["max"] = n_max
    	return rec
    
    def angle2pwm(self, servo, angle):
        """Work out pulse length to use to achieve a given requested angle taking into account stored calibration data"""
        #Base rad [-1.09, 1.09] to mSec [1,2]
        #OldRange = (OldMax - OldMin)
        #NewRange = (NewMax - NewMin)
        #NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    	
    	global basePWM, shoulderPWM, elbowPWM
    	
    	if( servo == "base"):
	    	baseRadMin = -1.09
	    	baseRadMax = 1.09
	    	baseRadRange = baseRadMax - baseRadMin
	    	basePWMmin = 2.5
	    	basePWMmax = 10.0
	    	basePWMrange = basePWMmax - basePWMmin
	    	
	    	basePWM = (( ( angle-baseRadMin )* basePWMrange)/ baseRadRange) + basePWMmin
	    	print "basePWM: ",  basePWM
	    	
	    	pwmB.ChangeDutyCycle(basePWM)
	    	
    	if( servo == "shoulder"):
	    	shoulderRadMin = 3.5
	    	shoulderRadMax = 0.57
	    	shoulderRadRange = shoulderRadMax - shoulderRadMin
	    	shoulderPWMmin = 7.0
	    	shoulderPWMmax = 11.0
	    	shoulderPWMrange = shoulderPWMmax - shoulderPWMmin
	    	
	    	shoulderPWM = (( ( angle-shoulderRadMin )* shoulderPWMrange)/ shoulderRadRange) + shoulderPWMmin
	    	print "shoulderPWM: ",  shoulderPWM
	    	
	    	pwmS.ChangeDutyCycle(shoulderPWM)
    	
    	ret = basePWM
    	
    	if( servo == "elbow"):
	    	elbowRadMin = 1.35
	    	elbowRadMax = -0.19
	    	elbowRadRange = elbowRadMax - elbowRadMin
	    	elbowPWMmin = 5.5
	    	elbowPWMmax = 8.0
	    	elbowPWMrange = elbowPWMmax - elbowPWMmin
	    	
	    	elbowPWM = (( ( angle-elbowRadMin )* elbowPWMrange)/ elbowRadRange) + elbowPWMmin
	    	print "elbowPWM: ",  elbowPWM
	    	
	    	pwmE.ChangeDutyCycle(elbowPWM)
    	
    	ret = basePWM
    	
    	return ret
    	
    def goDirectlyTo(self, x, y, z):
        """Set servo angles so as to place the gripper at a given Cartesian point as quickly as possible, without caring what path it takes to get there"""
    	angles = [0,0,0]
    	if kinematics.solve(x, y, z, angles):
    		radBase = angles[0]
    		radShoulder = angles[1]
    		radElbow = angles[2]
    		
    		 
    		self.pwm.setPWM(self.base, 0, self.angle2pwm("base", radBase))
    		self.pwm.setPWM(self.shoulder, 0, self.angle2pwm("shoulder", radShoulder))
    		self.pwm.setPWM(self.elbow, 0, self.angle2pwm("elbow", radElbow))
    		self.x = x
    		self.y = y
    		self.z = z
    		print "goto %s, radians %s" % ([x,y,z], [radBase, radShoulder, radElbow])
    		time.sleep(3)
    		
    def gotoPoint(self, x, y, z):
        """Travel in a straight line from current position to a requested position"""
    	x0 = self.x
    	y0 = self.y
    	z0 = self.z
    	dist = kinematics.distance(x0, y0, z0, x, y, z)
    	step = 10
    	i = 0
    	while i < dist:
    		self.goDirectlyTo(x0 + (x - x0) * i / dist, y0 + (y - y0) * i / dist, z0 + (z - z0) * i / dist)
    		time.sleep(0.05)
    		i += step
    	self.goDirectlyTo(x, y, z)
    	time.sleep(3)
    	
    def openGripper(self):
        """Open the gripper, dropping whatever is being carried"""
    	self.pwm.setPWM(self.gripper, 0, self.angle2pwm("gripper", pi/4.0))
    	time.sleep(0.3)
    	
    def closeGripper(self):
        """Close the gripper, grabbing onto anything that might be there"""
    	self.pwm.setPWM(self.gripper, 0, self.angle2pwm("gripper", -pi/4.0))
    	time.sleep(0.3)
    
    def isReachable(self, x, y, z):
        """Returns True if the point is (theoretically) reachable by the gripper"""
    	radBase = 0
    	radShoulder = 0
    	radElbow = 0
    	return kinematics.solve(x, y, z, radBase, radShoulder, radElbow)
    
    def getPos(self):
        """Returns the current position of the gripper"""
    	return [self.x, self.y, self.z]
