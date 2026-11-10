from pathlib import Path
import os

from flask import Flask, jsonify, request, send_file

from process import Decimal, Binary, Octal, HexaDecimal

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "konverter_bilangan.html"

app = Flask(__name__)

CONVERTER_CLASSES = {
    "decimal": Decimal,
    "binary": Binary,
    "octal": Octal,
    "hexadecimal": HexaDecimal,
}


@app.get("/")
def home():
    if not HTML_FILE.is_file():
        return "File konverter_bilangan.html tidak ditemukan.", 404
    return send_file(HTML_FILE, mimetype="text/html")


@app.post("/api/convert")
def convert():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "error": "Permintaan tidak valid. Data harus berformat JSON.",
        }), 400

    selected_base = payload.get("base")
    raw_value = payload.get("value")

    if selected_base not in CONVERTER_CLASSES or not isinstance(raw_value, str) or not raw_value:
        return jsonify({
            "success": False,
            "error": "Pilih basis dan masukkan angka terlebih dahulu.",
        }), 400

    if len(raw_value) > 4096:
        return jsonify({
            "success": False,
            "error": "Input terlalu panjang.",
        }), 400

    try:
        converter = CONVERTER_CLASSES[selected_base](raw_value)
        results = converter.output()

        if not results:
            return jsonify({
                "success": False,
                "error": "Input tidak sesuai dengan aturan basis yang dipilih.",
            }), 400

        return jsonify({
            "success": True,
            "source_base": selected_base,
            "source_value": converter.raw,
            "results": results,
        })
    except (ValueError, TypeError, KeyError):
        return jsonify({
            "success": False,
            "error": "Input tidak sesuai dengan aturan basis yang dipilih.",
        }), 400
    except Exception:
        app.logger.exception("Kesalahan saat melakukan konversi")
        return jsonify({
            "success": False,
            "error": "Terjadi kesalahan saat melakukan konversi.",
        }), 500


if __name__ == "__main__":
    # Untuk pengujian lokal. Vercel akan mengimpor objek `app` secara langsung.
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False)
