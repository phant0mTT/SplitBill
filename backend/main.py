from fastapi import FastAPI
from fastapi.responses import JSONResponse

from models import SplitRequest
from services.calc import calculate_split


app = FastAPI(
    title="Split Bill AI"
)


@app.get("/")
def root():
    return {
        "message": "Split Bill AI API is running"
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