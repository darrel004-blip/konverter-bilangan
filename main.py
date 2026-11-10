# Web InterFace
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from process import *
import json

BASE_DIR = Path(__file__).resolve().parent
CONVERTER_CLASSES = {
    "decimal": Decimal,
    "binary": Binary,
    "octal": Octal,
    "hexadecimal": HexaDecimal
}

class ConverterHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if urlparse(self.path).path != "/api/convert":
            self.send_json({"success": False, "error": "Endpoint tidak ditemukan."}, 404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > 4096:
                self.send_json({"success": False, "error": "Input tidak sesuai dengan aturan."}, 400)
                return

            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            selected_base = payload.get("base")
            raw_value = payload.get("value")

            if selected_base not in CONVERTER_CLASSES or not isinstance(raw_value, str) or raw_value == "":
                self.send_json({"success": False, "error": "Pilih basis dan masukkan angka terlebih dahulu."}, 400)
                return

            converter = CONVERTER_CLASSES[selected_base](raw_value)
            results = converter.output()

            if not results:
                self.send_json({"success": False, "error": "Input tidak sesuai dengan aturan basis yang dipilih."}, 400)
                return

            self.send_json({
                "success": True,
                "source_base": selected_base,
                "source_value": converter.raw,
                "results": results
            })
        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            self.send_json({"success": False, "error": "Input tidak sesuai dengan aturan basis yang dipilih."}, 400)
        except Exception:
            self.send_json({"success": False, "error": "Terjadi kesalahan saat melakukan konversi."}, 500)


def main():
    address = ("127.0.0.1", 8000)
    server = ThreadingHTTPServer(address, ConverterHandler)
    print("Number Converter berjalan di http://127.0.0.1:8000")
    print("Tekan Ctrl+C untuk menghentikan server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
