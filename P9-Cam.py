# import json
import cv2
# import numpy as np
# import time
# import requests
from flask import jsonify
from collections import Counter
from datetime import datetime
from waitress import serve
from flask import Flask, render_template, Response, stream_with_context, request, json, jsonify

video = cv2.VideoCapture(0)
video.set(3, 640)
video.set(4, 360)
port = 5000

# create a variable name of Flask
app = Flask('__name__')


def video_stream():

    ret, frame = video.read()
    while True:
        ret, frame = video.read()
        if not ret:
            break
        else:
            time.sleep(0.1)
            # cv2.imshow('frame',frame)
            # cv2.imshow('zoom',zoom)
            # cv2.imshow('ZC',zc)
            # print('ZC size = ',zc.shape) # size of frame 360,360
            # cv2.imshow("result", result)
            key = cv2.waitKey(1)
            if key == 27:
                cv2.destroyAllWindows()

            ret, buffer = cv2.imencode('.jpeg', frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port='5000', debug=False)
    print('Starting server in localhost:'+str(port))
    serve(app, host='0.0.0.0', port=port, threads=2)
