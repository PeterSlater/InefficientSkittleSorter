import serial
import time

# How long it takes to send a command
DELAY = 0.05

# Initialize the serial port for the arm
def init():
	return serial.Serial('/dev/ttyACM0', 9600, timeout=0)

# Move the arm to the home posistion
def home(ser):
	setZ(ser, 0)
	setR(ser, 75)
	setTheta(ser, 90)
	
# Close the serial port
def close(ser):
	ser.close()

# Set the theta coordinate 
def setTheta(ser, theta):
	ser.write('o ' + str(theta) + '\n')
	
	time.sleep(DELAY)

# Set the R coordinate
def setR(ser, r):
	ser.write('r ' + str(r) + '\n')
	time.sleep(DELAY)

# Set the Z coordinate
def setZ(ser, z):
	ser.write('z ' + str(z) + '\n')
	time.sleep(DELAY)
	
# Set the C coordinate
def setC(ser, c):
	ser.write('c ' + str(c) + '\n')
	time.sleep(DELAY)

# Set the X coordinate
def setX(ser, x):
	ser.write('x ' + str(x) + '\n')
	time.sleep(DELAY)

# Set the Y coordinate
def setY(ser, y):
	ser.write('y ' + str(y) + '\n')
	time.sleep(DELAY)

# Step the X coordinate
def stepX(ser, w):
	ser.write('w ' + str(w) + '\n')
	time.sleep(DELAY)

# Step the Y coordinate
def stepY(ser, h):
	ser.write('h ' + str(h) + '\n')
	time.sleep(DELAY)

# Read the current posistion of the arm
def posistion(ser, timeout):
	start = time.time()
	
	# send the command and wait for a response
	ser.write('v 0.0\n')
	
	while True:
		time.sleep(0.1)
		temp = ser.readline();
		
		# parse the float values
		vals = []	
		for t in temp.split():
			try:
				vals.append(float(t))
			except ValueError:
				pass
		
		# exit if read is correct
		if (len(vals) == 6):
			return vals
		
		# timeout if something went wrong
		if (time.time() - start > timeout):
			break
