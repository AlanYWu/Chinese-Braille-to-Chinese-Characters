# Flask网络框架和用于处理HTTP请求和响应的工具
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from werkzeug.debug import DebuggedApplication
import os
import sys






# 用于数值运算的NumPy库
import numpy as np

import requests

# 初始化一个Flask应用
app = Flask(__name__)

# 定义Web应用程序的根路由
@app.route('/', methods=['GET'])
def index():
    #渲染Web应用程序的主页面#
    image_files = os.listdir('./static/example_data')
    print(image_files)
    return render_template('index.html', image_files=image_files)


@app.route('/submit_example', methods=['POST'])
def submit_example():
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


# henry 240628 1500

# 获取图片参数 向api发送 获取一个string

import base64

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':

        # 处理POST请求中接收的图像
        img = base64_to_pil(request.json)

        # 预留：向 get_string_from_api1 发送图片，获取一个string

        raw_result = img2braille(img)

        # 使用 split_braille_sentences 函数将字符串分割为句子

        split_result = split_braille_sentences(raw_result)

        # 预留：将分割后的句子发送给 get_string_from_api2，获取一个string

        # 使用模型预测结果 [ab]
        # result = model_predict(img, model)
        final_result = braille2chinese(split_result)
        
        cnp_Result = "" #BtoCNP(final_result)

        eng_Result = "" #BtoENG(final_result)

        result = final_result#太傻了
        
        # 返回预测结果
        return jsonify({'result': result, 'CNP_Result': cnp_Result, 'ENG_Result': eng_Result})

    return None


# @app.route('/predict', methods=['POST'])
# def img2braille(file_path, url='http://localhost:5000/upload'):
#     img = base64
#     file_path = 'input.jpg'  # Update this path to the file you want to upload

#     with open(file_path, 'rb') as file:
#         files = {'file': (file_path, file)}
#         response = requests.post(url, files=files)
#     print(f'Status Code: {response.status_code}')
#     print(f'Response: {response.text}')
#     return response.text

def img2braille(img64):
    url= 'http://localhost:5000/upload')
      # Update this path to the file you want to upload
    response = requests.post(url,img64)

    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.text}')
    return response.text


# 获取一个列表，每一次发送一个string，返回一个string，最后将所有string拼接在一起

def split_braille_sentences(input_string):
    # 定义 Braille 标点符号
    braille_punctuation = {"⠐⠆": ".", "⠐⠄": "?", "⠰⠂": "!"}
    
    # 初始化临时字符串和结果列表
    temp_sentence = ""
    result = []
    
    # 遍历输入字符串中的每个字符
    i = 0
    while i < len(input_string):
        # 检查是否遇到 Braille 标点符号
        for braille_symbol, punctuation in braille_punctuation.items():
            if input_string[i:i+len(braille_symbol)] == braille_symbol:
                # 如果遇到标点符号，将当前句子添加到结果列表
                result.append(temp_sentence.strip() + punctuation)
                temp_sentence = ""
                i += len(braille_symbol)
                break
        else:
            # 如果没有遇到标点符号，则添加当前字符到临时字符串
            temp_sentence += input_string[i]
            i += 1
    
    # 添加最后一个句子（如果有的话）
    if temp_sentence.strip():
        result.append(temp_sentence.strip())
    
    return result

def braille2chinese(string_list):
    result = ""
    url = "http://localhost:5000/upload"
    for string in string_list:
        response = requests.post(url, data=string)
        result += response.text
    return result



# 运行Flask应用程序的主入口点
if __name__ == '__main__':
    # 使用gevent WSGI服务器提供应用
    # app.debug = True
    # http_server = WSGIServer(('0.0.0.0', 5000), DebuggedApplication(app, True))
    # http_server.serve_forever()
    app.run(debug=True)


