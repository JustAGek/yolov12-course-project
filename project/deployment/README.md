# Deployment

Simple REST API for YOLOv12 inference using FastAPI.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

The API will start on http://0.0.0.0:8000

## Build and run with Docker

```bash
docker build -t yolov12-api .
docker run -p 8000:8000 -e MODEL_PATH=yolov12n.pt yolov12-api
```

## API

- POST /predict
  - Form field: file (image)
  - Response: JSON with detections
