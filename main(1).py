from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import requests
import base64
import io

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Railway monitoring."""
    return jsonify({"status": "ok"}), 200

@app.route("/render", methods=["POST"])
def render_pdf():
    """
    Render PDF pages to PNG images.
    
    Request body:
    {
        "pdf_url": "https://.../file.pdf",
        "pages": [1, 2, 3]  // optional, empty = all pages
    }
    
    Response:
    {
        "images": {
            "1": "base64encodedpng...",
            "2": "base64encodedpng..."
        }
    }
    """
    try:
        data = request.get_json()
        if not data or "pdf_url" not in data:
            return jsonify({"error": "pdf_url is required"}), 400
        
        pdf_url = data["pdf_url"]
        pages = data.get("pages", [])  # Empty list = render all pages
        
        # Download PDF
        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()
        pdf_bytes = response.content
        
        # Open with PyMuPDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Determine which pages to render
        if pages:
            # Validate page numbers
            page_numbers = [p for p in pages if 1 <= p <= doc.page_count]
        else:
            # Render all pages
            page_numbers = list(range(1, doc.page_count + 1))
        
        # Render each page at 150 DPI (good balance of quality vs size)
        images = {}
        for page_num in page_numbers:
            page = doc.load_page(page_num - 1)  # 0-indexed
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            images[str(page_num)] = base64.b64encode(img_bytes).decode('utf-8')
        
        doc.close()
        
        return jsonify({"images": images}), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to download PDF: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Rendering failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
