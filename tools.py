from agents.coder import generate_and_write_code
from agents.shortcutter import perform_shortcut
from agents.spotify import play_song
from agents.commander import run_command
from utils import write_text

FUNCTIONS = {
    "generate_and_write_code": generate_and_write_code,
    "run_command": run_command,
    "perform_shortcut": perform_shortcut,
    "play_song": play_song,
    "write_text": write_text
}
