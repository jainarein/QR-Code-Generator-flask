from flask import Flask, render_template, request, send_file
import qrcode
from qrcode.constants import ERROR_CORRECT_H
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        
        # 🔵 Get custom colors from the form (with defaults)
        fill = request.form.get("fill_color", "black")
        back = request.form.get("back_color", "white")

        # 🔵 Generate QR code with colors
        qr = qrcode.QRCode(
            error_correction=ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill, back_color=back)

        # 🔽 Save to buffer for download
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return send_file(buffer, mimetype="image/png", as_attachment=True, download_name="qr.png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
