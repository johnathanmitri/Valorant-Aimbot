import serial, os, struct

# Initialize serial communication
ser = serial.Serial('COM3', 9600)  # Replace 'COM1' with your serial port name

def read_serial():
    while True:
        if ser.in_waiting > 0:
            received_text = ser.readline().decode().strip()
            print("Received:", received_text)

def write_integer(value):
    data = struct.pack('<i', value)
    # Write the binary string to the serial port
    ser.write(data)

def mouse(dx, dy, m1, m2, m3):
    buttonBitField = 0
    buttonBitField |= m1
    buttonBitField |= (m2 << 1)
    buttonBitField |= (m3 << 2)
    
    data = struct.pack('<iiB', dx, dy, buttonBitField)
    ser.write(data)


    #ser.write(value.to_bytes(4, 'little'))  # Write integer as 4 bytes in little-endian format

# Start a thread to continuously read from serial
# You can modify this part according to your application's requirement
import threading
read_thread = threading.Thread(target=read_serial)
read_thread.daemon = True
read_thread.start()


m1 = False

while True:
    line = input()
    if line == "m1":
        m1 = not m1
        mouse(0,0,m1,0,0)
    else:
        l = line.split()
        mouse(int(l[0]), int(l[1]), m1, 0, 0)

    #line = input().split()
    ##print("LINE IS : ", line)
#
    #for item in line:
    #    write_integer(int(item))
    
