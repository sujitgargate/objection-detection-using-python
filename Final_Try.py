import cv2
import numpy as np
import serial
serialout= serial.Serial('com3',9600)
cap = cv2.VideoCapture(1)



def process():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = gray.astype('uint8')
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,5,0.0009)
    dst = cv2.dilate(dst,None)
    
    ################################################
    frame[dst>0.01*dst.max()]=[255,255,0]
    
    
    ###############################################
    ret1, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
    dst = np.uint8(dst)

    ###############################################
    
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
    cv2.imshow('1', frame)
    if len(corners) < 25:
        #val=0  #rotate 180
        #sleep(1)
        print(len(corners))
        serialout.write(b'0')
        print(0)

        
    else :
        #val=1   #rotate 180
        #sleep(1)
        print(len(corners))
        serialout.write(b'1')
        print(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        serialout.close()
        cap.release()
        cv2.destroyAllWindows()       
        
        
#while cv2.waitKey(1):
while True:
    mydata=serialout.readline()
    #mydata=(int(int(mydata)))
    mydata=np.int(mydata)
    if mydata<700:
        process()
        