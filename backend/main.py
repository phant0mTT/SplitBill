from fastapi import FastAPI
from models import SplitRequest
from services.calc import calculate_split

app = FastAPI(title="Split Bill AI")


@app.get("/")
def root():
    return {
        "message": "Split Bill AI API is running"
    }


@app.post("/calculate-split")
def calculate(request: SplitRequest):

    result = calculate_split(
        request.bill,
        request.assignments
    )

    return {
        "breakdown": result
    }