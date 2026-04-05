from textual.app import App

from database import init_db

from database import sessions, events
from .screens import MainScreen, WelcomeScreen
from .screens.modals import SettingsScreen
from .utils import ASCII_ART
from .widgets import CommandPrompt


class VulnixApp(App):
    """Vulnix QA/VA Swarm TUI."""
    
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+p", "settings", "Settings"),
    ]
    ENABLE_COMMAND_PALETTE = False
    
    # Default configuration
    provider = "GitHub Copilot"
    model = "GPT-5.3-Codex"
    default_target = "."
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_session = None
    
    def on_mount(self) -> None:
        """Initialize app and show welcome screen."""
        self.title = "VULNIX"
        self.sub_title = "QA/VA Swarm"
        self.theme = "textual-dark"
        
        # Initialize database
        init_db()
        
        # Always create a new session when starting the app
        # (old sessions remain in database with their status)
        self.current_session = sessions.create_session(
            target=self.default_target,
            target_type="filesystem",
            config={
                "model": self.model,
                "provider": self.provider,
                "agents": ["SAST", "DAST", "Secrets", "Fuzz"]
            }
        )
        
        # Log session start event
        events.append(
            session_id=self.current_session.id,
            type="log",
            payload={"message": "Session started", "target": self.default_target, "tag": "SYSTEM"}
        )
        
        # Push welcome screen on startup
        self.push_screen(WelcomeScreen(ASCII_ART, self.model, self.provider))

    def on_command_prompt_submitted(self, message: CommandPrompt.Submitted) -> None:
        """Handle command submission from any screen."""
        # Log user command as event
        if self.current_session:
            events.append(
                session_id=self.current_session.id,
                type="log",
                payload={"message": message.value, "tag": "USER"}
            )
        
        if isinstance(self.screen, WelcomeScreen):
            self.switch_screen(MainScreen(session=self.current_session))
        elif isinstance(self.screen, MainScreen):
            self.screen.log_user_message(message.value)
    
    def action_settings(self) -> None:
        """Show the settings modal."""
        self.push_screen(SettingsScreen())


if __name__ == "__main__":
    app = VulnixApp()
    app.run()
