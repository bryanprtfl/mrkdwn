from flask import Flask, request, jsonify
import tempfile
import os
import traceback

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Lazy-load MarkItDown so cold starts don't fail on import errors
# ---------------------------------------------------------------------------
def get_markitdown():
    from markitdown import MarkItDown
    return MarkItDown()


# ---------------------------------------------------------------------------
# CORS helper
# ---------------------------------------------------------------------------
def _cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.after_request
def after_request(response):
    return _cors(response)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "markitdown-api",
        "endpoints": {
            "POST /api/convert/url":  "Converti un URL in Markdown",
            "POST /api/convert/file": "Converti un file uploadato in Markdown (multipart/form-data, campo: file)",
        }
    })


@app.route("/api/convert/url", methods=["POST", "OPTIONS"])
def convert_url():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    body = request.get_json(silent=True) or {}
    url = body.get("url", "").strip()

    if not url:
        return jsonify({"error": "Campo 'url' mancante o vuoto"}), 400

    try:
        md = get_markitdown()
        result = md.convert(url)
        return jsonify({
            "success": True,
            "source": url,
            "markdown": result.text_content,
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "detail": traceback.format_exc(),
        }), 500


@app.route("/api/convert/file", methods=["POST", "OPTIONS"])
def convert_file():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    if "file" not in request.files:
        return jsonify({"error": "Nessun file inviato. Usa multipart/form-data con il campo 'file'"}), 400

    uploaded = request.files["file"]
    filename = uploaded.filename or "upload"

    # Salva in un file temporaneo mantenendo l'estensione
    _, ext = os.path.splitext(filename)
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            uploaded.save(tmp.name)
            tmp_path = tmp.name

        md = get_markitdown()
        result = md.convert(tmp_path)

        return jsonify({
            "success": True,
            "filename": filename,
            "markdown": result.text_content,
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "detail": traceback.format_exc(),
        }), 500
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Vercel entry point
# ---------------------------------------------------------------------------
# Vercel cerca una variabile chiamata `app` (o `handler`) nel modulo
# Nessun `if __name__ == "__main__"` necessario per il deploy
