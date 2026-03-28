from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import RichLog


class AgentBrain(Container):
    """The Agent Brain/Live Trace (Left Pane)."""
    
    def compose(self) -> ComposeResult:
        log = RichLog(id="agent-log", markup=True, highlight=True, auto_scroll=True)
        log.can_focus = False
        yield log

    def on_mount(self) -> None:
        self.border_title = "[ AGENT BRAIN & TRACE ]"