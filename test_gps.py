import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 115200)
# AT+CGPSPWR=1 ---- Open GPS
# At+CGPSSTATUS ---- Read GPS fix status
# AT+CGPSINF=0 ---- Get the current gps location info: mode, latitude, longitude, UTC time, TIFF, num, speed, course
# AT+CGPSOUT=32 ---- Read NMEA $GPRMC data
# AT+CGPSRST=0 ---- Reset GPS in Cold start mode
# AT+CGPSRST=1 ---- Reset GPS in Hot start mode
#W_buff = ["AT+CGNSPWR=1\r\n", "AT+CGNSSEQ=\"RMC\"\r\n", "AT+CGNSINF\r\n", "AT+CGNSURC=2\r\n", "AT+CGNSTST=1\r\n"]
W_buff = ["AT+CGPSPWR=1\r\n", "AT+CGPSRST=0\r\n", "At+CGPSSTATUS\r\n", "At+CGPSSTATUS\r\n", "AT+CGPSINF=0\r\n", "AT+CGPSOUT=32\r\n"]
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
            if(num == 5):
                time.sleep(0.5)
                ser.write(W_buff[4].encode())
                num = 0
            data = ""
            
except KeyboardInterrupt:
    if(ser != None):
        ser.close()