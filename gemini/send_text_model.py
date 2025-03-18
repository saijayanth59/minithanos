import pyperclip
import pyautogui
import time
from gemini.client import client
from google.genai import types


def generate_text_overview(selected_text):
    """
    Generate an overview for the given selected text using the Gemini model.

    Args:
        selected_text (str): The text to be summarized.

    Returns:
        dict: The response from the Gemini model containing the overview.
    """
    model = "gemini-2.0-flash"
    prompt = f"Could you please provide an overview of the following text: {selected_text}"
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
        max_output_tokens=1200,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(
                text="""give short responses like in a chat"""),
        ],
    )

    return client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )


def describe_text():
    """
    Copy the selected text using pyautogui, get it from the clipboard, send it to the Gemini model, and get an overview.

    Returns:
        dict: The response from the Gemini model containing the overview.
    """
    time.sleep(5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    selected_text = pyperclip.paste()
    response = generate_text_overview(selected_text)
    return response


if __name__ == "__main__":
    overview = describe_text()
    print(overview)
