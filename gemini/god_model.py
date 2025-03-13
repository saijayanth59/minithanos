from .client import client
from google.genai import types
from agents.all_functions import all_functions

base_prompt = """
You are god.
Please know your tools.
If I want to talk to you, please talk to me back in a friendly manner.
If I want you to do a task. Please do it using your tools.
Give appropriate arguments to appropriate tools.
"""

def generate(prompt):
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=2,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""give short responses like in a chat"""),
        ],
        tools=all_functions
    )

    return client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

if __name__ == "__main__":
    generate()
