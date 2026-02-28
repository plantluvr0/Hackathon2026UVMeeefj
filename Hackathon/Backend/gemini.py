import os
import time
import logging
from google import genai
from google.genai import types
from pydantic import BaseModel

# require API key to be present in environment; make variable global for reuse
API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Gemini API key not found; set GEMINI_API_KEY or GOOGLE_API_KEY in environment")

class Patient(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    dob: str
    phone_number: str
    date: str
    diagnosis: str
    room_number: int
    insurance: str
    primary_symptoms_summary: str

def gemini_call(message, max_retries: int = 3, backoff_factor: float = 2.0):
    """Send a request to the Gemini model and handle rate‑limiting (429) by retrying.

    Args:
        message: The prompt to send to the model.
        max_retries: how many times to retry after receiving a 429.
        backoff_factor: exponential backoff base.

    Returns:
        Parsed response object on success.

    Raises:
        RuntimeError on any non-recoverable error.
    """

    client = genai.Client(api_key=API_KEY)
    config = types.GenerateContentConfig(
        # set the system message
        system_instruction=(
            "you are a healthcare professional who works in a hospital "
            "who fills out admission and dismissal forms for patients"
        ),
        # response type
        response_mime_type="application/json",
        # schema
        response_schema=Patient,
        temperature=0.8,
        max_output_tokens=500,
    )

    attempt = 0
    while True:
        attempt += 1
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[message],
            config=config,
        )

        if response.ok:
            return response.parsed

        status = getattr(response, "status_code", None)
        if status == 429 and attempt <= max_retries:
            sleep_time = backoff_factor ** attempt
            logging.warning(
                f"Gemini API rate limited (429) – retry {attempt}/{max_retries} after {sleep_time}s"
            )
            time.sleep(sleep_time)
            continue

        logging.error(f"Gemini API call failed (status={status}) {response}")
        raise RuntimeError("Gemini API call failed: " + str(response))