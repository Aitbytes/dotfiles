---
name: glm-ocr
description: Perform OCR on PDFs and images using GLM-OCR via ZAI API. Extract text, tables, and layout information with high accuracy.
license: MIT
compatibility: opencode
metadata:
  audience: document-processing-agents
  workflow: ocr
---

## What I do

- Convert PDFs or images to markdown/text using GLM-OCR (ZAI API)
- Preserve document structure (headers, paragraphs, tables)
- Extract multilingual text including handwriting support
- Return structured output with bounding boxes and layout info
- Process files locally using base64 encoding (no file upload needed)

## When to use me

Use this skill when you need to:

- Extract text from a PDF document
- OCR scanned documents or images
- Parse complex layouts with tables and mixed content
- Extract text in multiple languages (supports EN, FR, AR, ZH, JP, DE, ES, etc.)
- Get structured output with layout/bounding box information

## Requirements

- `ZAI_API_KEY` environment variable must be set
- Use `uv run --with zai-sdk,pymupdf python3` to run scripts
- PDF files or images (JPG, PNG)

## How to use

### Basic PDF OCR (single page)

```bash
uv run --with zai-sdk,pymupdf python3 - << 'EOF'
import fitz
import base64
import os
from zai import ZaiClient

pdf_path = "/path/to/document.pdf"
output_path = "/path/to/output.md"

client = ZaiClient(api_key=os.environ["ZAI_API_KEY"])

doc = fitz.open(pdf_path)
page = doc[0]
mat = fitz.Matrix(150/72, 150/72)
pix = page.get_pixmap(matrix=mat)
img_bytes = pix.tobytes("png")
doc.close()

img_b64 = base64.b64encode(img_bytes).decode()

resp = client.layout_parsing.create(
    model="glm-ocr",
    file=f"data:image/png;base64,{img_b64}"
)

with open(output_path, "w") as f:
    f.write(resp.md_results)

print(f"OCR output written to {output_path}")
EOF
```

### Process entire PDF (all pages)

```bash
uv run --with zai-sdk,pymupdf python3 - << 'EOF'
import fitz
import base64
import os
from zai import ZaiClient

pdf_path = "/path/to/document.pdf"
output_path = "/path/to/output.md"

client = ZaiClient(api_key=os.environ["ZAI_API_KEY"])
doc = fitz.open(pdf_path)

all_text = []
for page_num in range(len(doc)):
    page = doc[page_num]
    mat = fitz.Matrix(150/72, 150/72)
    pix = page.get_pixmap(matrix=mat)
    img_bytes = pix.tobytes("png")
    img_b64 = base64.b64encode(img_bytes).decode()

    resp = client.layout_parsing.create(
        model="glm-ocr",
        file=f"data:image/png;base64,{img_b64}"
    )
    all_text.append(f"--- Page {page_num + 1} ---\n{resp.md_results}")

doc.close()

with open(output_path, "w") as f:
    f.write("\n\n".join(all_text))

print(f"OCR output written to {output_path}")
EOF
```

### Process multiple PDFs to individual markdown files

```bash
uv run --with zai-sdk,pymupdf python3 - << 'EOF'
import fitz
import base64
import os
from zai import ZaiClient
from pathlib import Path

input_dir = Path("/path/to/pdfs")
output_dir = Path("/path/to/output")

client = ZaiClient(api_key=os.environ["ZAI_API_KEY"])
output_dir.mkdir(parents=True, exist_ok=True)

for pdf_file in sorted(input_dir.glob("*.pdf")):
    output_file = output_dir / f"{pdf_file.stem}.md"

    print(f"Processing {pdf_file.name}...")
    doc = fitz.open(pdf_file)

    all_text = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        mat = fitz.Matrix(150/72, 150/72)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        img_b64 = base64.b64encode(img_bytes).decode()

        resp = client.layout_parsing.create(
            model="glm-ocr",
            file=f"data:image/png;base64,{img_b64}"
        )
        all_text.append(f"--- Page {page_num + 1} ---\n{resp.md_results}")

    doc.close()

    with open(output_file, "w") as f:
        f.write("\n\n".join(all_text))

    print(f"  -> {output_file}")

print("Done")
EOF
```

### Process image file (JPG, PNG)

```bash
uv run --with zai-sdk,pymupdf python3 - << 'EOF'
import base64
import os
from zai import ZaiClient

image_path = "/path/to/image.jpg"
output_path = "/path/to/output.md"

client = ZaiClient(api_key=os.environ["ZAI_API_KEY"])

with open(image_path, "rb") as f:
    img_bytes = f.read()

img_b64 = base64.b64encode(img_bytes).decode()

resp = client.layout_parsing.create(
    model="glm-ocr",
    file=f"data:image/png;base64,{img_b64}"
)

with open(output_path, "w") as f:
    f.write(resp.md_results)

print(f"OCR output written to {output_path}")
EOF
```

## Output format

The `LayoutParsingResp` contains:

| Field            | Description                                     |
| ---------------- | ----------------------------------------------- |
| `id`             | Task ID                                         |
| `created`        | Unix timestamp                                  |
| `model`          | Model name (glm-ocr)                            |
| `md_results`     | Markdown formatted text                         |
| `layout_details` | List of detected elements with bbox coordinates |
| `data_info`      | Page dimensions and page count                  |
| `usage`          | Token usage statistics                          |

Each `LayoutDetail` contains:

- `label`: element type ('text', 'image', etc.)
- `bbox_2d`: bounding box [x1, y1, x2, y2]
- `content`: text content (for text elements)
- `height`, `width`: page dimensions

## Limitations

- Image/PDF size limit: 10MB per image, 50MB per PDF
- Max 100 pages per PDF
- Requires valid ZAI API key
- For very large PDFs, process page by page to avoid timeouts

## Pricing

GLM-OCR via ZAI API costs ~$0.03 per million tokens (very affordable for document OCR).
