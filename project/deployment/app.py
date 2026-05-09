import io
import os
from typing import Any, Dict, List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from ultralytics import YOLO

app = FastAPI(title="YOLOv12 API")

MODEL_PATH = os.getenv("MODEL_PATH", "yolov12n.pt")

try:
    model = YOLO(MODEL_PATH)
except Exception as exc:
    raise RuntimeError(f"Failed to load model from {MODEL_PATH}: {exc}")


def _format_results(results) -> List[Dict[str, Any]]:
    detections: List[Dict[str, Any]] = []
    for r in results:
        if r.boxes is None:
            continue
        boxes = r.boxes
        for i in range(len(boxes)):
            xyxy = boxes.xyxy[i].tolist()
            conf = float(boxes.conf[i]) if boxes.conf is not None else None
            cls_id = int(boxes.cls[i]) if boxes.cls is not None else None
            detections.append({
                "bbox_xyxy": xyxy,
                "confidence": conf,
                "class_id": cls_id,
            })
    return detections


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")

    data = await file.read()
    try:
        image = Image.open(io.BytesIO(data)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid image: {exc}")

    results = model.predict(image, verbose=False)
    detections = _format_results(results)
    return JSONResponse({"detections": detections})


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_PATH}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
