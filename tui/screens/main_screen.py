from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, RichLog, Static
from typing import Optional

from ..database import Session, MessageManager
from ..utils import log_message
from ..widgets import ActiveContext, AgentBrain, CommandPrompt, LootReport


class MainScreen(Screen):
    """Main conversation screen with panels and logs."""
    
    CSS = """
    MainScreen {
        layout: vertical;
    }
    
    #app-header {
        margin-bottom: 1;
    }
    
    #app-footer {
        margin-top: 1;
    }
    
    #main-container {
        layout: vertical;
        width: 100%;
        height: 100%;
        padding: 0 1;
    }
    
    #main-content {
        height: 1fr;
        margin: 0 0 1 0;
    }
    
    .pane {
        background: $surface;
        padding: 1 1;
        margin: 0 1 0 0;
        transition: border 300ms, border-title-color 300ms;
    }
    
    .pane:focus-within {
        border: round $accent;
        border-title-color: $text-accent;
    }
    
    #left-pane {
        width: 60%;
        height: 100%;
        border: round $primary;
        border-title-color: $text-primary;
        border-title-style: bold;
    }
    
    #right-column {
        width: 40%;
        height: 100%;
        layout: vertical;
    }
    
    #top-right-pane {
        height: 37%;
        margin: 0 0 1 0;
        border: round $secondary;
        border-title-color: $text-secondary;
        border-title-style: bold;
        border-title-align: right;
    }
    
    #bottom-right-pane {
        height: 63%;
        margin: 0;
        border: round $success;
        border-title-color: $text-success;
        border-title-style: bold;
        border-title-align: right;
    }
    
    #command-prompt {
        width: 100%;
        height: auto;
        min-height: 3;
        max-height: 12;
        border: none;
        border-left: outer $primary;
        background: $surface;
        color: $text;
        text-style: bold;
        padding: 1;
        
        scrollbar-background: transparent;
        scrollbar-color: $panel-lighten-1;
        scrollbar-color-hover: $panel-lighten-2;
        scrollbar-color-active: $panel-lighten-3;
        scrollbar-corner-color: transparent;
        scrollbar-size: 1 1;
    }
    
    #command-prompt:focus {
        border: none;
        border-left: outer $primary;
    }
    """
    
    def __init__(
        self, 
        model: str, 
        provider: str, 
        safe_mode: bool,
        session: Optional[Session] = None,
        message_manager: Optional[MessageManager] = None
    ):
        super().__init__()
        self.model = model
        self.provider = provider
        self.safe_mode = safe_mode
        self.session = session
        self.message_manager = message_manager
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="app-header")
        
        with Container(id="main-container"):
            with Horizontal(id="main-content"):
                yield AgentBrain(id="left-pane", classes="pane")
                with Vertical(id="right-column"):
                    yield ActiveContext(id="top-right-pane", classes="pane")
                    yield LootReport(id="bottom-right-pane", classes="pane")
            yield CommandPrompt(placeholder="Enter command...", id="command-prompt")
        
        yield Footer(id="app-footer")
    
    def on_mount(self) -> None:
        """Initialize the conversation on mount."""
        self._update_context_panel(status="SCANNING")
        
        richlog = self.query_one("#agent-log", RichLog)
        
        # Load conversation history if we have a session
        if self.session and self.message_manager:
            messages = self.message_manager.get_history(self.session.id)
            for msg in messages:
                # Display the message with appropriate tag
                tag = msg.tag or msg.role.upper()
                log_message(richlog, tag, msg.content)
        else:
            # Default startup messages if no history
            log_message(richlog, "SYSTEM", "Swarm initialized.")
            log_message(richlog, "AGENT", "Parsing active context and scope.")
            log_message(richlog, "TRACE", "Connected to GitHub Copilot provider.")
            log_message(richlog, "DAST", "Header and endpoint probing queued.")
            log_message(richlog, "SAST", "Injection pattern pass started.")
    
    def _update_context_panel(self, status: str) -> None:
        """Update the active context panel with current status."""
        status_color = "bold $text-success" if status == "SCANNING" else "bold $text-warning"
        safe_mode_label = "ON" if self.safe_mode else "OFF"
        safe_mode_color = "bold $text-success" if self.safe_mode else "bold $text-warning"
        
        context_text = (
            "[bold $text-primary]TARGET[/]  github.com/example/repo\n"
            f"[bold $text-primary]STATUS[/]  [{status_color}]{status}[/]\n"
            f"[bold $text-primary]MODEL[/]   {self.model}\n"
            "[bold $text-primary]MODE[/]    Vulnerability Assessment\n\n"
            f"[$text-muted]Provider:[/] {self.provider}\n"
            f"[$text-muted]Safe mode:[/] [{safe_mode_color}]{safe_mode_label}[/]\n"
            "[$text-muted]Active agents:[/] DAST, SAST, Secrets, Fuzz\n"
            "[$text-muted]Last event:[/] Pattern baseline loaded"
        )
        self.query_one("#context-info", Static).update(context_text)
    
    def log_user_message(self, message: str) -> None:
        """Log a user message to the agent brain."""
        richlog = self.query_one("#agent-log", RichLog)
        log_message(richlog, "USER", message)
