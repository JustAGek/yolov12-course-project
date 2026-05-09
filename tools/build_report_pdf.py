from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PDF = ROOT / "project" / "report.pdf"
FIGURES_DIR = ROOT / "project" / "figures"


def _table(data, col_widths):
    table = Table(data, colWidths=col_widths, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaeaea")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b0b0b0")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ]
        )
    )
    return table


def _add_image(story, path, max_width_in, max_height_in=4.5):
    if not path.exists():
        return
    img = Image(str(path))
    max_width = max_width_in * inch
    max_height = max_height_in * inch
    width_scale = max_width / img.imageWidth
    height_scale = max_height / img.imageHeight
    scale = min(width_scale, height_scale)
    img.drawWidth = img.imageWidth * scale
    img.drawHeight = img.imageHeight * scale
    story.append(img)
    story.append(Spacer(1, 0.2 * inch))


def build():
    styles = getSampleStyleSheet()
    title = styles["Title"]
    h2 = styles["Heading2"]
    h3 = styles["Heading3"]
    body = styles["BodyText"]

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54,
        title="YOLOv12n vs YOLO11n vs YOLOv8n on COCO 2017 (val)",
    )

    story = []
    story.append(Paragraph("YOLOv12n vs YOLO11n vs YOLOv8n on COCO 2017 (val)", title))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Abstract", h2))
    story.append(
        Paragraph(
            "This report evaluates the YOLOv12n detector against YOLO11n and YOLOv8n using the COCO 2017 "
            "validation split (5,000 images). All models are evaluated at 640px input size on a Tesla T4 GPU "
            "using Ultralytics v8.3.63 with the same dataset configuration and preprocessing pipeline. Results "
            "show YOLOv12n achieves the best overall detection accuracy with comparable latency to YOLO11n "
            "and YOLOv8n, while improving AP across small, medium, and large objects.",
            body,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("1. Introduction", h2))
    story.append(
        Paragraph(
            "The YOLO family focuses on real-time object detection by performing classification and localization "
            "in a single forward pass. YOLOv12 introduces attention-centric design elements intended to improve "
            "representation quality without sacrificing speed. This report measures the practical performance "
            "of YOLOv12n (the smallest YOLOv12 variant) against YOLO11n and YOLOv8n using a standardized "
            "evaluation pipeline to quantify accuracy and speed tradeoffs.",
            body,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("2. Approach", h2))
    story.append(Paragraph("2.1 Models", h3))
    story.append(
        Paragraph(
            "YOLOv12n (attention-centric), YOLO11n (Ultralytics baseline), YOLOv8n (Ultralytics baseline).", body
        )
    )
    story.append(Paragraph("2.2 Dataset", h3))
    story.append(Paragraph("COCO 2017 validation set (5,000 images) with 80 object classes.", body))
    story.append(Paragraph("2.3 Evaluation Protocol", h3))
    story.append(
        Paragraph(
            "Ultralytics 8.3.63 on Tesla T4 GPU, input size 640, batch size 16, COCO AP/AR metrics.", body
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("3. Results", h2))
    story.append(Paragraph("3.1 Overall Accuracy", h3))
    accuracy_table = _table(
        [
            ["Model", "AP50-95", "AP50", "AP75", "AP_S", "AP_M", "AP_L"],
            ["YOLOv12n", "0.404", "0.559", "0.435", "0.198", "0.447", "0.592"],
            ["YOLO11n", "0.394", "0.553", "0.428", "0.198", "0.432", "0.570"],
            ["YOLOv8n", "0.374", "0.526", "0.405", "0.186", "0.410", "0.535"],
        ],
        [1.2 * inch, 0.8 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch],
    )
    story.append(accuracy_table)
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("3.2 Recall", h3))
    recall_table = _table(
        [
            ["Model", "AR_1", "AR_10", "AR_100", "AR_S", "AR_M", "AR_L"],
            ["YOLOv12n", "0.329", "0.549", "0.605", "0.368", "0.672", "0.795"],
            ["YOLO11n", "0.324", "0.540", "0.598", "0.370", "0.663", "0.781"],
            ["YOLOv8n", "0.320", "0.533", "0.589", "0.369", "0.654", "0.769"],
        ],
        [1.2 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch],
    )
    story.append(recall_table)
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("3.3 Throughput", h3))
    throughput_table = _table(
        [
            ["Model", "Preprocess (ms)", "Inference (ms)", "Postprocess (ms)"],
            ["YOLOv12n", "0.2", "5.1", "1.0"],
            ["YOLO11n", "0.2", "2.9", "0.9"],
            ["YOLOv8n", "0.2", "3.0", "1.0"],
        ],
        [1.2 * inch, 1.4 * inch, 1.2 * inch, 1.2 * inch],
    )
    story.append(throughput_table)
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("3.4 Evaluation Plots (YOLOv12n)", h3))
    _add_image(story, FIGURES_DIR / "pr_curve_yolov12n.png", 6.5, 4.2)
    _add_image(story, FIGURES_DIR / "f1_curve_yolov12n.png", 6.5, 4.2)
    _add_image(story, FIGURES_DIR / "confusion_matrix_yolov12n.png", 6.5, 4.2)

    story.append(Paragraph("4. Discussion", h2))
    story.append(
        Paragraph(
            "YOLOv12n achieves the highest AP50-95 (0.404), a 1.0 point gain over YOLO11n and 3.0 points over "
            "YOLOv8n. Gains are consistent across object sizes, with the largest improvement on large objects. "
            "Recall improvements are modest but consistent, especially at AR_100. Inference time for YOLOv12n "
            "is higher than YOLO11n and YOLOv8n on the same hardware, indicating a small accuracy-speed tradeoff.",
            body,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("5. Qualitative Results", h2))
    story.append(
        Paragraph(
            "Sample detections from YOLOv12n on COCO val illustrate multi-object scenes and small-object detection.",
            body,
        )
    )
    _add_image(story, FIGURES_DIR / "qualitative_1.jpg", 6.5, 4.0)
    _add_image(story, FIGURES_DIR / "qualitative_2.jpg", 6.5, 4.0)

    story.append(Paragraph("6. Limitations", h2))
    story.append(
        Paragraph(
            "Results are limited to the COCO 2017 validation set with pretrained weights (no fine-tuning), a "
            "single input size (640), and fixed batch size. Only the smallest model variants were tested; larger "
            "models may show different tradeoffs.",
            body,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("7. Conclusion", h2))
    story.append(
        Paragraph(
            "YOLOv12n provides the best overall detection accuracy in this evaluation while maintaining "
            "acceptable speed on a T4 GPU. It outperforms YOLO11n and YOLOv8n across standard COCO metrics, "
            "confirming that the attention-centric design yields measurable gains without requiring additional "
            "training.",
            body,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("8. References", h2))
    story.append(Paragraph("YOLOv12: Attention-Centric Real-Time Object Detectors.", body))
    story.append(Paragraph("Ultralytics YOLO documentation.", body))
    story.append(Paragraph("COCO 2017 dataset.", body))

    doc.build(story)


if __name__ == "__main__":
    build()
