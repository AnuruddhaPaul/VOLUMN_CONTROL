import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode)
        self.mpDraw=mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) # hands only use RGB img
        self.results=self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame,handLms,self.mpHands.HAND_CONNECTIONS) #
                    
        return frame

    def findPosition(self, frame, handNo=0, draw=True):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
            
                h, w, c = frame.shape # we are getting a decimal value so we are
                # convert the decimal to Pixcel by multiplying the width and height 
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),15,(255,0,255),cv2.FILLED)

        return lmList
                
                
            
             #

   




def main():
    pTime=0
    cTime=0
    url = 'http://10.5.126.236:8080/video'  

# Open the video stream
    cap = cv2.VideoCapture(0)
    dectector=handDetector()
    while True:
        _, frame = cap.read()
        frame=dectector.findHands(frame)
        lmList=dectector.findPosition(frame)
        if len(lmList)!=0:
            print(lmList[4])
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()