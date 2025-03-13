from gemini import commander_model
import subprocess


def run_command(prompt: str) -> None:
    """
    Generate a command for a given prompt and run it in the terminal.
    Args:
        prompt (str): The prompt to generate a command from.
    """
    for _ in range(3):
        command = commander_model.generate(prompt)
        output = subprocess.run([r"C:\Program Files\Git\bin\bash.exe", "-c", command], shell=True, capture_output=True)
        if output.stderr != b'':
            continue
        break 
