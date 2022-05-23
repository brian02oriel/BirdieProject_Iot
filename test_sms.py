import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 115200)
ser.write("AT\r\n".encode())
ser.flushInput()
ser.write("AT+CMGF=1\r\n".encode())
ser.flushInput()
ser.write("AT+CSCA=\"+8613800755500\"\r\n".encode())
ser.flushInput()
ser.write("AT+CMGS=\"+50765883374\"\r\n".encode())
ser.flushInput()
ser.write("HELLO WORLD".encode())
ser.flushInput()
time.sleep(0.5)