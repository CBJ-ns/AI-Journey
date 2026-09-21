# My AI Journey 🚀

土木，零基础转型 AI  的成长记录。

## 📅 进度记录

### 2026.09.21 · Day 1
- **完成**：在 Google Colab (T4 GPU) 上成功部署 YOLOv8-seg 模型，跑通官方 Demo 及自采照片的推理。
- **踩坑**：遇到了 `FileNotFoundError`，理解了 Colab 云端系统盘 `/` 与工作区 `/content` 的区别，学会用 `!mv` 挪动文件。
- **感悟**：用 YOLOv8s 跑我拍的照片没识别出侧脸小孩和保温杯。理解了预训练模型在非典型场景的泛化能力很弱，要解决裂缝检测问题，必须用专用数据集微调。# AI-Journey
