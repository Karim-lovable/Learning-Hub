# PDF Render Service for IGCSE Grading

A lightweight Flask service that renders PDF pages to PNG images via PyMuPDF.

## Endpoints

### POST /render
Renders PDF pages to base64-encoded PNGs.

**Request:**
```json
{
  "pdf_url": "https://example.com/file.pdf",
  "pages": [1, 2, 3]
}
```

**Response:**
```json
{
  "images": {
    "1": "iVBORw0KGgo...",
    "2": "iVBORw0KGgo...",
    "3": "iVBORw0KGgo..."
  }
}
```

### GET /health
Health check for Railway monitoring.

## Deployment to Railway

1. Create a new Railway project
2. Connect this GitHub repo or use "New" → "Empty Project"
3. Railway auto-detects Python from `requirements.txt`
4. Set environment variables (if needed):
   - `PORT` (Railway sets this automatically)
5. Deploy — Railway provides a public URL like `https://your-service.up.railway.app`

## Local Testing

```bash
pip install -r requirements.txt
python main.py
# Service runs on http://localhost:5000

curl -X POST http://localhost:5000/render \
  -H "Content-Type: application/json" \
  -d '{"pdf_url":"https://www.africau.edu/images/default/sample.pdf","pages":[1]}'
```
