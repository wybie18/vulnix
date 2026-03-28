from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static


class ActiveContext(Container):
    """The Active Context (Top Right Pane)."""
    
    can_focus = False
    
    def compose(self) -> ComposeResult:
        context_text = (
            "[bold $text-primary]TARGET[/]  github.com/example/repo\n"
            "[bold $text-primary]STATUS[/]  [bold $text-success]SCANNING[/]\n"
            "[bold $text-primary]MODEL[/]   GitHub Copilot\n"
            "[bold $text-primary]MODE[/]    Vulnerability Assessment\n\n"
            "[$text-muted]Active agents:[/] DAST, SAST, Secrets, Fuzz\n"
            "[$text-muted]Last event:[/] Pattern baseline loaded"
        )
        yield Static(context_text, id="context-info", markup=True)

    def on_mount(self) -> None:
        self.border_title = "[ ACTIVE CONTEXT ]"
