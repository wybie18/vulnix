from textual.widgets import ListItem
from textual.app import ComposeResult

from .base_modal import BaseModalScreen
from .themes_screen import ThemesScreen
from .widgets import SectionHeader, WrapListView

class SettingsScreen(BaseModalScreen):
    """Modal screen for application settings."""
    
    TITLE = "Settings"
    SEARCH_PLACEHOLDER = "Search settings..."
    STARTING_INDEX = 1
    
    def compose_items(self) -> ComposeResult:
        # Sessions section
        yield ListItem(SectionHeader("Sessions"), classes="section-header", disabled=True)
        yield ListItem(self._menu_item("Switch Session", ""), id="switch-session")
        yield ListItem(self._menu_item("New Session", ""), id="new-session")
        
        # Prompt section
        yield ListItem(SectionHeader("Prompt"), classes="section-header", disabled=True)
        yield ListItem(self._menu_item("Skills", ""), id="skills")
        
        # Agent section
        yield ListItem(SectionHeader("Agent"), classes="section-header", disabled=True)
        yield ListItem(self._menu_item("Switch Agent", ""), id="switch-agent")
        yield ListItem(self._menu_item("Switch Model", ""), id="switch-model")
        
        # Provider section
        yield ListItem(SectionHeader("Provider"), classes="section-header", disabled=True)
        yield ListItem(self._menu_item("Connect Provider", ""), id="connect-provider")
        
        # System section
        yield ListItem(SectionHeader("System"), classes="section-header", disabled=True)
        yield ListItem(self._menu_item("Theme"), id="theme")
        yield ListItem(self._menu_item("Screenshot", ""), id="screenshot")
        yield ListItem(self._menu_item("Quit", "ctrl+q"), id="quit")

    def on_list_view_selected(self, event: WrapListView.Selected) -> None:
        """Handle menu item selection."""
        item_id = event.item.id
        
        if item_id == "switch-session":
            self.notify("Switch Session - Not implemented yet")
        # ... (keep the rest of your original elif statements here) ...
        elif item_id == "theme":
            self.app.switch_screen(ThemesScreen())
        elif item_id == "quit":
            self.app.exit()