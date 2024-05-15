import math
import cv2
import socket
import pickle
import struct
import supervision as sv
import numpy as np
import threading
import time

from controller import MouseHandler
import captureMouse

mouseHandler = MouseHandler('COM3', 38400, mouseConsole=True)

'''console_thread = threading.Thread(target=MouseHandler.mouseConsole)
console_thread.daemon = True  # Set daemon to True to allow the thread to exit when the main program exits
console_thread.start()'''

captureMouse.captureMouse(mouseHandler)

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.254.143', 8080))  # Connect to the server's IP address and port

modelNames = ["body", "head"]
HEAD = modelNames.index("head")

box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=1, text_scale=0.5)
SIZE = (640,480)
SCREEN_CENTER = (SIZE[0]//2, SIZE[1]//2)

def euclidean_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def aimbot(detections):
    #objects = []
    closest = None
    closestDistance = 9999999
    for i, box in enumerate(detections.xyxy):
        if detections.class_id[i] == HEAD:
            centerX = round((box[0] + box[2])/2)
            centerY = round((box[1] + box[3])/2)
            center = (centerX, centerY)
            distance = euclidean_distance(center, SCREEN_CENTER)
            if distance < closestDistance:
                closestDistance = distance
                closest = center
        
    if closest != None:
        '''note: controller considers +/- X to be Right/Left,  and +/- Y to be Up/Down. YOLOv8 considers +/- Y to be Down/Up, since the origin is top left.'''
        print("Chose", closest, "  from", detections.xyxy)
        
        # say if closest x is 0, and screen center is 320, then we want mouse to go left. 
        # in this operation, our xDiff would be -320, so it will move towards positive x (good).
        xDiff = closest[0] - SCREEN_CENTER[0]
        # if closest y is 0, and center is 240, then we want mouse to go up.
        # in this setup, then yDiff is 240, and it will move towards positive y (good, matches controller).
        yDiff = SCREEN_CENTER[1] - closest[1]

        click = False
        if abs(xDiff) < 5 and abs(yDiff) < 5:
            click = True

        mouseHandler.mouse(xDiff//4, yDiff//4, click, False, False)



    #print(detections)
    #print("----------------")
    #print(detections.xyxy)

    #print(detections)

frameTimes = []
while True:
    try:
        # Receive frame size
        data_size = client_socket.recv(4)
        if not data_size:
            break
        # Unpack frame size
        size = struct.unpack(">L", data_size)[0]
        # Receive frame data
        data = b""
        while len(data) < size:
            packet = client_socket.recv(size - len(data))
            if not packet:
                break
            data += packet

        # Deserialize the data
        #z = pickle.loads(data)
        #print(z)
        
        #frame = z
        (encodedFrame, detections) = pickle.loads(data)
        #decoded_frame = cv2.imdecode(np.frombuffer(encoded_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        decodedFrame = cv2.imdecode(encodedFrame, cv2.IMREAD_COLOR)


        aimbot(detections)

        labels = [f"{modelNames[detections.class_id[i]]} {detections.confidence[i]:0.2f}" for i in range(len(detections.class_id))]

        decodedFrame = box_annotator.annotate(scene=decodedFrame, detections=detections, labels=labels)

        # Display the frame
        cv2.imshow('Received Frame', decodedFrame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frameTimes.append(time.time())
        while time.time() - frameTimes[0] >= 10:    
            frameTimes.pop(0)

        print("FPS =", len(frameTimes) / 10)
    except KeyboardInterrupt as e:
        print(f"Error: {e}")
        break

#cv2.destroyAllWindows()
client_socket.close()
