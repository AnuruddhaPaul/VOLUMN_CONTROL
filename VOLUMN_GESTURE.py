import cv2
import mediapipe as mp
import time
import numpy as np
import HAND_TRAKING_MODULE as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
cap=cv2.VideoCapture(0)
pTime=0
width ,height=1000,1000
cap.set(3,width)
cap.set(4,height)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
minvol,maxvol,_=volume.GetVolumeRange()

detector=htm.handDetector()
while True:
    _,frame=cap.read()
    frame=detector.findHands(frame)
    lmList=detector.findPosition(frame,draw=False)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),3)
        length=math.hypot(x2-x1,y2-y1)
        #print(length)
        #hand range 50-300 volrange -65.25-0
        cv2.circle(frame,(x1,y1),15,(0,255,0),cv2.FILLED)
        cv2.circle(frame,(x2,y2),15,(0,255,0),cv2.FILLED)
        vol=np.interp(length,[50,300],[minvol,maxvol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break