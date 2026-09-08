import os
import base64

from dotenv import load_dotenv
from google import genai

from models import Bill


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


PROMPT = """
You are a restaurant bill extraction system.

Analyze the provided bill image and extract the information exactly as printed.

Rules:
1. Extract every food and drink line item.
2. Extract the quantity.
3. IMPORTANT: `price` must represent the PRE-TAX amount
   for that line item.
4. Calculate the pre-tax item amount as:
   Rate × Quantity.
5. Do NOT use the TOTAL column as `price` when that column
   includes tax.
6. Extract the printed subtotal.
7. Combine CGST, SGST, VAT, S.Tax and similar taxes into `tax`.
8. Only use `service_charge` when the bill explicitly contains
   a restaurant/service charge.
9. Extract discounts if present.
10. Extract the final printed total.
11. Do not invent missing values.
12. Preserve the printed total even if the arithmetic appears incorrect.
13. Do not correct or modify printed amounts.
14. Give every item a confidence score between 0 and 1.
15. Ignore restaurant address, phone number, GSTIN, invoice number
    and other non-calculation information.

The output must strictly follow the provided schema.
"""


async def extract_bill(image_bytes: bytes, mime_type: str) -> Bill:

    image_base64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    response = client.models.generate_content(
        model="gemini-3.5-flash",

        contents=[
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_base64
                }
            },
            PROMPT
        ],

        config={
            "response_mime_type": "application/json",
            "response_schema": Bill
        }
    )

    bill = Bill.model_validate_json(response.text)

    for index, item in enumerate(bill.items, start=1):
        item.id = index

    return bill