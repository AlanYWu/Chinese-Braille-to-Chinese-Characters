from flask import Flask, request
import retinaface

Model = retinaface.retinaface()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# /setmodel用于修改模型
@app.route('/setmodel', methods=['POST'])
def initialization():
    if request.method == 'POST':
        model_mold = request.form
        
        # Model.setModel(model_mold["model_mold"])
    return "initialization " + model_mold["model_mold"] + " finish"

# /predict用于预测
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.form
        keys_Points = Model.receive_results(file["img_path"])
        return keys_Points



if __name__ == '__main__':
    app.run()