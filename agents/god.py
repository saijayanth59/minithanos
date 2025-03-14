from gemini import god_model


def do(prompt):
    return god_model.generate(prompt).text
