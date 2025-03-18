import base64
from PIL import Image
from io import BytesIO
from gemini.screenshot import take_screenshot
from gemini.client import client
from google.genai import types

def resize_image(image_data, max_size=(800, 800)):
    """
    Resize the image to ensure it does not exceed the maximum size.

    Args:
        image_data (bytes): The original image data.
        max_size (tuple): The maximum width and height for the resized image.

    Returns:
        bytes: The resized image data.
    """
    image = Image.open(BytesIO(image_data))
    image.thumbnail(max_size)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()

def generate_description(image_data):
    """
    Generate a description for the given image data using the Gemini model.

    Args:
        image_data (bytes): The image data to be described.

    Returns:
        dict: The response from the Gemini model containing the description.
    """
    model = "gemini-2.0-flash"
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    prompt = "Could you please describe what you see in the following image? If the image has text give comment on the text. If the image contains code, kindly explain what the code is about. If there are pictures, provide a detailed description of all the elements and images present. Please be clear and specific in your description."
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
                types.Part.from_text(text=image_base64),
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
            types.Part.from_text(text="""give short responses like in a chat"""),
        ],
    )

    return client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

def describe_screenshot():
    """
    Take a screenshot, resize it if necessary, and generate a description for it.

    Returns:
        dict: The response from the Gemini model containing the description.
    """
    screenshot_path = take_screenshot()
    with open(screenshot_path, "rb") as image_file:
        image_data = image_file.read()
    
    # Resize image if token size exceeds limit
    image_data = resize_image(image_data)
    
    response = generate_description(image_data)
    return response

if __name__ == "__main__":
    description = describe_screenshot()
    print(description)
