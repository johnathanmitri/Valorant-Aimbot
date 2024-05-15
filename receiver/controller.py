import serial, os, struct,  time
import threading

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class MouseHandler:
    def __init__(self, port, baudrate, mouseConsole = False):
       self.initialized = False
       self.port, self.baudrate = port, baudrate
       self.dx, self.dy = 0, 0
       self.buttons = [False, False, False]
       if mouseConsole: 
            self.console_thread = threading.Thread(target=self.mouseConsole)
            self.console_thread.daemon = True
            self.console_thread.start()
       self.start()

    def addMovement(self, dx, dy):
        if abs(dx) > 1000 or abs(dy) > 1000:
            return
        self.dx += dx
        self.dy += dy

    def start(self):
        self.stopFlag = False
        self.ser = serial.Serial(self.port, self.baudrate)
        self.read_thread = threading.Thread(target=self.readLoop)
        self.read_thread.daemon = True
        self.read_thread.start()
        self.write_thread = threading.Thread(target=self.writeLoop)
        self.write_thread.daemon = True
        self.write_thread.start()
        print("Mouse Handler running...")

    def stop(self):
        #nonlocal stopFlag
        self.stopFlag = True
        time.sleep(0.05)
        self.ser.close()
        self.start()

    def btnDown(self, btn):
        self.buttons[btn] = True

    def btnUp(self, btn):
        self.buttons[btn] = False

    def writeLoop(self):
        while not self.stopFlag:
            if self.initialized:
                resDx, resDy = self.mouse(self.dx, self.dy, self.buttons[0], self.buttons[1], self.buttons[2])
                self.dx-=resDx
                self.dy-=resDy
            time.sleep(0.010)

    def readLoop(self):
        while not self.stopFlag:
            if self.ser.in_waiting > 0:
                received_text = self.ser.readline().decode().strip()
                print("Received:", received_text)
            time.sleep(0.005)

    def write_integer(self, value):
        data = struct.pack('<i', value)
        # Write the binary string to the serial port
        self.ser.write(data)

    def mouse(self, dx, dy, m1, m2, m3):
        lim = 150
        if abs(dx) > lim or abs(dy) > lim:   # TDDO: MAKE THIS A RANDOMIZED MAXIMUM !! LET IT BE 19 SOMETIMES, OTHER TIMES 23, ETC...
            print("DX OR DY BIGGER THAN " + str(lim) + ": ", (dx, dy))
            dx = clamp(dx, -lim, lim)
            dy = clamp(dy, -lim, lim)

        buttonBitField = 0
        buttonBitField |= m1
        buttonBitField |= (m2 << 1)
        buttonBitField |= (m3 << 2)
        
        data = struct.pack('<iiB', dx, dy, buttonBitField)
        self.ser.write(data)
        return dx, dy

    def mouseConsole(self):
        m1 = False
        while True:
            line = input()
            if line == "m1":
                m1 = not m1
                self.mouse(0,0,m1,0,0)
            elif line == "init":
                self.initialized = True
                self.dx = self.dy = 0
                print("initialized = true")
            else:
                l = line.split()
                self.mouse(int(l[0]), int(l[1]), m1, 0, 0)

if __name__ == "__main__":
    mouseHandler = MouseHandler('COM3', 38400, True)

    while (True):
        time.sleep(1)

    
#
    #line = input().split()
    ##print("LINE IS : ", line)
#
    #for item in line:
    #    write_integer(int(item))
    
