from gemini import coder_model
from utils import write_code


def generate_and_write_code(prompt: str) -> dict:
    """
    Generate code for a given prompt and write it to the active text editor.
    Args:
        prompt (str): The prompt to generate code from.
    """
    print("Coder called!")
    print(prompt)
    code = coder_model.generate(prompt).model_dump()['parsed']['code']
    write_code(code)
    return {"message": "Done"}
