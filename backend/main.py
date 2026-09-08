from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models import SplitRequest
from services.calc import calculate_split
from services.bill_ext import extract_bill

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
async def extract_bill_endpoint(
    file: UploadFile = File(...)
):

    try:

        image_bytes = await file.read()

        bill = await extract_bill(
            image_bytes,
            file.content_type
        )

        return {
            "success": True,
            "bill": bill.model_dump()
        }

    except Exception as error:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(error)
            }
        )

@app.post("/calculate-split")
def calculate(request: SplitRequest):
    try:
        result = calculate_split(
            request.bill,
            request.assignments
        )

        return {
            "success": True,
            "result": result
        }

    except ValueError as error:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": str(error)
            }
        )