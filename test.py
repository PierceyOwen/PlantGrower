import serial
import RPi.GPIO as GPIO
import time

ser = serial.Serial('/dev/ttyACM0',9600)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
    
while True:
    
	if ser.in_waiting > 0:
		rawserial = ser.readline()
		cookedserial = rawserial.decode('utf-8').strip('\r\n')
		datasplit = cookedserial.split(',')
		temperature = datasplit[0].strip('<')
		humidity = datasplit[1].strip('>')
		print(temperature)
		print(humidity)
		ser.write(str.encode(str(temperature) + str(humidity)))
		GPIO.output(7, GPIO.HIGH)
		time.sleep(2)
