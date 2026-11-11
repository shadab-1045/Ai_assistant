
import os

start_sequence=" \033[90m"
end_sequence="\033[0m"
def log(text):
    """Print a dim debug message only when DEBUG is enabled in the environment."""
    if(os.getenv("DEBUG")=="True"):
        print(f" {start_sequence}{text}{end_sequence}")