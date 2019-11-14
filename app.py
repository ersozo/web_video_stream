from flask import Flask, render_template, render_template, Response
import cv2
import socket
import io


app = Flask(__name__)

cam = cv2.VideoCapture(0)


@app.route("/")
def index():
    return render_template("index.html")


def gen():
    """Video streaming generator function."""
    while True:
        # capture frame-by-frame
        ret, frame = cam.read()
        cv2.imwrite('pic.jpg', frame)

        # yield the output frame in the byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n')

@app.route("/video")
def video():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
