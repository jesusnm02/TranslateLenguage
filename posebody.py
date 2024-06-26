import cv2
import mediapipe as mp
import math
class poseDtetector():

    def __init__(self, mode=False, upperBody=False, smooth=True, enableseg=False,
                 smoothseg=True, minde=0.5, mintrack=0.5):

        self.mode=mode
        self.upperBody=upperBody
        self.smooth=smooth
        self.enableseg=enableseg
        self.smoothseg=smoothseg
        self.minde=minde
        self.mintrack=mintrack

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upperBody,self.smooth,self.enableseg,
                                     self.smoothseg,self.minde, self.mintrack)

    def findPose(self,img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if draw:
            if self.results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img
    def getPosicition(self, img, draw=True):
        self.lmlist=[]
        if self.results.pose_landmarks:
         for id, lm in enumerate(self.results.pose_landmarks.landmark):
            h, w, c=img.shape

            cx, cy=int(lm.x*w), int(lm.y*h)
            self.lmlist.append([id,cx,cy])
            if draw:
               cv2.circle(img, (cx,cy), 6,(255,0,0),cv2.FILLED)
        return self.lmlist

    def findAngle(self,img,p1,p2,p3, draw=True):
        #get the landmarks
        x1,y1=self.lmlist[p1][1:]
        x2,y2 = self.lmlist[p2][1:]
        x3,y3 = self.lmlist[p3][1:]
        #calculate the angle
        angle=math.degrees(math.atan2(y3-y2,x3-x2)-
        math.atan2(y1-y2,x1-x2))

        if angle<0:
            angle+=360

        #draw
        if draw:
            cv2.line(img, (x1,y1),(x2,y2),(255,255,255),3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)

            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)),(x2-50,y2+50),
                        cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
        return angle