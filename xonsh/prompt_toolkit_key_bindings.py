"""Key bindings for prompt_toolkit xonsh shell."""
import builtins

from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import Condition
from prompt_toolkit.keys import Keys


@Condition
def tabs_should_insert_indent():
    """
    Filter that is intended to check if <Tab> should insert indent instead of
    starting autocompletion.
    It basically just checks if there are only whitespaces before the cursor -
    if so indent should be inserted, otherwise autocompletion.
    """
    before_cursor = get_app().current_buffer.document.current_line_before_cursor
    return bool(before_cursor.isspace())


def load_xonsh_bindings():
    """
    Load custom key bindings.
    """
    kb = KeyBindings()
    env = builtins.__xonsh_env__

    @kb.add('tab', filter=tabs_should_insert_indent)
    def _(event):
        """
        If there are only whitespaces before current cursor position insert
        indent instead of autocompleting.
        """
        event.app.current_buffer.insert_text(env.get('INDENT'))

    @kb.add(Keys.BackTab)
    def insert_literal_tab(event):
        """
        Insert literal tab on Shift+Tab instead of autocompleting
        """
        event.app.current_buffer.insert_text(env.get('INDENT'))


    return kb
