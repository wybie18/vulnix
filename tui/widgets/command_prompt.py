from textual import events
from textual.message import Message
from textual.widgets import TextArea


class CommandPrompt(TextArea):
    """Multiline command prompt: Enter submits, Shift+Enter inserts newline."""

    class Submitted(Message):
        """Posted when user submits command text."""

        def __init__(self, sender: "CommandPrompt", value: str) -> None:
            self.value = value
            super().__init__()

    def __init__(self, placeholder: str = "", model_info: str = "", **kwargs):
        super().__init__(placeholder=placeholder, **kwargs)
        self.model_info = model_info

    def on_mount(self) -> None:
        self.border_title = "[ COMMAND ]"
        self.show_line_numbers = False
        
        # Set bottom subtitle if model_info is provided
        if self.model_info:
            self.border_subtitle = self.model_info

    def on_key(self, event: events.Key) -> None:
        if event.key == "shift+enter":
            self.insert("\n")
            event.stop()
            return

        if event.key == "enter":
            value = self.text.strip()
            if value:
                self.post_message(self.Submitted(self, value))
            self.clear()
            event.stop()
    
    def watch_text(self, new_text: str) -> None:
        line_count = max(1, new_text.count('\n') + 1)
        max_lines = 10
        height = min(line_count + 2, max_lines + 2)
        self.styles.height = height
