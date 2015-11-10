# coding: utf-8
import builtins
from operator import itemgetter
import os
import pickle
import re
import subprocess
import sys
import webbrowser

import click
from github3 import login, null
from tabulate import tabulate
from gitsome.gitsome_command import GitSomeCommand
from xonsh.built_ins import iglobpath
from xonsh.environ import repo_from_remote
from xonsh.tools import subexpr_from_unbalanced
from xonsh.tools import ON_WINDOWS


class GitHub(object):
    """Provides integration with the GitHub API.

    Attributes:
        * api: An instance of github3 to interact with the GitHub API.
        * repo: A string that represents the user's current repo, as
            determined by the .git/ configured remote repo.
        * user_id: A string that represents the user's id in ~/.xonshrc
        * user_pass: A string that represents the user's pass in ~/.xonshrc
        * user_token: A string that represents the user's token in ~/.xonshrc

    """

    def __init__(self):
        """Inits GitSome.

        Args:
            * None.

        Returns:
            None.
        """
        self._login()
        self.repo = repo_from_remote()

    def _format_repo(self, repo):
        """Formats a repo tuple for pretty print.

        Example:
            Input:  ('donnemartin', 'gitsome')
            Output: donnemartin/gitsome

        Args:
            * args: A tuple that contains the user and repo.

        Returns:
            A string of the form user/repo.
        """
        return '/'.join(repo)

    def _listify(self, items):
        """Puts each list element in its own list.

        Example:
            Input: [a, b, c]
            Output: [[a], [b], [c]]

        This is needed for tabulate to print rows [a], [b], and [c].

        Args:
            * items: A list to listify.

        Returns:
            A list that contains elements that are listified.
        """
        output = []
        for item in items:
            item_list = []
            item_list.append(item)
            output.append(item_list)
        return output
