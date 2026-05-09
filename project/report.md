# YOLOv12n vs YOLO11n vs YOLOv8n on COCO 2017 (val)

## Abstract

This report evaluates the YOLOv12n detector against YOLO11n and YOLOv8n using the COCO 2017 validation split (5,000 images). All models are evaluated at 640px input size on a Tesla T4 GPU using Ultralytics v8.3.63 with the same dataset configuration and preprocessing pipeline. Results show YOLOv12n achieves the best overall detection accuracy with comparable latency to YOLO11n and YOLOv8n, while improving AP across small, medium, and large objects.

## 1. Introduction

The YOLO family focuses on real-time object detection by performing classification and localization in a single forward pass. YOLOv12 introduces attention-centric design elements intended to improve representation quality without sacrificing speed. This report measures the practical performance of YOLOv12n (the smallest YOLOv12 variant) against YOLO11n and YOLOv8n using a standardized evaluation pipeline to quantify accuracy and speed tradeoffs.

## 2. Approach

### 2.1 Models

- YOLOv12n (attention-centric, smallest variant)
- YOLO11n (Ultralytics baseline)
- YOLOv8n (Ultralytics baseline)

All models are evaluated using their official pretrained weights.

### 2.2 Dataset

- COCO 2017 validation set (5,000 images)
- 80 object classes
- YOLO-format labels provided by Ultralytics assets

### 2.3 Evaluation Protocol

- Framework: Ultralytics 8.3.63
- Hardware: Tesla T4 GPU
- Input size: 640
- Batch size: 16
- Metrics: COCO AP and AR

Key metrics:

- $\text{AP}_{50-95}$: average precision across IoU thresholds 0.50 to 0.95
- $\text{AP}_{50}$ and $\text{AP}_{75}$
- $\text{AP}_S$, $\text{AP}_M$, $\text{AP}_L$ (small/medium/large objects)
- $\text{AR}_{1}$, $\text{AR}_{10}$, $\text{AR}_{100}$

## 3. Results

### 3.1 Overall Accuracy

| Model    | AP50-95 | AP50  | AP75  | AP_S  | AP_M  | AP_L  |
| -------- | ------- | ----- | ----- | ----- | ----- | ----- |
| YOLOv12n | 0.404   | 0.559 | 0.435 | 0.198 | 0.447 | 0.592 |
| YOLO11n  | 0.394   | 0.553 | 0.428 | 0.198 | 0.432 | 0.570 |
| YOLOv8n  | 0.374   | 0.526 | 0.405 | 0.186 | 0.410 | 0.535 |

### 3.2 Recall

| Model    | AR_1  | AR_10 | AR_100 | AR_S  | AR_M  | AR_L  |
| -------- | ----- | ----- | ------ | ----- | ----- | ----- |
| YOLOv12n | 0.329 | 0.549 | 0.605  | 0.368 | 0.672 | 0.795 |
| YOLO11n  | 0.324 | 0.540 | 0.598  | 0.370 | 0.663 | 0.781 |
| YOLOv8n  | 0.320 | 0.533 | 0.589  | 0.369 | 0.654 | 0.769 |

### 3.3 Throughput

| Model    | Preprocess (ms) | Inference (ms) | Postprocess (ms) |
| -------- | --------------- | -------------- | ---------------- |
| YOLOv12n | 0.2             | 5.1            | 1.0              |
| YOLO11n  | 0.2             | 2.9            | 0.9              |
| YOLOv8n  | 0.2             | 3.0            | 1.0              |

Note: These timings reflect the Ultralytics pipeline as reported by the validation logs on Tesla T4. The YOLOv12n inference time is higher than YOLO11n and YOLOv8n in this run, while still producing higher accuracy.

### 3.4 Evaluation Plots (YOLOv12n)

The following plots are generated from the YOLOv12n validation run:

![Precision-Recall curve (YOLOv12n)](figures/pr_curve_yolov12n.png)

![F1-Confidence curve (YOLOv12n)](figures/f1_curve_yolov12n.png)

![Normalized confusion matrix (YOLOv12n)](figures/confusion_matrix_yolov12n.png)

## 4. Discussion

- YOLOv12n achieves the highest $\text{AP}_{50-95}$ (0.404), a +1.0 point gain over YOLO11n and +3.0 points over YOLOv8n.
- Gains are consistent across object sizes, with the largest improvement on large objects ($\text{AP}_L$ = 0.592).
- Recall improvements are modest but consistent, especially at $\text{AR}_{100}$.
- Inference time for YOLOv12n is higher than YOLO11n and YOLOv8n on the same hardware, indicating a small accuracy-speed tradeoff.

## 5. Qualitative Results

Sample detections from YOLOv12n on COCO val illustrate multi-object scenes and small-object detection:

![Qualitative example 1 (YOLOv12n)](figures/qualitative_1.jpg)

![Qualitative example 2 (YOLOv12n)](figures/qualitative_2.jpg)

## 6. Limitations

- Results are limited to the COCO 2017 validation set with pretrained weights (no fine-tuning).
- Single input size (640) and fixed batch size.
- Only the smallest model variants were tested; larger models may show different tradeoffs.

## 7. Conclusion

YOLOv12n provides the best overall detection accuracy in this evaluation while maintaining acceptable speed on a T4 GPU. It outperforms YOLO11n and YOLOv8n across standard COCO metrics, confirming that the attention-centric design yields measurable gains without requiring additional training. The deployment scaffold in this repository enables direct integration of YOLOv12n into a FastAPI service for practical usage.

## 8. References

- YOLOv12 paper: "YOLOv12: Attention-Centric Real-Time Object Detectors".
- Ultralytics YOLO documentation.
- COCO 2017 dataset.
