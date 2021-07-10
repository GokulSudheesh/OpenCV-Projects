import cv2
import pyautogui as pag
#make sure you are atleast 3 feet away from the screen
palm_cascade = cv2.CascadeClassifier('dataXML/palm.xml')
fist_cascade = cv2.CascadeClassifier('dataXML/fist.xml')
#Change the following to whatever you are confortable with (Fist/Palm) while calling the function
#Coordinates for the Region of Interest
global init_x1, init_x2, init_y1, init_y2
init_x1 = 280
init_y1 =200
init_x2 = init_x1 + 475
init_y2 = init_y1 + 335
sF = 1.2 #ScaleFactor (Keep it at 1.2)
neighbour = 5 #Minimum Neighbours (Keep it at 5)
cap = cv2.VideoCapture(0)
cap.set(3, 1040)
cap.set(4, 720)
#BGR
colors = {"white": (255, 255, 255), "red": (0, 0, 255), "green": (0, 255, 0)}
def display_text(frame, mssg, x, y, color):
    cv2.putText(frame, mssg, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, colors[color], 2, cv2.LINE_AA)
def startGesture(cascade):
    global init_x1, init_x2, init_y1, init_y2
    while True:
        try:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2.rectangle(frame, (init_x1, init_y1), (init_x2, init_y2), colors["green"], 2)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected = cascade.detectMultiScale(frame, scaleFactor=sF, minNeighbors=neighbour)
            for (x, y, w, h) in detected:
                cv2.rectangle(frame, (x, y), (x + w, y + h), colors["white"], 2)
                if(init_y2 < y+h):
                    print("Down")
                    pag.press("down")
                if (init_y1 > y):
                    print("Up")
                    pag.press("up")
                if (init_x2 < x+w):
                    print("Right")
                    pag.press("right")
                if (init_x1 > x):
                    print("Left")
                    pag.press("left")
            cv2.imshow('Gesture Control', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit()
        except Exception as e:
            print(e)
def position(cascade = fist_cascade, gesture = "fist"):
    global init_x1, init_x2, init_y1, init_y2
    while True:
        try:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2.rectangle(frame, (init_x1, init_y1), (init_x2, init_y2), colors["green"], 2)
            display_text(frame, "Position yourself towards the center of the screen", 20, 25, "white")
            display_text(frame, "and then press c", 20, 55, "white")
            display_text(frame, "Please stay atleast 3ft away from the screen", 20, 85, "white")
            display_text(frame, "Press q to exit", 20, 115, "white")
            cv2.imshow('Gesture Control', frame)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                startGesture(cascade)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit()
        except Exception as e:
            print (e)
#position(palm_cascade, "palm")
position()