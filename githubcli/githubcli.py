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

    def _issue(self, user, repo, issue_number):
        """Outputs detailed information about the given issue.

        Args:
            * user: A string representing the user login.
            * repo: A string representing the repo name.
            * issue_number: An int representing the issue number.

        Returns:
            None.
        """
        issue = self.api.issue(user, repo, issue_number)
        if type(issue) is null.NullObject:
            click.secho('Error: Invalid issue.', fg='red')
            return
        click.echo('repo: ' + self._format_repo(issue.repository))
        click.echo('title: ' + issue.title)
        click.echo('issue url: ' + issue.html_url)
        click.echo('issue number: ' + str(issue.number))
        click.echo('state: ' + issue.state)
        click.echo('comments: ' + str(issue.comments_count))
        click.echo('labels: ' + str(issue.original_labels))
        if issue.milestone is not None:
            click.echo('milestone: ' + issue.milestone)
        click.echo('')
        click.echo(issue.body)
        comments = issue.comments()
        for comment in comments:
            click.echo('')
            click.echo('---Comment---')
            click.echo('')
            click.echo('user: ' + str(comment.user))
            click.echo('comment url: ' + comment.html_url)
            click.echo('created at: ' + str(comment.created_at))
            click.echo('updated at: ' + str(comment.updated_at))
            click.echo('')
            click.echo(comment.body)

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

    def _login(self):
        """Logs into GitHub.

        Logs in with a token if present, otherwise it uses the user and pass.
        TODO: Two factor authentication does not seem to be triggering the
            SMS code: https://github.com/sigmavirus24/github3.py/issues/387

        Args:
            * None.

        Returns:
            None.
        """
        get_env = lambda name, default=None: builtins.__xonsh_env__.get(
            name, default)
        self.user_id = get_env('GITHUB_USER_ID', None)
        self.user_pass = get_env('GITHUB_USER_PASS', None)
        self.user_token = get_env('GITHUB_TOKEN', None)
        if self.user_token is not None and False:
            self.api = login(token=self.user_token,
                            two_factor_callback=self._two_factor_code)
            click.echo('Authenticated with token: ' + self.api.me().login)
        else:
            self.api = login(self.user_id,
                             self.user_pass,
                             two_factor_callback=self._two_factor_code)
            click.echo('Authenticated with user id and password: ' + \
                self.api.me().login)

    def _print_items(self, items, headers):
        """Prints the items and headers with tabulate.

        Args:
            * items: A collection of items to print as rows with tabulate.
                Can be a list or dictionary.
            * headers: A collection of column headers to print with tabulate.
                If items is a list, headers should be a list.
                If items is a dictionary, set headers='keys'.

        Returns:
            None.
        """
        table = []
        for item in items:
            table.append(item)
        self._print_table(table, headers=headers)

    def _print_table(self, table, headers):
        """Prints the input table and headers with tabulate.

        Args:
            * table: A collection of items to print as rows with tabulate.
                Can be a list or dictionary.
            * headers: A collection of column headers to print with tabulate.
                If items is a list, headers should be a list.
                If items is a dictionary, set headers='keys'.

        Returns:
            None.
        """
        click.echo(tabulate(table, headers, tablefmt='grid'))

    def _return_elem_or_list(self, args):
        """Utility function to get a single element if len(args) == 1.

        Args:
            * args: A list of args.

        Returns:
            If args contains only one item, returns a single element.
            Else, returns args.
        """
        return args[0] if len(args) == 1 else args

    def _two_factor_code(self):
        """Callback if two factor authentication is requested.

        Args:
            * None.

        Returns:
            A string that represents the user input two factor
                authentication code.
        """
        code = ''
        while not code:
            code = input('Enter 2FA code: ')
        return code


pass_github = click.make_pass_decorator(GitHub)


class GitHubCli(object):

    @click.group()
    @click.pass_context
    def cli(ctx):
        # Create a GitHub object and remember it as as the context object.
        # From this point onwards other commands can refer to it by using the
        # @pass_github decorator.
        ctx.obj = GitHub()

    @cli.command()
    @click.argument('user')
    @click.argument('repo')
    @click.argument('issue_title')
    @pass_github
    def create_issue(github, user, repo, issue_title):
        """Creates an issue.

        Long description.

        Args:
            * user: A string representing the user login.
            * repo: A string representing the repo name.
            * issue_title: A string representing the issue title.

        Returns:
            None.
        """
        issue = github.api.create_issue(user, repo, issue_title)
        click.echo('Created issue: ' + issue.title)
        github._issue(user, repo, issue.number)

    @cli.command()
    @click.argument('user')
    @click.argument('repo')
    @click.argument('issue_number')
    @pass_github
    def issue(github, user, repo, issue_number):
        """Outputs detailed information about the given issue.

        Args:
            * user: A string representing the user login.
            * repo: A string representing the repo name.
            * issue_number: An int representing the issue number.

        Returns:
            None.
        """
        github._issue(user, repo, issue_number)

    @cli.command()
    @pass_github
    def emails(github):
        """Lists all the user's registered emails.

        Args:
            * None.

        Returns:
            None.
        """
        github._print_items(github.api.emails(), headers='keys')

    @cli.command()
    @pass_github
    def events(github):
        """Lists all public events.

        Args:
            * None.

        Returns:
            None.
        """
        events = github.api.all_events()
        table = []
        for event in events:
            table.append([event.created_at,
                          event.actor,
                          event.type,
                          github._format_repo(event.repo)])
        github._print_table(table,
                            headers=['created at', 'user', 'type', 'repo'])

    @cli.command()
    @pass_github
    def emojis(github):
        """Lists all GitHub supported emojis.

        Args:
            * None.

        Returns:
            None.
        """
        github._print_items(github._listify(github.api.emojis()),
                                            headers=['emoji'])

    @cli.command()
    @click.argument('threshold', required=False, default=20)
    @pass_github
    def rate_limit(github, threshold):
        """Outputs the rate limit.

        Args:
            * args: A list that contains an int representing the threshold.
                The rate limit is shown if it falls below the threshold.

        Returns:
            None.
        """
        limit = github.api.ratelimit_remaining
        if limit < threshold:
            click.echo('Rate limit: ' + str(limit))
