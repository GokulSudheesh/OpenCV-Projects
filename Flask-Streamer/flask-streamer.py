import cv2
from flask import Flask, render_template, Response


class Capture:
    def __init__(self, width=640, height=480):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, width)
        self.cap.set(4, height)

    def get_frames(self):
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


app = Flask(__name__)
cap_frame = Capture(1080, 720)


@app.route('/video_feed')
def video_feed():
    return Response(cap_frame.get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
