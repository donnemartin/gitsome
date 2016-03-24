# coding: utf-8
from getpass import getpass
from operator import itemgetter
import os
import urllib
import webbrowser
try:
    # Python 3
    import configparser
except ImportError:
    # Python 2
    import ConfigParser as configparser

import click
from gitsome.lib.github3 import authorize, login, null
from gitsome.lib.github3.exceptions import UnprocessableEntity
from tabulate import tabulate

# from gitsome.lib.img2txt import img2txt


class GitHub(object):
    """Provides integration with the GitHub API.

    Attributes:
        * api: An instance of github3 to interact with the GitHub API.
        * CONFIG: A string representing the config file name.
        * CONFIG_SECTION: A string representing the main config file section.
        * CONFIG_USER_LOGIN: A string representing the user login config.
        * CONFIG_USER_PASS: A string representing the user pass config.
        * CONFIG_USER_TOKEN: A string representing the user token config.
        * CONFIG_URL: A string representing the jump to url config file name.
        * CONFIG_URL_SECTION: A string representing the jump to url config
            file section.
        * CONFIG_URL_LIST: A string representing the jump to url list in the
            config.
        * GITHUB_ISSUES: A string representing the GitHub issues url portion.
        * GITHUB_URL: A string representing the GitHub main url.
        * urls: A list containing the last set of urls the user has seen,
            which allows the user to quickly access a repo url with the
            gh view [url_index] command.
        * user_login: A string that represents the user's login in
            ~/.githubconfig
        * user_pass: A string that represents the user's pass in
            ~/.githubconfig
        * user_token: A string that represents the user's token in
            ~/.githubconfig
    """

    CONFIG = '.githubconfig'
    CONFIG_SECTION = 'github'
    CONFIG_USER_LOGIN = 'user_login'
    CONFIG_USER_PASS = 'user_pass'
    CONFIG_USER_TOKEN = 'user_token'
    CONFIG_URL = '.githubconfigurl'
    CONFIG_URL_SECTION = 'url'
    CONFIG_URL_LIST = 'url_list'
    CONFIG_AVATAR = '.githubconfigavatar.png'
    GITHUB_ISSUES = 'issues/'
    GITHUB_URL = 'https://github.com/'

    def __init__(self):
        """Inits GitHub.

        Args:
            * None.

        Returns:
            None.
        """
        self.api = None
        self.user_login = None
        self.user_pass = None
        self.user_token = None
        self._login()
        self.urls = []

    def _github_config(self, config_file_name):
        """Attempts to find the github config file.

        Adapted from https://github.com/sigmavirus24/github-cli.

        Args:
            * config_file_name: A String that represents the config file name.

        Returns:
            A string that represents the github config file path.
        """
        home = os.path.abspath(os.environ.get('HOME', ''))
        config_file_path = os.path.join(home, config_file_name)
        return config_file_path

    def _login(self):
        """Logs into GitHub.

        Adapted from https://github.com/sigmavirus24/github-cli.

        TODO: Two factor authentication does not seem to be triggering the
            SMS code: https://github.com/sigmavirus24/github3.py/issues/387

        Args:
            * None.

        Returns:
            None.
        """
        # Get the full path to the configuration file
        config = self._github_config(self.CONFIG)
        parser = configparser.RawConfigParser()
        # Check to make sure the file exists and we are allowed to read it
        if os.path.isfile(config) and os.access(config, os.R_OK | os.W_OK):
            parser.readfp(open(config))
            self.user_login = parser.get(self.CONFIG_SECTION,
                                         self.CONFIG_USER_LOGIN)
            self.api = login(token=parser.get(self.CONFIG_SECTION,
                                              self.CONFIG_USER_TOKEN),
                             two_factor_callback=self._two_factor_code)
        else:
            # Either the file didn't exist or we didn't have the correct
            # permissions
            self.user_login = ''
            while not user_login:
                user_login = input('User Login: ')
            user_pass = ''
            while not user_pass:
                user_pass = getpass('Password: ')
            auth = None
            try:
                # Get an authorization for this
                auth = authorize(
                    user_login,
                    user_pass,
                    scopes=['user', 'repo', 'gist'],
                    note='githubcli',
                    note_url='https://github.com/donnemartin/github-cli'
                )
            except UnprocessableEntity:
                click.secho('Error creating token.\nVisit the following ' \
                            'page and verify you do not have an existing ' \
                            'token named "githubcli":\n' \
                            'See https://github.com/settings/tokens\n' \
                            'If a token already exists update your ' + \
                            self.githubconfig + ' file with your user_token.',
                            fg='red')
            parser.add_section(self.CONFIG_SECTION)
            parser.set(self.CONFIG_SECTION, self.CONFIG_USER_LOGIN, user_login)
            parser.set(self.CONFIG_SECTION, self.CONFIG_USER_PASS, user_pass)
            parser.set(self.CONFIG_SECTION, self.CONFIG_USER_TOKEN, auth.token)
            self.api = login(token=auth.token,
                             two_factor_callback=self._two_factor_code)
            # Create the file if it doesn't exist. Otherwise completely blank
            # out what was there before. Kind of dangerous and destructive but
            # somewhat necessary
            # TODO: Refactor this
            config_file = open(config, 'w+')
            parser.write(config_file)
            config_file.close()

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

    def avatar(self, url, ansi):
        """Displays the user's avatar from the specified url.

        Args:
            * url: A string representing the user's avatar image.
            * ansi: A boolean that determines whether to view the profile
                avatar in a ansi, or plain text.

        Returns:
            None.
        """
        avatar = self._github_config(self.CONFIG_AVATAR)
        urllib.request.urlretrieve(url, avatar)
        img2txt(avatar, ansi=ansi)
        os.remove(avatar)

    def build_issue_urls(self, table, url_index, issue_index):
        """Builds the GitHub urls for the input table containing issues.

        Note: This method modifies the table's url_index, adding a
        0-based index that allow you to access an issue url with the
        gh view [url_index] command.

        Args:
            * table: A list that contains repo information.
            * url_index: The index in the table that will allow you to
                access a repo url with the gh view [url_index] command.
            * issue_index: The index in the table containing the issue.

        Returns:
            None.
        """
        click.secho('Tip: View issue details in your terminal or browser' \
                    ' with the following command:\n' \
                    '    gh view [#] [-b/--browser]',
                    fg='blue')
        number = 0
        for row in table:
            row[0] = number
            number += 1
            self.urls.append(self.GITHUB_URL + row[issue_index])
        self.save_urls()

    def build_repo_urls(self, table, url_index, repo_index):
        """Builds the GitHub urls for the input table containing repo names.

        Note: This method modifies the table's url_index, adding a
        0-based index that allow you to access a repo url with the
        gh view [url_index] command.

        Args:
            * table: A list that contains repo information.
            * url_index: The index in the table that will allow you to
                access a repo url with the gh view [url_index] command.
            * repo_index: The index in the table containing the repo name.

        Returns:
            None.
        """
        click.secho('Tip: View repo details in your terminal or browser' \
                    ' with the following command:\n' \
                    '    gh view [#] [-b/--browser]',
                    fg='blue')
        number = 0
        for row in table:
            row[0] = number
            number += 1
            self.urls.append(self.GITHUB_URL + row[repo_index])
        self.save_urls()

    def format_repo(self, repo):
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

    def issue(self, user_login, repo_name, issue_number):
        """Outputs detailed information about the given issue.

        Args:
            * user_login: A string representing the user login.
            * repo: A string representing the repo name.
            * issue_number: An int representing the issue number.

        Returns:
            None.
        """
        issue = self.api.issue(user_login, repo_name, issue_number)
        if type(issue) is null.NullObject:
            click.secho('Error: Invalid issue.', fg='red')
            return
        click.secho('#' + str(issue.number) + ': ' + \
                   issue.title + ' - ' + \
                   '@' + str(issue.user) + ' [' + \
                   issue.state + ']',
                   fg='blue')
        click.secho('Assignee: ' + str(issue.assignee), fg='blue')
        if issue.body and issue.body is not None:
            click.echo('\n' + issue.body)
        comments = issue.comments()
        for comment in comments:
            click.secho('\n--Comment by @' + str(comment.user) + '---\n',
                        fg='blue')
            click.echo(comment.body)

    def issues(self, issue_filter, state):
        """Lists all issues.

        Args:
            * issue_filter: A string with the following accepted values:
                'assigned', 'created', 'mentioned', 'subscribed'.
            * state: A string with the following accepted values:
                'all', 'open', 'closed'.

        Returns:
            None.
        """
        issues = self.api.issues(filter=issue_filter, state=state)
        table = []
        number = 0
        for issue in issues:
            table.append([number,
                          issue.state,
                          self.format_repo(issue.repository) + '/' + \
                          str(self.GITHUB_ISSUES) + str(issue.number),
                          issue.title + ' @' + str(issue.user),
                          str(issue.assignee),
                          issue.comments_count])
        # Sort by repo, state
        table = sorted(table, key=itemgetter(1, 0))
        self.build_issue_urls(table, url_index=0, issue_index=2)
        self.print_table(table,
                         headers=['#', 'state', 'issue',
                                  'title', 'assignee', 'comments'])

    def listify(self, items):
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

    def view(self, index, view_in_browser):
        """Views the given index in a browser.

        Loads urls from ~/.githubconfigurl and stores them in self.urls.
        Opens a browser with the url based on the given index.

        Args:
            * index: An int that specifies the index to open in a browser.
            * view_in_browser: A boolean that determines whether to view
                in a web browser or a terminal.

        Returns:
            None.
        """
        config = self._github_config(self.CONFIG_URL)
        parser = configparser.RawConfigParser()
        config_file = open(config)
        try:
            parser.readfp(config_file)
            urls = parser.get(self.CONFIG_URL_SECTION,
                              self.CONFIG_URL_LIST)
            urls = urls.strip()
            excludes = ['[', ']', "'"]
            for exclude in excludes:
                urls = urls.replace(exclude, '')
                if not view_in_browser:
                    urls = urls.replace(self.GITHUB_URL, '')
            self.urls = urls.split(', ')
            if view_in_browser:
                webbrowser.open(self.urls[index])
            else:
                url = self.urls[index]
                if self.GITHUB_ISSUES in url:
                    url = url.replace(self.GITHUB_ISSUES, '')
                    user_login, repo_name, issue_number = url.split('/')
                    self.issue(user_login, repo_name, issue_number)
                else:
                    user_login, repo_name = url.split('/')
                    self.repository(user_login, repo_name)
        except Exception as e:
            click.secho('Error: ' + str(e), fg='red')
        finally:
            config_file.close()

    def print_items(self, items, headers):
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
        self.print_table(table, headers=headers)

    def print_table(self, table, headers):
        """Prints the table and headers with tabulate.

        Args:
            * table: A collection of items to print as rows with tabulate.
            * headers: A collection of column headers to print with tabulate.

        Returns:
            None.
        """
        click.echo(tabulate(table, headers, tablefmt='grid'))

    def repository(self, user_login, repo_name, num_readme_lines=25):
        """Outputs detailed information about the given repo.

        If args does not contain user and repo, attempts to display repo
        information from the .git/ configured remote repo.

        Args:
            * user_login: A string representing the user login.
            * repo_name: A string representing the repo name.
            * num_readme_lines: An int that determines the number of lines
                to display for the README.

        Returns:
            None.
        """
        repo = self.api.repository(user_login, repo_name)
        if type(repo) is null.NullObject:
            click.secho('Repo not found.', fg='red')
            return
        click.secho(repo.full_name, fg='blue')
        if repo.description:
            click.secho(repo.description, fg='blue')
        click.secho('Stars: ' + str(repo.stargazers_count) + ' | '
                    'Forks: ' + str(repo.forks_count),
                    fg='blue')
        click.secho('Url: ' + repo.clone_url, fg='blue')
        readme = repo.readme()
        click.echo('')
        if type(readme) is null.NullObject:
            click.secho('No README found.', fg='blue')
            return
        click.secho('--Displaying first ' + str(num_readme_lines) + \
                    ' lines of README--\n',
                    fg='blue')
        content = readme.decoded.decode('utf-8')
        lines = content.split('\n')
        for iterations, line in enumerate(lines):
            click.echo(line)
            if iterations >= num_readme_lines:
                break

    def repositories(self, repos, repo_filter=''):
        """Lists all repos matching the given filter.

        Args:
            * repos: A list of github3.repos.repo.
            * repo_filter: A string representing a filter for repo names.
                Only repos matching the filter will be returned.
                If None, outputs all starred repos.

        Returns:
            None.
        """
        table = []
        number = 0
        for repo in repos:
            if repo_filter in repo.full_name.lower() or \
                    repo_filter in repo.description.lower():
                table.append([number,
                              repo.full_name,
                              repo.clone_url,
                              repo.stargazers_count,
                              repo.forks_count])
            number += 1
        # Sort by stars, repo name
        table = sorted(table, key=itemgetter(3, 1), reverse=True)
        self.build_repo_urls(table, url_index=0, repo_index=1)
        self.print_table(table, headers=['#', 'repo', 'url', 'stars', 'forks'])

    def save_urls(self):
        """Saves the current set of urls to ~/.githubconfigurl.

        Args:
            * None

        Returns:
            None.
        """
        config = self._github_config(self.CONFIG_URL)
        parser = configparser.RawConfigParser()
        try:
            parser.add_section(self.CONFIG_URL_SECTION)
        except DuplicateSectionError:
            pass
        parser.set(self.CONFIG_URL_SECTION, self.CONFIG_URL_LIST, self.urls)
        # TODO: Refactor this
        config_file = open(config, 'w+')
        parser.write(config_file)
        config_file.close()
