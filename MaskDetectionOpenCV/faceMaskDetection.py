import cv2

face_cascade = cv2.CascadeClassifier('dataXML/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('dataXML/haarcascade_eye.xml')
nose_cascade = cv2.CascadeClassifier('dataXML/haarcascade_mcs_nose.xml')
#Use any one of the .xml files for mouth depending on which one works best
#mouth_cascade = cv2.CascadeClassifier('dataXML/haarcascade_mcs_mouth.xml')
mouth_cascade = cv2.CascadeClassifier('dataXML/Mouth.xml')
upper_body = cv2.CascadeClassifier('dataXML/haarcascade_upperbody.xml')



# Vary this value based on your light (80-105)
bw_threshold = 80

# Font settings for the text thats shown in the frame
font = cv2.FONT_HERSHEY_SIMPLEX
mask_ON_font_color = (0, 255, 0)#BGR
mask_OFF_font_color = (0, 0, 255)#BGR
thickness = 2
font_scale = 1
mask_ON = "Mask"
mask_OFF = "No Mask"

# Read video
cap = cv2.VideoCapture(0)

while True:
    # Get individual frame
    ret, frame = cap.read()
    #Un-comment this to mirror the frame
    #frame = cv2.flip(frame,1)

    # Convert Image into gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert image in black and white
    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
    #cv2.imshow('black_and_white', black_and_white)

    # Detects face
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Face prediction for black and white (For masks that are white in color that are harder to detect)
    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4)

    eyes = eye_cascade.detectMultiScale(gray, 1.5, 5)
    #Mess around with the following code to try and see if you are getting better accuracy.
    '''if len(eyes) != 0:
        print("Im here")
        mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)
        if len(mouth_rects) == 0:
            cv2.putText(frame, mask_ON, (300,300), font, font_scale, mask_ON_font_color, thickness,cv2.LINE_AA)'''
    if(len(faces) == 0 and len(faces_bw) == 0):
        pass
    elif(len(faces) == 0 and len(faces_bw) == 1):
        # If a white colored mask is worn and a face is not detected
        cv2.putText(frame, mask_ON, (30, 30), font, font_scale, mask_ON_font_color, thickness, cv2.LINE_AA)
    else:
        # Draws a rectangle on detected face
        for (x, y, w, h) in faces:
            if len(eyes) != 0:
                print("Im here")
                mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)
                noses = nose_cascade.detectMultiScale(gray, 1.5, 5)
                #Eyes are detected but no mouth or nose is detected (Means the person is wearing a mask)
                if len(mouth_rects) == 0 or len(noses) == 0:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, mask_ON, (x-20, y-20), font, font_scale, mask_ON_font_color, thickness, cv2.LINE_AA)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            #Region of interest (Basically crops out the face into gray and color)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]


            # Detect mouth
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)
            noses = nose_cascade.detectMultiScale(gray, 1.5, 5)
        # Face detected but no mouth detected means person is wearing mask
        if(len(mouth_rects) == 0 or len(noses) == 0):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, mask_ON, (x - 20, y - 20), font, font_scale, mask_ON_font_color, thickness, cv2.LINE_AA)

        else:
            for (mx, my, mw, mh) in mouth_rects:

                if(y < my < y + h):
                    # Face and Lips are detected but lips coordinates are within face cordinates which `means lips prediction is true and
                    # person is not waring mask
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, mask_OFF, (x - 20, y - 20), font, font_scale, mask_OFF_font_color, thickness, cv2.LINE_AA)

                    #cv2.rectangle(frame, (mx, my), (mx + mh, my + mw), (0, 0, 255), 3)
                    break

    # Show frame with results
    cv2.imshow('Mask Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video
cap.release()
cv2.destroyAllWindows()
