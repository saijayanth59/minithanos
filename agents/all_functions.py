from agents.coder import write_code
from agents.commander import run_command
from agents.shortcutter import perform_shortcut
from agents.spotify import play_song

all_functions = {
    "write_code": write_code,
    "run_command": run_command,
    "perform_shortcut": perform_shortcut,
    "play_song": play_song,
}