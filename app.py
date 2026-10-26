from flask import Flask, render_template, request, send_file
import qrcode
import os
import cv2
from werkzeug.utils import secure_filename
from database import create_table, save_history, get_history

app = Flask(__name__)
create_table()

QR_FOLDER = "generated_qr"
UPLOAD_FOLDER = "uploads"

os.makedirs(QR_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/history")
def history():
    records = get_history()
    return render_template("history.html", records=records)

@app.route("/generate",
methods=["POST"])
def generate_qr():
    data = request.form.get("data", "").strip()

    if not data:
        return render_template(
            "index.html",
            error="Please enter text or a URL."
        )

    file_path = os.path.join(QR_FOLDER, "generated_qr.png")
    qrcode.make(data).save(file_path)

    save_history("Generated", data)

    return render_template(
        "index.html",
        generated=True,
        qr_data=data
    )


@app.route("/qr-image")
def qr_image():
    file_path = os.path.join(QR_FOLDER, "generated_qr.png")

    if not os.path.exists(file_path):
        return "QR image not found.", 404

    return send_file(file_path, mimetype="image/png")


@app.route("/download-qr")
def download_qr():
    file_path = os.path.join(QR_FOLDER, "generated_qr.png")

    if not os.path.exists(file_path):
        return "Generate a QR code first.", 404

    return send_file(
        file_path,
        mimetype="image/png",
        as_attachment=True,
        download_name="my_qr_code.png"
    )


@app.route("/detect", methods=["POST"])
def detect_qr():
    uploaded = request.files.get("file")

    if not uploaded or not uploaded.filename:
        return render_template(
            "index.html",
            error="Please select an image to scan."
        )

    filename = secure_filename(uploaded.filename)

    if not filename:
        return render_template(
            "index.html",
            error="Please choose a valid image file."
        )

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    uploaded.save(file_path)

    image = cv2.imread(file_path)

    if image is None:
        return render_template(
            "index.html",
            error="The uploaded file is not a readable image."
        )

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(image)

    if data:
        save_history("Detected", data)
        
        return render_template(
            "index.html",
            detection_result=data
        )

    return render_template(
        "index.html",
        error="QR code not detected. Try a clearer image."
    )


if __name__ == "__main__":
    app.run(debug=True)