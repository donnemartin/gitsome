"""Completer implementation to use with prompt_toolkit."""
from prompt_toolkit.completion import Completer, Completion

from gitsome.completer import CompleterGitsome


class PromptToolkitCompleter(Completer):
    """Simple prompt_toolkit Completer object.

    It just redirects requests to normal Xonsh completer.
    """

    def __init__(self, completer, ctx):
        """Takes instance of xonsh.completer.Completer and dict with context."""
        self.completer = completer
        self.completer_gitsome = CompleterGitsome()
        self.ctx = ctx

    def get_completions(self, document, complete_event):
        """Returns a generator for list of completions."""
        line = document.current_line
        endidx = document.cursor_position_col
        space_pos = document.find_backwards(' ')
        if space_pos is None:
            begidx = 0
        else:
            begidx = space_pos + endidx + 1
        prefix = line[begidx:endidx]
        completions = self.completer.complete(prefix,
                                              line,
                                              begidx,
                                              endidx,
                                              self.ctx)
        completions_gitsome = \
            self.completer_gitsome.get_completions(document,
                                                   complete_event)
        completions_with_meta = \
            self.completer_gitsome.build_completions_with_meta(line,
                                                               prefix,
                                                               completions)
        completions_gitsome.extend(completions_with_meta)
        for comp in completions_gitsome:
            yield comp
