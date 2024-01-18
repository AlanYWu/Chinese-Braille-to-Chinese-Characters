# 用于HTTP Post请求过程模拟。
# import requests
# resp = requests.post("http://localhost:5000/setmodel",
#                      data={'model_mold': 'mobilenetX0.25'})
# print(resp.text)


import requests
resp = requests.post("http://localhost:5000/predict",
                     data={'img_path': '"./assets/alpha-numeric.jpeg"'})
print(resp.text)
