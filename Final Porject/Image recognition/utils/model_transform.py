import torch
import torch.utils.data.distributed

# pytorch环境中
model_pt =" yolov8_braille.pt"
mobile_pt_new ='model.pt' # 将模型保存为Android可以调用的文件

model = torch.load(model_pt)
model.eval() # 模型设为评估模式
device = torch.device('cpu')
model.to(device)
# 1张3通道224*224的图片
input_tensor = torch.rand(1, 3, 224, 224) # 设定输入数据格式

mobile = torch.jit.trace(model, input_tensor) # 模型转化
mobile.save(mobile_pt_new) # 保存文件