from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal, Middle, Vertical
from textual.screen import Screen
from textual.widgets import Static

from ..widgets import CommandPrompt


class WelcomeScreen(Screen):
    """Welcome screen with centered prompt and branding."""
    
    CSS = """
    WelcomeScreen {
        align: center middle;
    }
    
    #welcome-content {
        width: 80;
        height: auto;
        align: center middle;
    }

    #welcome-title {
        width: 100%;
        height: auto;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        text-align: center;
        margin-bottom: 2;
    }

    #welcome-prompt {
        width: 100%;
        height: auto;
        min-height: 4;
        max-height: 13;
        border: none;
        border-left: outer $accent;
        background: $surface;
        color: $text;
        text-style: bold;
        padding: 1 1 2 1;

        scrollbar-background: transparent;
        scrollbar-color: $panel-lighten-1;
        scrollbar-color-hover: $panel-lighten-2;
        scrollbar-color-active: $panel-lighten-3;
        scrollbar-corner-color: transparent;
        scrollbar-size: 1 1;
    }

    #welcome-prompt:focus {
        border: none;
        border-left: outer $accent;
    }

    #welcome-info {
        offset-y: -2;
        width: 100%;
        height: auto;
        align: center middle;
        background: $surface;
        border: none;
        border-left: outer $accent;
    }

    #welcome-prompt-info {
        width: 1fr;
        height: auto;
        padding: 1 0 1 1;
    }

    #welcome-commands {
        width: auto;
        height: auto;
        text-align: right;
        padding: 1 1 1 0;
    }

    #welcome-tip {
        width: 1fr;
        height: auto;
        color: $text-muted;
        text-align: center;
        padding: 0 2 0 0;
        offset-y: -1;
    }
    """
    
    def __init__(self, ascii_art: str, model: str, provider: str):
        super().__init__()
        self.ascii_art = ascii_art
        self.model = model
        self.provider = provider
    
    def compose(self) -> ComposeResult:
        with Container():
            with Center():
                with Middle():
                    with Vertical(id="welcome-content"):
                        yield Static(self.ascii_art, id="welcome-title")
                        yield CommandPrompt(placeholder="Ask anything...", id="welcome-prompt")
                        with Horizontal(id="welcome-info"):
                            yield Static(
                                f"[bold $text-primary]{self.model}[/] [dim]{self.provider}[/]",
                                id="welcome-prompt-info"
                            )
                            yield Static(
                                "ctrl+q [dim]quit[/]  ctrl+p [dim]commands[/]",
                                id="welcome-commands"
                            )
                        yield Static(
                            "Tip: Try commands like 'scan repo' or 'show scope'",
                            id="welcome-tip"
                        )
