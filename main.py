from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

PDF_FILE = Path(__file__).resolve().parent / "portfolio.pdf"

@app.get("/")
def get_pdf():
    return FileResponse(
        path=PDF_FILE,
        media_type="application/pdf",
        filename="portfolio.pdf"
    )
