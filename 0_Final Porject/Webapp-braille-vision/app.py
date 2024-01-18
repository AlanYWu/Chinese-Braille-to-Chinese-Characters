import os
import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

import PIL
from ultralytics import YOLO
from src.convert import convert_to_braille_unicode, parse_xywh_and_class



# Some utilites
import numpy as np
from util import base64_to_pil


# Declare a flask app
app = Flask(__name__)

# constants
CONF = 0.15 # or other desirable confidence threshold level
MODEL_PATH = "./weights/yolov8_braille.pt"
# IMAGE_PATH = "./assets/alpha-numeric.jpeg"

model = YOLO(MODEL_PATH)


print('Model loaded. Check http://127.0.0.1:5000/')

def load_image(IMAGE_PATH):
    """load image from path"""
    image = PIL.Image.open(image_path)
    return image

def model_predict(img, model):
    res = model.predict(img, save=True, save_txt=True, exist_ok=True, conf=CONF)
    boxes = res[0].boxes  # first image
    list_boxes = parse_xywh_and_class(boxes)

    result = ""
    for box_line in list_boxes:
        str_left_to_right = ""
        box_classes = box_line[:, -1]
        for each_class in box_classes:
            str_left_to_right += convert_to_braille_unicode(model.names[int(each_class)])
        result += str_left_to_right + "\n"

    print(result)
    return result


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Save the image to ./uploads
        # img.save("./uploads/image.png")

        # Make prediction
        result = model_predict(img, model)

        
        # Serialize the result, you can add additional fields
        return jsonify(result=result)

    return None


if __name__ == '__main__':
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
