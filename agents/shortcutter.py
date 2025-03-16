from gemini import shortcutter_model
from utils import press_shortcut

def perform_shortcut(prompt: str) -> dict:
    """
    Generate a shortcut for a given prompt and press it.
    Args:
        prompt (str): The prompt to generate a shortcut from.
    Returns:
        dict: The result of the operation
    """
    print("Shortcutter called!")
    print("Prompt: " + prompt)
    shortcut = shortcutter_model.generate(prompt).model_dump()["parsed"]["shortcut"]
    print(shortcut)
    press_shortcut(shortcut)
    return {"result": "Done"}
