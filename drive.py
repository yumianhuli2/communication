#parsing command line arguments
import argparse
#decoding camera images
import base64
#for frametimestamp saving
from datetime import datetime
#reading and writing files
import os
#high level file operations
import shutil
#matrix math
import numpy as np
#real-time server
import socketio
#concurrent networking 
import eventlet
#web server gateway interface
import eventlet.wsgi
#image manipulation
from PIL import Image
#web framework
from flask import Flask
#input output
from io import BytesIO

#load our saved model
from keras.models import load_model

#helper class
import utils

import cv2

#initialize our server
sio = socketio.Server()
#our flask (web) app
app = Flask(__name__)

#init our model and image array as empty
# model = None
# prev_image_array = None


#registering event handler for the server
@sio.on('telemetry')
def telemetry(sid, data):
    if data:
        image = Image.open(BytesIO(base64.b64decode(data["image"])))

        img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        # print(str(image.size))
        cv2.imshow("Test", img)
        cv2.waitKey(1)

        try:
            #pytorch code here


            #send command to client
            command = 456
            run(command)
        except Exception as e:
            print(e)
    else:
        sio.emit('manual', data={}, skip_sid=True)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    # send_control(0, 0)
    # send_control(123)
    run(123)

def run(command):
    sio.emit(
        "run",
        data={
            'command': command.__str__()
        },
        skip_sid=True)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Remote Driving')
    # parser.add_argument(
    #     'model',
    #     type=str,
    #     help='Path to model file. Model should be on the same path.'
    # )
    # parser.add_argument(
    #     'image_folder',
    #     type=str,
    #     nargs='?',
    #     default='',
    #     help='Path to image folder. This is where the images from the run will be saved.'
    # )
    # args = parser.parse_args()
    #
    # #load model
    # model = load_model(args.model)
    #
    # if args.image_folder != '':
    #     print("Creating image folder at {}".format(args.image_folder))
    #     if not os.path.exists(args.image_folder):
    #         os.makedirs(args.image_folder)
    #     else:
    #         shutil.rmtree(args.image_folder)
    #         os.makedirs(args.image_folder)
    #     print("RECORDING THIS RUN ...")
    # else:
    #     print("NOT RECORDING THIS RUN ...")

    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)

    cv2.destroyAllWindows()
