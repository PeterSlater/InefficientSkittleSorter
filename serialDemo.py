import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)

while 1 :
	try:
		ser.write('v 140.0\n')
		time.sleep(0.1)
		temp = ser.readline();
		print temp
		
		vals = []
		
		for t in temp.split():
			try:
				vals.append(float(t))
			except ValueError:
				pass
		
		print vals
		
		print 'end'
		time.sleep(1)
	except:
		pass
	time.sleep(1)

ser.close();

