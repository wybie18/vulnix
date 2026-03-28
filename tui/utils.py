from datetime import datetime
from textual.widgets import RichLog
import textwrap

SEV_COLORS = {
    "SYSTEM":  "green",
    "AGENT":   "cyan",
    "TRACE":   "bright_cyan",
    "DAST":    "yellow",
    "SAST":    "red",
    "SECRETS": "yellow",
    "FUZZ":    "magenta",
    "NET":     "cyan",
    "FIX":     "green",
    "REPORT":  "white",
    "USER":    "blue",
    "ERROR":   "red",
}

ASCII_ART = r"""

 ██▒   █▓ █    ██  ██▓     ███▄    █  ██▓▒██   ██▒
▓██░   █▒ ██  ▓██▒▓██▒     ██ ▀█   █ ▓██▒▒▒ █ █ ▒░
 ▓██  █▒░▓██  ▒██░▒██░    ▓██  ▀█ ██▒▒██▒░░  █   ░
  ▒██ █░░▓▓█  ░██░▒██░    ▓██▒  ▐▌██▒░██░ ░ █ █ ▒ 
   ▒▀█░  ▒▒█████▓ ░██████▒▒██░   ▓██░░██░▒██▒ ▒██▒
   ░ ▐░  ░▒▓▒ ▒ ▒ ░ ▒░▓  ░░ ▒░   ▒ ▒ ░▓  ▒▒ ░ ░▓ ░
   ░ ░░  ░░▒░ ░ ░ ░ ░ ▒  ░░ ░░   ░ ▒░ ▒ ░░░   ░▒ ░
     ░░   ░░░ ░ ░   ░ ░      ░   ░ ░  ▒ ░ ░    ░  
      ░     ░         ░  ░         ░  ░   ░    ░  
     ░                                            

"""

def log_message(richlog: RichLog, tag: str, message: str) -> None:
    color = SEV_COLORS.get(tag, "cyan")
    ts = datetime.now().strftime("%H:%M:%S")
    
    prefix = f"[dim]{ts}[/]  [bold {color}]{tag:<8}[/]  "
    indent_width = 20
    
    wrapper = textwrap.TextWrapper(
        width=richlog.content_size.width - 1 if richlog.content_size.width > 0 else 80,
        initial_indent="",
        subsequent_indent=" " * indent_width
    )
    
    wrapped_lines = wrapper.wrap(message)
    
    if not wrapped_lines:
        richlog.write(prefix)
        return

    richlog.write(f"{prefix}{wrapped_lines[0]}")
    
    for line in wrapped_lines[1:]:
        richlog.write(line)