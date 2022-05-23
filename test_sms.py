import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 115200)
ser.write("AT\r\n")
ser.write("AT+CMGF=1\r\n")
ser.write("AT+CSCA=\"+8613800755500\"\r\n")
ser.write("AT+CMGS=\"+50765883374\"\r\n")
ser.write("HELLO WORLD")
ser.flushInput()