from google import genai
from google.genai import types

def gemini_call(message):
    #set up client
    client = genai.Client(api_key="AIzaSyDniPDJEUeWjH6qWM2jpBBcLTB9zz_6mzc")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message,
    )

    return response.text


print(gemini_call("heyyyyyyy"))
