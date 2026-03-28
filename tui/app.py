from textual.app import App, ComposeResult
from textual.widgets import RichLog

from .database import Database, SessionManager, MessageManager
from .screens import MainScreen, WelcomeScreen
from .utils import ASCII_ART, log_message
from .widgets import CommandPrompt


class VulnixApp(App):
    """Vulnix QA/VA Swarm TUI."""
    
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
    ]
    
    # Model configuration
    provider = "GitHub Copilot"
    model = "GPT-5.3-Codex"
    safe_mode = True
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = None
        self.session_manager = None
        self.message_manager = None
        self.current_session = None

    def on_mount(self) -> None:
        """Initialize app and show welcome screen."""
        self.title = "VULNIX"
        self.sub_title = "QA/VA Swarm"
        self.theme = "textual-dark"
        
        # Initialize database
        self.db = Database()
        self.db.connect()
        self.session_manager = SessionManager(self.db)
        self.message_manager = MessageManager(self.db)
        
        # Create or load session
        latest_session = self.session_manager.get_latest()
        if latest_session:
            self.current_session = latest_session
            # Update app config from session
            self.model = latest_session.model
            self.provider = latest_session.provider
            self.safe_mode = latest_session.safe_mode
        else:
            # Create new session
            self.current_session = self.session_manager.create(
                model=self.model,
                provider=self.provider,
                safe_mode=self.safe_mode
            )
        
        # Push welcome screen on startup
        self.push_screen(WelcomeScreen(ASCII_ART, self.model, self.provider))

    def on_command_prompt_submitted(self, message: CommandPrompt.Submitted) -> None:
        """Handle command submission from any screen."""
        # Save user message to database
        if self.current_session and self.message_manager:
            self.message_manager.add(
                session_id=self.current_session.id,
                role="user",
                content=message.value,
                tag="USER"
            )
            # Touch session to update timestamp
            self.session_manager.touch(self.current_session.id)
        
        # Check if we're on the welcome screen
        if isinstance(self.screen, WelcomeScreen):
            # Switch to main screen
            self.switch_screen(MainScreen(
                self.model, 
                self.provider, 
                self.safe_mode,
                self.current_session,
                self.message_manager
            ))
            # Log the user message on the new screen
            main_screen = self.screen
            if isinstance(main_screen, MainScreen):
                main_screen.log_user_message(message.value)
        elif isinstance(self.screen, MainScreen):
            # Already on main screen, just log the message
            self.screen.log_user_message(message.value)
    
    def on_unmount(self) -> None:
        """Clean up database connection on app exit."""
        if self.db:
            self.db.close()


if __name__ == "__main__":
    app = VulnixApp()
    app.run()
