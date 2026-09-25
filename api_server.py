from fastapi import FastAPI, File, UploadFile, HTTPException
from ultralytics import YOLO
import shutil
import os

# 1. 初始化 FastAPI 应用
app = FastAPI(title="CrackEye AI API")

# 2. 加载你训练好的模型 (如果你本地路径不同，请修改)
# 如果没有训练好的，可以先用官方 yolov8n.pt 测试
MODEL_PATH = "runs/detect/train/weights/best.pt"
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = "yolov8n.pt"
    print("未找到自训练模型，使用官方预训练模型进行测试。")

model = YOLO(MODEL_PATH)


# 3. 定义根路径，确认服务是否活着
@app.get("/")
def read_root():
    return {"message": "CrackEye 模型推理服务已启动", "model": MODEL_PATH}


# 4. 定义核心推理接口
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 4.1 检查文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件 (jpg/png)")

    # 4.2 保存上传的图片到本地临时文件
    temp_file_path = "temp_uploaded_image.jpg"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")

    # 4.3 进行推理
    try:
        results = model(temp_file_path)
        result = results[0]

        # 4.4 提取结果数据
        detections = []
        for box in result.boxes:
            # 获取坐标、置信度、类别
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = result.names[class_id]

            detections.append({
                "class": class_name,
                "confidence": round(confidence, 4),
                "bbox": [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)]
            })

        # 4.5 清理临时文件
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        # 4.6 返回 JSON 结果
        return {
            "filename": file.filename,
            "detections_count": len(detections),
            "detections": detections
        }
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"模型推理失败: {str(e)}")