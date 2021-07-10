import cv2
import numpy as np
import mediapipe as mp
from scipy.spatial import distance
import os

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
w, h = 640, 480

def normalize(landmark):
    # Get the normalized x,y coordinates. (Map function)
    return int(landmark.x * w), int(landmark.y * h)

def draw_gauntlet(frame, landmarks):
    # Drawing rest of the gauntlet
    pts = np.array([list(landmarks[0]), list(landmarks[1]), list(landmarks[2]),
                    list(landmarks[5]), list(landmarks[9]), list(landmarks[13]),
                    list(landmarks[17])], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(frame, [pts], (0, 215, 255))
    # Drawing Stones & Joints
    stones = {"2": (0, 255, 0), "5": (128, 0, 128), "9": (242, 162, 2),
              "13": (2, 42, 242), "17": (2, 98, 242), "soul" : (0, 140, 255)}
    thicc = 30
    for i in range(2, 21):
        if (i % 4 != 1):
            # Joints
            cv2.line(frame, landmarks[i - 1], landmarks[i], (0, 215, 255), thickness=thicc)
            if ((i != 2) and ((i - 1) % 4 == 1 or i == 3)): # Deal with it! (Match the dictionary)
                # Stones
                cv2.circle(frame, landmarks[i - 1], 1, stones[str(i - 1)], thickness=thicc - 5)
            else:
                cv2.circle(frame, landmarks[i], 2, (0, 129, 168), thickness=thicc)
    cv2.circle(frame, (landmarks[9][0], landmarks[9][1] + 75), 1, stones["soul"], thickness=thicc - 5)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, w)
    cap.set(4, h)

    hands = mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            landmarks = hand_landmarks.landmark
            landmarks_normal = list(map(normalize, landmarks))

            draw_gauntlet(image, landmarks_normal)

            coords = [landmarks_normal[4], landmarks_normal[12]] # Snap
            dist = distance.cdist(coords, coords, 'euclidean')[0][1]
            #print(dist)
            if dist < 15: # Increase or reduce this
                print("Snap")
                cap.release()
                return False
            #mp_drawing.draw_landmarks(
            #    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('Thanos', image)
        if cv2.waitKey(5) & 0xFF == 27:
          break
    cap.release()
    return True

def gamora():
    cap = cv2.VideoCapture("./Didudoit.mp4")
    while cap.isOpened():
        success, image = cap.read()
        if success:
            cv2.imshow('Why', image)
            cv2.waitKey(5)
        else:
            break
    cap.release()

if __name__ == '__main__':
    if(not main()):
        print("Mr. Stark... I don't feel so good.")
        gamora()
        os.system("shutdown /s /t 1")