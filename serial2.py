import serial

neck = serial.Serial('/dev/ttyUSB0', 9600)
neck.write(b's')
neck.write(b's')
neck.write(b's')
