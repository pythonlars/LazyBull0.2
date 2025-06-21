from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import shutil
import os
import datetime
from dotenv import load_dotenv

# Import the analysis function from main.py
import main

# Load environment variables so GOOGLE_API_KEY is available
load_dotenv()

app = FastAPI(title="Gemini Image Analyzer")

# Allow requests from the Chrome extension (or any origin running on the user machine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """Receive an image file, run Gemini analysis, and return the result."""
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    # Save a copy with the conventional screenshot name so it is available later
    screenshot_name = f"Screenshot {datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')}.png"
    shutil.copyfile(temp_path, screenshot_name)

    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not set in environment")

        result = main.analyze_image_with_gemini(api_key, temp_path)
        return JSONResponse({"result": result, "screenshot": screenshot_name})
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
