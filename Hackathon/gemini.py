import os
from google import genai
from google.genai import types

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
        response_schema={
            "type": "Admission",
            "properties": {
                "answer": {"type": "STRING"},
                "confidence_score": {"type": "NUMBER"}
            }
        },
        temperature=0.8,
        max_output_tokens=500
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[message],
        config=config
    )

    if response.ok:
        return response.content
    else:
        #maybe throw something
        print("Api call failed")
        raise Exception()