import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 115200)

W_buff = ["AT\r\n", "AT+CMGF=1\r\n", "AT+CSCA=\"+507\"\r\n", "AT+CMGS=\"65883374\"\r\n", "HELLO WORLD"]
ser.write(W_buff[0].encode())
ser.flushInput()
data=""
num=0
try:
    while True:
        while ser.inWaiting() > 0:
            data += ser.read(ser.inWaiting()).decode()
        if(data != ""):
            print(data)
            time.sleep(0.5)
            ser.write(W_buff[num+1].encode())
            num = num + 1
            if(num == 3):
                time.sleep(0.5)
            if(num == 4):
                time.sleep(0.5)
                ser.write(W_buff[4].encode())
                num = 0
            data = ""
            
except KeyboardInterrupt:
    if(ser != None):
        ser.close()