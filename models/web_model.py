from google import genai
from google.genai import types
import json


def get_xpath(rawHtml, element):
    client = genai.Client(api_key="AIzaSyAkSmvQGTAMQblIWJPT0ufPzr7vFLgmJog")
    model = "gemini-2.0-flash"
    config = types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema={
            'required': [
                'xpath'
            ],
            'properties': {
                'xpath': {'type': 'STRING', 'description': 'The exact XPath of the specified UI element in the DOM.'},
            },
            'type': 'OBJECT',
            'description': 'Extracts the exact XPath of a UI element based on the provided raw HTML and description.',
        })
    response = client.models.generate_content(
        model=model,
        contents=["I will give the raw html and description of the ui element give me exact the xpath",
                  f"UI element: {element}\n", f"Raw html: {rawHtml}\n"],
        config=config
    ).text
    return json.loads(response)
