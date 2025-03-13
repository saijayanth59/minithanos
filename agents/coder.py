from gemini import coder_model
from gui_utils import write_text


def write_code(prompt: str) -> None:
    """
    Generate code for a given prompt and write it to the active text editor.
    Args:
        prompt (str): The prompt to generate code from.
    """
    code = coder_model.generate(prompt).model_dump()['parsed']['code']
    write_text(code)
