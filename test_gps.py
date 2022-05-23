import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 115200)
W_buff = ["AT+CGNSPWR=1\r\n", "AT+CGNSSEQ=\"RMC\"\r\n", "AT+CGNSINF\r\n", "AT+CGNSURC=2\r\n", "AT+CGNSTST=1\r\n"]
ser.write(W_buff[0].encode())
ser.flushInput()
data=""
num=0
try:
    while True:
        while ser.inWaiting() > 0:
            data += ser.read(ser.inWaiting())
        if(data != ""):
            print(data)
            time.sleep(0.5)
            ser.write(W_buff[num+1].encode())
            num = num + 1
            if(num == 4):
                time.sleep(0.5)
                ser.write(W_buff[4].encode())
            data = ""
            
except KeyboardInterrupt:
    if(ser != None):
        ser.close()