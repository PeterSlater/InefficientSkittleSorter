import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

while 1 :
	ser.write('r 140.0\n')

ser.close();

