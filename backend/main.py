from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models import SplitRequest
from services.calc import calculate_split


app = FastAPI(
    title="Split Bill AI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Split Bill AI API is running"
    }

@app.post("/extract-bill")
async def extract_bill(file: UploadFile = File(...)):

    image_data = await file.read()

    return {
        "filename": file.filename,
        "size": len(image_data)
    }

@app.post("/calculate-split")
def calculate(request: SplitRequest):

    try:

        breakdown = calculate_split(
            request.bill,
            request.assignments
        )

        return {
            "success": True,
            "breakdown": breakdown
        }

    except ValueError as error:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": str(error)
            }
        )