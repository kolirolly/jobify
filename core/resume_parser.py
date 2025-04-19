import pymupdf4llm
import io
import tempfile
import fitz

async def extract_text(file):
    file_bytes = await file.read()
    # Save to a temp file
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp.flush()  # Ensure it's written to disk
        markdown = pymupdf4llm.to_markdown(tmp.name)
    return markdown
