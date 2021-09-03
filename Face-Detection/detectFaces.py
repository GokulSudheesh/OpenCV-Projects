import cv2
import numpy as np

w, h = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, w)
cap.set(4, h)

prototxtPath = "./facenet/deploy.prototxt.txt"
weightsPath = "./facenet/res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
IMAGE_SIZE = 224

def get_faces(frame):
    faces = []
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                                 (104.0, 177.0, 123.0))
    faceNet.setInput(blob)
    detections = faceNet.forward()
    print(detections.shape)
    for j in range(0, detections.shape[2]):
        confidence = detections[0, 0, j, 2]
        if confidence > 0.5:
            box = detections[0, 0, j, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            (startX, startY) = (max(0, startX - 20), max(0, startY - 20))
            (endX, endY) = (min(w - 1, endX + 20), min(h - 1, endY + 20))

            face = frame[startY:endY, startX:endX]
            face = cv2.resize(face, (IMAGE_SIZE, IMAGE_SIZE))
            faces.append([face, (startX, startY), (endX, endY)])
    return faces

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    image = cv2.flip(image, 1)
    try:
        faces = get_faces(image)
        for face in faces:
            cv2.rectangle(image, face[1], face[2], (255, 0, 0), 2)
    except Exception as e:
        print(e)
    cv2.imshow("Test", image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
