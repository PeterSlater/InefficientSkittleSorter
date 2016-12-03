import mearm.control as arm
import atexit
import time

# Create the arm serial port
ser = arm.init()

# Send arm to the home posistion
arm.home(ser)
time.sleep(3)

# Always close the serial port on exit
def close():
	arm.close(ser)
atexit.register(close)

# Go through some moves and give arm time to comply
arm.setTheta(ser, 0)
time.sleep(1)
arm.setR(ser, 100)
time.sleep(1)
arm.setZ(ser, -30)
time.sleep(1)
arm.setC(ser, 0)
time.sleep(1)
arm.setZ(ser, 0)
time.sleep(1)
arm.setY(ser, 75)
arm.setX(ser, 0)
time.sleep(1)

while True:
	pos = arm.posistion(ser, 2)
	print pos
	
	arm.stepY(ser, 3)
	arm.stepX(ser, 3)
	
	if(pos[5] == 129.0):
		arm.setC(ser, 50)
		arm.home(ser)
		exit(0)
