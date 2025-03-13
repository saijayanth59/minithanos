from gemini import shortcutter_model
from gui_utils import press_shortcut

def get_shortcut_and_do(prompt):
    shortcut = shortcutter_model.generate(prompt).model_dump()["parsed"]["shortcut"]
    press_shortcut(shortcut)
