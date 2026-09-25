import torch
from ultralytics import YOLO

# 1. 检查显卡
print("=" * 30)
print("CUDA是否可用:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("你的显卡型号:", torch.cuda.get_device_name(0))
print("=" * 30)

# 2. 让 YOLO 跑一次推理
print("正在下载 YOLOv8n 模型并推理...")
model = YOLO('yolov8n.pt')
results = model('qunxiang.png')
results[0].save('my_local_first_result.jpg')
print("推理完成！去左侧文件夹找 my_local_first_result.jpg")