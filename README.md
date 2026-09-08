# Split Bill AI

An AI-powered restaurant bill splitting application.

## Features

- Upload a restaurant bill image
- Extract bill information using Gemini Vision
- Extract items, quantities, prices, taxes, discounts and service charges
- Human review and correction of extracted information
- Add multiple people
- Assign items to people
- Support equal and proportional item splitting
- Distribute taxes and service charges proportionally
- Detect total mismatches and normal rounding differences

## Architecture

React frontend → FastAPI backend → Gemini Vision → Pydantic validation → deterministic calculation engine

## Tech Stack

- React
- Vite
- FastAPI
- Python
- Gemini API
- Pydantic

## Running Locally

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload