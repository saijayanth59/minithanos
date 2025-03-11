from gemini import coder_model
from gui_utils import write_text

def write_code(prompt):
    code = coder_model.generate(prompt).model_dump()['parsed']['code']
    write_text(code)
        
write_code("write code for trapping rain water")

