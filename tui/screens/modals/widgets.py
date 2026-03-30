"""Shared widgets for modal screens."""

from textual.widgets import Input, ListView, Static


class SectionHeader(Static):
    """A non-interactive section header."""
    pass


class SearchInput(Input):
    """Search input for modal screens."""
    
    DEFAULT_CSS = """
    SearchInput {
        width: 100%;
        height: auto;
        background: transparent;
        border: none;
        padding: 0 1;
    }
    
    SearchInput:focus {
        border: none;
        background: transparent;
    }
    
    SearchInput > .input--placeholder {
        color: $text-muted;
    }
    """


class WrapListView(ListView):
    """A ListView that wraps around when navigating past boundaries."""
    
    def _get_selectable_indices(self) -> list[int]:
        """Get indices of all selectable (non-disabled, visible) items."""
        return [
            i for i, item in enumerate(self._nodes) 
            if not item.disabled and item.display
        ]
    
    def action_cursor_down(self) -> None:
        """Move cursor down, wrapping to top if at bottom."""
        selectable = self._get_selectable_indices()
        if not selectable:
            return
        
        # Find current position in selectable items
        try:
            current_pos = selectable.index(self.index)
            # Move to next, or wrap to first
            if current_pos >= len(selectable) - 1:
                self.index = selectable[0]
            else:
                self.index = selectable[current_pos + 1]
        except ValueError:
            # Current index not in selectable, go to first
            self.index = selectable[0]
    
    def action_cursor_up(self) -> None:
        """Move cursor up, wrapping to bottom if at top."""
        selectable = self._get_selectable_indices()
        if not selectable:
            return
        
        # Find current position in selectable items
        try:
            current_pos = selectable.index(self.index)
            # Move to previous, or wrap to last
            if current_pos <= 0:
                self.index = selectable[-1]
            else:
                self.index = selectable[current_pos - 1]
        except ValueError:
            # Current index not in selectable, go to last
            self.index = selectable[-1]
    
    def select_first_visible(self) -> None:
        """Select the first visible, selectable item."""
        selectable = self._get_selectable_indices()
        if selectable:
            self.index = selectable[0]
