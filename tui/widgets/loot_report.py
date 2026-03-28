from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Markdown


class LootReport(Container):
    """The Loot/Report Table (Bottom Right Pane)."""
    
    can_focus = False
    
    def compose(self) -> ComposeResult:
        yield Markdown(id="loot-markdown")

    def on_mount(self) -> None:
        self.border_title = "[ LOOT REPORT ]"
        
        report_md = """\
| ID | Severity | Vulnerability | File |
|---|---|---|---|
| 1 | **High** | SQL Injection | `src/db.py` |
| 2 | **Medium** | Reflected XSS | `frontend/app.tsx` |
| 3 | **Low** | Missing Headers | `config/nginx.conf` |
| 4 | **Critical** | Hardcoded Secret | `settings.py` |
"""
        self.query_one(Markdown).update(report_md)
