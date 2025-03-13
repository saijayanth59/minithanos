from gemini import commander_model
import subprocess


def run_command(task: str) -> None:
    """
    Can do any task which involves running a terminal command. From opening a file to running a script.
    Generate a terminal command for a given task.
    Args:
        task (str): The prompt to generate a command from.
    """
    for _ in range(3):
        command = commander_model.generate(task)
        output = subprocess.run([r"C:\Program Files\Git\bin\bash.exe", "-c", command], shell=True, capture_output=True)
        if output.stderr != b'':
            continue
        break 