"""
    def model_predict(img, model):
    # 使用模型预测结果 --YOLO
    result = None
    return result

# 这个也不用 0628


# Henry 240628 1520
# 前端用的是这个api
# 定义处理预测逻辑的预测路由
@app.route('old/predict', methods=['GET', 'POST'])
def predict():
    import PIL  # 用于图像处理的Python图像处理库
    from util import base64_to_pil  # 将base64图像转换为PIL格式的工具

    if request.method == 'POST':
            
    # 翻译
    #Henry 240203 2000

    # 扔了 0628
        def BtoCNP(input):

            import io
            import unicodedata
            # The fucntion can receive inputs from txt.
            # f = io.open('./a.txt', 'r', encoding = 'utf8')
            # t = f.read()

            dic = {chr(0x2803):'b',
                chr(0x2809):'c',
                chr(0x281F):'ch',
                chr(0x2819):'d',
                chr(0x280B):'f',
                chr(0x281B):'g/j',
                chr(0x2813):'h/x',
                chr(0x2805):'k/q',
                chr(0x2807):'l',
                chr(0x280D):'m',
                chr(0x281D):'n',
                chr(0x280F):'p',
                chr(0x281A):'r',
                chr(0x280E):'s',
                chr(0x2831):'sh',
                chr(0x281E):'t',
                chr(0x2835):'z',
                chr(0x280C):'zh',
                chr(0x2814):'a',
                chr(0x282A):'ai',
                chr(0x2827):'an',
                chr(0x2826):'ang',
                chr(0x2816):'ao',
                chr(0x2822):'o/e',
                chr(0x282E):'ei',
                chr(0x2834):'en',
                chr(0x283C):'eng',
                chr(0x2817):'er',
                chr(0x280A):'i/yi',
                chr(0x282B):'ia/ya',
                chr(0x2811):'ie/ye',
                chr(0x281C):'iao/yao',
                chr(0x2833):'iu/you',
                chr(0x2829):'ian/yan',
                chr(0x2823):'in/yin',
                chr(0x282D):'iang/yang',
                chr(0x2821) : 'ing/ying',
                chr(0x2839) : 'iong/yong',
                chr(0x2832) : 'ong/weng',
                chr(0x2837) : 'ou',
                chr(0x2825) : 'u/wu',
                chr(0x283F) : 'ua/wa',
                chr(0x283D) : 'uai/wai',
                chr(0x283B) : 'uan/wan',
                chr(0x2836) : 'uang/wang',
                chr(0x283A) : 'ui/wei',
                chr(0x283B) : 'un/wen',
                chr(0x2815) : 'uo/wo',
                chr(0x282C) : 'v/yu',
                chr(0x2812) : 'un/yuan',
                chr(0x283E) : 'ue/yue',
                chr(0x2838) : 'en',
                chr(0x2801) : '1',
                chr(0x2802) : '2',
                chr(0x2804) : '3',
                chr(0x2806) : '4',
                chr(0x2800) : ' ',
                chr(0x2810) : ','
                }
            output = ''
            for i in input:
                ch = dic.get(i)
                if not ch is None:
                    output += ch
                elif i == ' ':
                    output += ' '
                else:
                    output += '*'
                    print(i, 'notfound')
            return output
                
        # 这个也扔了 0628
        def BtoENG(brailleToEnglish):
            inputString = ''

            alphaBraille = ['⠁', '⠃', '⠉', '⠙', '⠑', '⠋', '⠛', '⠓', '⠊', '⠚', '⠅', '⠇',
                '⠍', '⠝', '⠕', '⠏', '⠟', '⠗', '⠎', '⠞', '⠥', '⠧', '⠺', '⠭', '⠽', '⠵', ' ']
            numBraille = ['⠼⠁', '⠼⠃', '⠼⠉', '⠼⠙', '⠼⠑', '⠼⠋', '⠼⠛', '⠼⠓', '⠼⠊', '⠼⠚']
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
            nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            puntuation = [',',';',':','.','?','!', ';','(',')', '/', '-']
            puntuationBraille = ['⠂','⠆','⠒','⠲','⠦','⠖','⠐⠣','⠐⠜','⠸⠌','⠤']
            character = ['&','*','@','©','®','™','°',]
            characterBraille = ['⠈⠯','⠐⠔','⠈⠁','⠘⠉','⠘⠗','⠘⠞','⠘⠚',]

            if len(brailleToEnglish) > 0 : 
                for n in brailleToEnglish:
                    if n in alphaBraille:
                        inputString += alphabet[alphaBraille.index(n)]
                    elif n in numBraille:
                        inputString += nums[numBraille.index(n)]
                    elif n in puntuationBraille:
                        inputString += puntuation[puntuationBraille.index(n)]
                    elif n in characterBraille:
                        inputString += character[characterBraille.index(n)]
                return inputString

            # 处理POST请求中接收的图像
            img = base64_to_pil(request.json) #FIXME: 不一定需要加入base64_to_pil，直接传入图片是否可行？
            img = request.json

            # 预留：向 get_string_from_api1 发送图片，获取一个string

            raw_result = get_string_from_api1(img)

            # 使用 split_braille_sentences 函数将字符串分割为句子

            split_result = split_braille_sentences(raw_result)

            # 预留：将分割后的句子发送给 get_string_from_api2，获取一个string

            # 使用模型预测结果 [ab]
            # result = model_predict(img, model)
            final_result = get_string_from_api2(split_result)
            
            cnp_Result = BtoCNP(final_result)

            eng_Result = BtoENG(final_result)

            result = final_result#太傻了
            
            # 返回预测结果
            return jsonify({'result': result, 'CNP_Result': cnp_Result, 'ENG_Result': eng_Result})

        return "This function is outdated. Please use the new API at /api/predict instead."

# 翻译所需的路由
#Henry 240321 1900  程序极度不安全，有任意代码风险，建议此处1.增加输入验证；2.建议增加鉴权；3.别说是我写的
@app.route('/py_translate', methods=['GET', 'POST'])
def py_translate():

    if request.method == 'POST':
        input_data = request.json['input']  # 从JSON中获取输入

        result = pinyin2hanziAPI.server_braille_to_chinese_API.main(input_data)

    return jsonify({'result': result, 'input_data': input_data })  # 返回结果

#api
#Henry 240118 2230
#Henry 20240203 2000 添加多结果
# 前端没用 0628
@app.route('old-old/api/predict', methods=['POST'])
def api_predict():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400

    file = request.files['file']
    
    # 确保文件的存在
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    # 使用YOLO模型进行预测
    # image = Image.open(io.BytesIO(file.read()))
    img = base64_to_pil(request.json)
    result = model_predict(img, model)

    
    cnp_Result =  BtoCNP(result)

    eng_Result = BtoENG(result)
    # 返回预测结果
    return jsonify({'result': result, 'CNP_Result': cnp_Result, 'ENG_Result': eng_Result})
    """