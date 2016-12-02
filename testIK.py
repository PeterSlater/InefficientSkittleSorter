#test IK service with servo
import RPi.GPIO as GPIO
import time

import kinematics

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 50)
pwm.start(7.5)




print "moving servo M, L, R"
while(1):
	
	pwm.ChangeDutyCycle(7.5)
	time.sleep(1)
	pwm.ChangeDutyCycle(12.5)
	time.sleep(1)
	pwm.ChangeDutyCycle(2.5)
	time.sleep(1)


