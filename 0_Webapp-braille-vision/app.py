# Flask网络框架和用于处理HTTP请求和响应的工具
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
# from gevent.pywsgi import WSGIServer
from werkzeug.debug import DebuggedApplication
from io import BytesIO
import os
import sys
import numpy as np
import requests
import base64
import uuid
import logging

# 初始化一个Flask应用
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# 定义Web应用程序的根路由
@app.route('/', methods=['GET'])
def index():
    #渲染Web应用程序的主页面#
    image_files = os.listdir('./static/example_data')
    print(image_files)
    return render_template('index.html', image_files=image_files)

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Ensure the file exists
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file
    print(os.path.join('example_data', secure_filename(file.filename)))
    file.save(os.path.join('example_data', secure_filename(file.filename)))

    return jsonify({'message': 'File has been saved successfully.'}), 200


# 以下为计算逻辑

# henry 240628 1500
# henry 240630 0100 
# henry 240630 1120 
# 获取图片 向api发送 获取一个盲文string 拆分string 翻译为中文


# 设置保存图像的目录
SAVE_DIR = 'uploaded_images'
os.makedirs(SAVE_DIR, exist_ok=True)

# 设置日志记录
logging.basicConfig(level=logging.INFO)

def upload_file(file_path, url):
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(url, files={'file': (file_path, f)})
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f'Failed to upload file to {url}: {e}')
        raise

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_data = data  # 确保从请求中正确获取图像数据

    if not image_data or not image_data.startswith('data:image'):
        return jsonify({'error': 'Invalid image data'}), 400

    try:
        _, image_data = image_data.split(',', 1)
        image_data = base64.b64decode(image_data)
    except (ValueError, base64.binascii.Error) as e:
        logging.error(f'Error decoding image data: {e}')
        return jsonify({'error': 'Invalid image data'}), 400

    image_filename = os.path.join(SAVE_DIR, 'uploaded_image.png')
    try:
        with open(image_filename, 'wb') as f:
            f.write(image_data)
    except IOError as e:
        logging.error(f'Error saving image: {e}')
        return jsonify({'error': 'Failed to save image'}), 500

    url = "http://49.233.9.116:6700/image_to_chinese"
    try:
        result = upload_file(image_filename, url)
        result_text = result.text
    except requests.RequestException:
        return jsonify({'error': 'Failed to upload image to API'}), 500
    finally:
        try:
            os.remove(image_filename)
        except OSError as e:
            logging.warning(f'Failed to remove image file: {e}')

    return jsonify({
        'result': result_text,
        'CNP_Result': '',
        'ENG_Result': ''
    })


# 运行Flask应用程序的主入口点
if __name__ == '__main__':
    # 使用gevent WSGI服务器提供应用
    # app.debug = True
    # http_server = WSGIServer(('0.0.0.0', 5000), DebuggedApplication(app, True))
    # http_server.serve_forever()
    app.run(debug=True)