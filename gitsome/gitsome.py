import builtins
from operator import itemgetter
import os
import pickle
import re
import subprocess
import sys
import webbrowser

from gitsome.githubcli import GitHubCli
from gitsome.lib.github3 import login, null
from tabulate import tabulate
from xonsh.built_ins import iglobpath
from xonsh.tools import subexpr_from_unbalanced
from xonsh.tools import ON_WINDOWS


class GitSome(object):
    """Thin wrapper around GitHubCli.

    Attributes:
        * github_cli: An instance of GitHubCli.
    """

    def __init__(self):
        """Inits GitSome.

        Args:
            * None.

        Returns:
            None.
        """
        self.github_cli = GitHubCli()

    def execute(self, args):
        """Executes the gh command.

        Calls the dispatch to execute the command.
        If no command is given, it lists all available commands.
        Prints the rate limit if it starts to get low.

        Args:
            * args: A list of user supplied args.

        Returns:
            None.
        """
        old_sys_args = list(sys.argv)
        if args:
            # GitHubCli uses click, which looks for args in sys.argv.
            # Update sys.argv with our arguments before sending the command
            # off to GitHubCli.
            # TODO: Determine if there is a cleaner way to do this.
            sys.argv.extend(args)
        try:
            # Send the command to GitHubCli.
            self.github_cli.cli()
        except:
            # TODO: After every cli call the following exception is thrown:
            #   AttributeError: 'module' object has no
            #       attribute '__xonsh_env__'
            # Suppressing this exception does also silence helpful errors
            # during debugging, so disable this try/except block during dev
            # until this problem is fixed.
            pass
        if args:
            # Restore sys.argv to its original state.
            sys.argv = old_sys_args
