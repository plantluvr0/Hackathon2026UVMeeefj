import os
from google import genai
from google.genai import types
from pydantic import BaseModel

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

def gemini_call(message):
    #set up client
    client = genai.Client(api_key=os.getenv(API_KEY))
    config = types.GenerateContentConfig(
        #set the system message
        system_instruction="you are a healthcare professional who works in a hospital"
                           "who fills out admission and dismissal forms for patients",
        #response type
        response_mime_type = "application/json",
        #schema
        response_schema=Patient,
        temperature=0.8,
        max_output_tokens=500
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[message],
        config=config
    )

    if response.ok:
        return response.parsed
    else:
        #maybe throw something
        print("Api call failed")
        raise Exception()