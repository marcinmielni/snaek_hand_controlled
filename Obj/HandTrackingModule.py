import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode = False, maxHands = 2,complexity = 1, minDetConfidence = 0.5, minTrackConfidence = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.minDetConfidence = minDetConfidence
        self.minTrackConfidence = minTrackConfidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.minDetConfidence,self.minTrackConfidence)
        self.mpDraw = mp.solutions.drawing_utils
    
    def findHands(self, img, draw = True):
        imgRBG = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRBG)
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = True):                       #find each landmarks position on screen(pixels)
        lmList = []
        if self.results.multi_hand_landmarks:
            targetHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(targetHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int( lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)
        return lmList

    def line(self, img, lmList, startId, endId, draw = True):
        if lmList:
            start = lmList[startId]
            end = lmList[endId]
            if draw:
                cv2.line(img, start[1:], end[1:], (0, 255, 0), 3)
            return (start[1] - end[1], start[2] - end[2])
        else:
            return (0, 0)

   

def main():                                                                             #exaple usage of this module
    cap = cv2.VideoCapture(0)               #defining capture src

    pTime = 0                               #time used to display framerate (fps)
    cTime = 0
    detector = handDetector(False, 1)

    while True:
            success, img = cap.read()
            
            img = detector.findHands(img, False)
            lmList = detector.findPosition(img, 0 , False)
            print(detector.line(img, lmList, 5, 8))

            cTime = time.time()                                                             #calculating fps
            fps = 1/(cTime - pTime)
            pTime = cTime

            img = cv2.flip(img, 3)
            cv2.putText(img, str(int(fps)),(10,30), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 0), 2)
            cv2.imshow("Image", img)
            cv2.waitKey(1)


if __name__ == "__main__":
    main()