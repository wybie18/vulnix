from textual.widgets import ListItem
from textual.app import ComposeResult
from textual.containers import Container

from .base_modal import BaseModalScreen
from .widgets import WrapListView, SearchInput

class ThemesScreen(BaseModalScreen):
    """Modal screen for theme selection."""
    
    TITLE = "Themes"
    SEARCH_PLACEHOLDER = "Search themes..."
    STARTING_INDEX = 0
    
    THEMES = [
        "atom-one-dark",
        "catppuccin-frappe",
        "catppuccin-macchiato",
        "catppuccin-mocha",
        "dracula",
        "flexoki",
        "gruvbox",
        "monokai",
        "nord",
        "rose-pine",
        "rose-pine-moon",
        "solarized-dark",
        "textual-dark",
        "tokyo-night",
    ]
    
    def compose(self) -> ComposeResult:
        with Container(classes="modal-container"):
            yield self._menu_item("Themes", "esc to close")

            yield SearchInput(placeholder="Search themes...", classes="modal-search mt-1")

            with WrapListView(classes="modal-list mt-1"):
                for theme in self.THEMES:
                    yield ListItem(self._menu_item(theme, ""), id=theme)

    def on_list_view_selected(self, event: WrapListView.Selected) -> None:
        """Handle theme selection."""
        item_id = event.item.id
        
        if item_id in self.THEMES:
            self.app.theme = item_id
            self.app.pop_screen()