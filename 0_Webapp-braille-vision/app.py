import os
import sys

# Flask网络框架和用于处理HTTP请求和响应的工具
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

import PIL  # 用于图像处理的Python图像处理库
from ultralytics import YOLO  # 导入YOLO对象检测模型
from src.convert import convert_to_braille_unicode, parse_xywh_and_class  # 自定义的转换和解析工具

# 用于数值运算的NumPy库
import numpy as np
from util import base64_to_pil  # 将base64图像转换为PIL格式的工具

# 初始化一个Flask应用
app = Flask(__name__)

# 模型配置的常量
CONF = 0.15  # YOLO模型预测的置信度阈值
MODEL_PATH = "./models/yolov8_braille.pt"  # 训练好的YOLO模型的路径

# 载入YOLO模型
model = YOLO(MODEL_PATH)

print('模型已加载。请访问 http://127.0.0.1:5000/')
    
def load_image(IMAGE_PATH):
    """从指定的文件路径加载图像。"""
    image = PIL.Image.open(IMAGE_PATH)
    return image

def model_predict(img, model):
    """
    使用YOLO模型对给定图像进行预测。
    
    参数:
    - img: 要进行预测的图像。
    - model: YOLO模型实例。
    
    返回:
    - result: 预测结果的字符串表示。
    """
    # 使用模型进行预测
    res = model.predict(img, save=True, save_txt=True, exist_ok=True, conf=CONF)
    boxes = res[0].boxes  # 提取第一张图像的边界框
    list_boxes = parse_xywh_and_class(boxes)  # 解析框以获取类别和坐标

    result = ""
    # 遍历框，构造结果字符串
    for box_line in list_boxes:
        str_left_to_right = ""
        box_classes = box_line[:, -1]
        for each_class in box_classes:
            str_left_to_right += convert_to_braille_unicode(model.names[int(each_class)])
        result += str_left_to_right + "\n"

    print(result)
    return result

# 定义Web应用程序的根路由
@app.route('/', methods=['GET'])
def index():
    """渲染Web应用程序的主页面。"""
    return render_template('index.html')

# 定义处理预测逻辑的预测路由
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # 处理POST请求中接收的图像
        img = base64_to_pil(request.json)

        # 使用模型预测结果
        result = model_predict(img, model)

        # 以JSON格式返回结果
        return jsonify(result=result)

    return None

#api
#Henry 240118 2230
@app.route('/api/predict', methods=['POST'])
def api_predict():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400

    file = request.files['file']
    
    # 确保文件的存在
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    # 使用YOLO模型进行预测
    image = Image.open(io.BytesIO(file.read()))
    result = model_predict(image, model)

    # 返回预测结果
    return jsonify({'result': result})

# 运行Flask应用程序的主入口点
if __name__ == '__main__':
    # 使用gevent WSGI服务器提供应用
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()

