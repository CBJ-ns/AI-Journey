# 数据清洗与排错日志（Day 4 - Day 5）

## 实验目标
使用开源裂缝数据集（14张图）训练 YOLOv8 模型。

## 报错现场
运行 `task=segment` 时终端报错：`ValueError: Segment dataset requires equal numbers of boxes and segments, but got len(segments) = 10, len(boxes) = 12.`

## 排查过程
1. 检查标签文件（.txt），发现只有 `class_id x_center y_center width height`（边界框坐标），没有 `x1 y1 x2 y2...`（多边形轮廓点）。
2. 明确原因：该数据集是“目标检测”数据集，没有做“分割”所需的像素级掩膜。

## 解决策略
果断放弃分割模型，将任务类型切换为 `task=detect`，模型改为 `yolov8n.pt`。成功规避数据格式不匹配，并在14张图的数据集上跑通了完整的检测训练闭环。

## 工程感悟
1. 必须明确AI任务与数据标签的对应关系（检测框 vs 分割掩膜）。
2. 遇到无法跑通的代码，快速排查是“数据问题”还是“代码问题”。
3. 免费Colab会断线重置文件，以后要用代码自动创建文件夹和YAML配置文件。
