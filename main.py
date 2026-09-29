from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

PDF_FILE = Path(__file__).resolve().parent / "General Attendance Report (18).pdf"

@app.get("/")
def get_pdf():
    return FileResponse(
        path=PDF_FILE,
        media_type="application/pdf",
        filename="portfolio.pdf"
    )
