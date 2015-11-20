# coding: utf-8
import builtins
from operator import itemgetter
import os
import pickle
import re
import subprocess
import sys
import webbrowser
import urllib
from getpass import getpass
try:
    # Python 3
    import configparser
except ImportError:
    # Python 2
    import ConfigParser as configparser

import click
from github3 import authorize, login, null
from github3.exceptions import UnprocessableEntity
from tabulate import tabulate

from img2txt.img2txt import img2txt


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
            parser.write(open(config, 'w+'))

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

        Loads urls from .githubconfigurl and stores them in self.urls.
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
        try:
            parser.readfp(open(config))
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
        """Saves the current set of urls to .githubconfigurl.

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
        parser.write(open(config, 'w+'))


pass_github = click.make_pass_decorator(GitHub)


class GitHubCli(object):
    """Encapsulates the GitHubCli.

    Attributes:
        * None.
    """

    @click.group()
    @click.pass_context
    def cli(ctx):
        """Main entry point for GitHubCli.

        Args:
            * ctx: An instance of click.core.Context that stores an instance
                 of GitHub used to interact with the GitHub API.

        Returns:
            None.
        """
        # Create a GitHub object and remember it as as the context object.
        # From this point onwards other commands can refer to it by using the
        # @pass_github decorator.
        ctx.obj = GitHub()

    @cli.command()
    @click.argument('index')
    @click.option('-b', '--browser', is_flag=True)
    @pass_github
    def view(github, index, browser):
        """Views the given index in a browser.

        Example(s):
            gh view repos
            gh view 0

            gh view starred
            gh view 0 -b
            gh view 0 --browser

        This method is meant to be called after one of the following commands
        which outputs a table of repos or issues:

            * gh repos
            * gh search_repos
            * gh starred

            * gh issues
            * gh pull_requests
            * gh search_issues

        Args:
            * index: An int that specifies the index to open in a browser.
                For example, calling gh repositories will list repos with a
                0-based index for each repo.  Calling gh view [index] will
                open the url for the associated repo in a browser.
            * browser: A boolean that determines whether to view in a
                web browser or a terminal.

        Returns:
            None.
        """
        github.view(int(index), browser)

    @cli.command()
    @click.argument('user_login')
    @click.argument('repo_name')
    @click.argument('issue_title')
    @click.argument('issue_body', required=False)
    @pass_github
    def create_issue(github, user_login, repo_name, issue_title, issue_body):
        """Creates an issue.

        Example(s):
            gh donnemartin gitsome "issue title"
            gh donnemartin gitsome "issue title" "issue body"

        Args:
            * user_login: A string representing the user login.
            * repo_name: A string representing the repo name.
            * issue_title: A string representing the issue title.
            * issue_body: A string representing the issue body (optional).

        Returns:
            None.
        """
        issue = github.api.create_issue(user_login,
                                        repo_name,
                                        issue_title,
                                        issue_body)
        click.echo('Created issue: ' + issue.title)
        github.issue(user_login, repo_name, issue.number)

    @cli.command()
    @click.argument('repo_name')
    @click.argument('repo_desc', required=False)
    @click.option('-p', '--private', is_flag=True)
    @pass_github
    def create_repo(github, repo_name, repo_desc, private):
        """Creates a repo.

        Example(s):
            gh create_repo "repo name"
            gh create_repo "repo name" "repo description"
            gh create_repo "repo name" "repo description" -p
            gh create_repo "repo name" "repo description" --private

        Args:
            * repo_name: A string representing the repo name.
            * repo_desc: A string representing the repo description (optional).
            * private: A boolean that determines whether the repo is private.
                Default: False.

        Returns:
            None.
        """
        repo = github.api.create_repository(repo_name,
                                            repo_desc,
                                            private=private)
        click.secho('Created repo: ' + repo.full_name, fg='blue')

    @cli.command()
    @pass_github
    def emails(github):
        """Lists all the user's registered emails.

        Example(s):
            gh emails

        Args:
            * None.

        Returns:
            None.
        """
        github.print_items(github.api.emails(), headers='keys')

    @cli.command()
    @pass_github
    def events(github):
        """Lists all public events.

        Examples:
            gh events | grep foo
            gh events | less

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
                          github.format_repo(event.repo)])
        github.print_table(table,
                           headers=['created at', 'user', 'type', 'repo'])

    @cli.command()
    @pass_github
    def emojis(github):
        """Lists all GitHub supported emojis.

        Example(s):
            gh emojis | grep octo

        Args:
            * None.

        Returns:
            None.
        """
        github.print_items(github.listify(github.api.emojis()),
                                          headers=['emoji'])

    @cli.command()
    @pass_github
    def feeds(github):
        """Lists GitHub's timeline resources.

        Requires authentication with user/pass, cannot be used with tokens
        due to a limitation with the GitHub API itself.

        TODO: Results in an exception with github3.py.

        Example(s):
            gh feeds

        Args:
            * None.

        Returns:
            None.

        Raises:
            TypeError: Seems to be a github3.py bug.
        """
        click.secho('This command is temporarily unavailable.', fg='red')
        # github.api.feeds()

    @cli.command()
    @click.argument('user_login', required=False)
    @pass_github
    def followers(github, user_login):
        """Lists all followers and the total follower count.

        Example(s):
            gh followers
            gh followers donnemartin

        Args:
            * user_login: A string representing the user login.
                If None, returns followers of the logged in user.

        Returns:
            None.
        """
        if user_login is None:
            user_login = github.user_login
        users = github.api.followers_of(user_login)
        table = []
        for user in users:
            table.append([user.login, user.html_url])
        github.print_table(table, headers=['user', 'profile'])
        click.secho(
            'Followers: ' + str(github.api.user(user_login).followers_count),
            fg='blue')

    @cli.command()
    @click.argument('user_login', required=False)
    @pass_github
    def following(github, user_login):
        """Lists all followed users and the total followed count.

        Example(s):
            gh following
            gh following donnemartin

        Args:
            * user_login: A string representing the user login.
                If None, returns the followed users of the logged in user.

        Returns:
            None.
        """
        if user_login is None:
            user_login = github.user_login
        users = github.api.followed_by(user_login)
        table = []
        for user in users:
            table.append([user.login, user.html_url])
        github.print_table(table, headers=['user', 'profile'])
        click.secho(
            'Following ' + str(github.api.user(user_login).following_count),
            fg='blue')

    @cli.command()
    @click.argument('language')
    @pass_github
    def gitignore_template(github, language):
        """Outputs the gitignore template for the given language.

        Example(s):
            gh gitignore_template Python
            gh gitignore_template Python > .gitignore

        Args:
            * language: A string representing the language.

        Returns:
            None.
        """
        template = github.api.gitignore_template(language)
        if template:
            click.echo(template)
        else:
            click.secho('Invalid template requested, run the following ' \
                       'command to see available templates:\n' \
                       '    gh gitignore_templates',
                       fg='red')

    @cli.command()
    @pass_github
    def gitignore_templates(github):
        """Outputs all supported gitignore templates.

        Example(s):
            gh gitignore_templates

        Args:
            * None.

        Returns:
            None.
        """
        github.print_items(
            github.listify(github.api.gitignore_templates()),
                           headers=['language'])

    @cli.command()
    @click.argument('user_login')
    @click.argument('repo_name')
    @click.argument('issue_number')
    @pass_github
    def issue(github, user_login, repo_name, issue_number):
        """Outputs detailed information about the given issue.

        Example(s):
            gh donnemartin saws 1

        Args:
            * user_login: A string representing the user login.
            * repo_name: A string representing the repo name.
            * issue_number: An int representing the issue number.

        Returns:
            None.
        """
        github.issue(user_login, repo_name, issue_number)

    @cli.command()
    @click.argument('issue_filter', required=False, default='subscribed')
    @click.argument('state', required=False, default='open')
    @pass_github
    def issues(github, issue_filter, state):
        """Lists all issues.

        Example(s):
            gh issues
            gh issues assigned
            gh issues created all | grep foo

        Args:
            * issue_filter: A string with the following accepted values:
                'assigned', 'created', 'mentioned', 'subscribed' (default).
            * state: A string with the following accepted values:
                'all', 'open' (default), 'closed'.

        Returns:
            None.
        """
        github.issues(issue_filter, state)

    @cli.command()
    @click.option('-b', '--browser', is_flag=True)
    @click.option('-a', '--ansi', is_flag=True)
    @pass_github
    def me(github, browser, ansi):
        """Lists information about the logged in user.

        Example(s):
            gh me
            gh me -b
            gh me --browser
            gh me -a
            gh me --ansi

        Args:
            * browser: A Boolean that determines whether to view the profile
                in a browser, or in the terminal.
            * ansi: A boolean that determines whether to view the profile
                avatar in a ansi, or plain text.

        Returns:
            None.
        """
        if browser:
            url = 'https://github.com/' + github.user_login
            webbrowser.open(url)
        else:
            user = github.api.me()
            github.avatar(user.avatar_url, ansi)
            click.echo('')
            click.secho(user.login, fg='blue')
            if user.company is not None:
                click.secho('company:', user.company, fg='blue')
            if user.location is not None:
                click.secho('location:', user.location, fg='blue')
            if user.email is not None:
                click.secho('email: ' + user.email, fg='blue')
            click.secho('followers: ' + str(user.followers_count), fg='blue')
            click.secho('following: ' + str(user.following_count), fg='blue')
            click.echo('')
            github.repositories(github.api.repositories())

    @cli.command()
    @pass_github
    def notifications(github):
        """Lists all notifications.

        TODO: Always results in an empty list.  Possible github3.py bug.

        Example(s):
            gh notifications

        Args:
            * None.

        Returns:
            None.
        """
        click.secho('This command is temporarily unavailable.', fg='red')
        # github.print_items(github.api.notifications(participating=True),
        #                    headers=['notification'])

    @cli.command()
    @click.argument('say', required=False)
    @pass_github
    def octocat(github, say):
        """Outputs an Easter egg or the given message from Octocat.

        Example(s):
            gh octocat
            gh octocat "foo bar"

        Args:
            * say: A string for octocat to say.
                If say is None, octocat speaks an Easter egg.

        Returns:
            None.
        """
        output = str(github.api.octocat(say))
        output = output.replace('\\n', '\n')
        click.echo(output)

    @cli.command()
    @click.argument('user_login')
    @click.argument('repo_name')
    @click.argument('issue_number')
    @pass_github
    def pull_request(github, user_login, repo_name, issue_number):
        """Outputs detailed information about the given pull request.

        Example(s):
            gh pull_request donnemartin awesome-aws 2

        Args:
            * user_login: A string representing the user login.
            * repo_name: A string representing the repo name.
            * issue_number: An int representing the issue number.

        Returns:
            None.
        """
        github.issue(user_login, repo_name, issue_number)

    @cli.command()
    @pass_github
    def pull_requests(github):
        """Lists all pull requests.

        Example(s):
            gh pull_requests

        Args:
            * None.

        Returns:
            None.
        """
        pull_requests = []
        repositories = github.api.repositories()
        for repository in repositories:
            repo_pulls = repository.pull_requests()
            for repo_pull in repo_pulls:
                pull_requests.append(repo_pull)
        table = []
        for pull_request in pull_requests:
            user_login, repo_name = pull_request.repository
            repo = user_login.strip('repos/') + '/' + repo_name
            table.append([pull_request.number,
                          repo,
                          pull_request.title])
        # Sort by repo, pull request number
        table = sorted(table, key=itemgetter(1, 0))
        github.print_table(table, headers=['#', 'repo', 'title'])

    @cli.command()
    @pass_github
    def rate_limit(github):
        """Outputs the rate limit.

        Example(s):
            gh rate_limit

        Args:
            * None.

        Returns:
            None.
        """
        click.echo('Rate limit: ' + str(github.api.ratelimit_remaining))

    @cli.command('repo')
    @click.argument('user_login')
    @click.argument('repo_name')
    @pass_github
    def repository(github, user_login, repo_name):
        """Outputs detailed information about the given repo.

        Example(s):
            gh repo donnemartin gitsome

        Args:
            * user_login: A string representing the user login.
            * repo_name: A string representing the repo name.

        Returns:
            None.
        """
        github.repository(user_login, repo_name)

    @cli.command('repos')
    @pass_github
    def repositories(github):
        """Lists all repos.

        Example(s):
            gh repos

        Args:
            * None.

        Returns:
            None.
        """
        github.repositories(github.api.repositories())

    @cli.command()
    @click.argument('query')
    @pass_github
    def search_issues(github, query):
        """Searches all issues with the given query.

        The query can contain any combination of the following supported
        qualifers:

        - ``type`` With this qualifier you can restrict the search to issues
          or pull request only.
        - ``in`` Qualifies which fields are searched. With this qualifier you
          can restrict the search to just the title, body, comments, or any
          combination of these.
        - ``author`` Finds issues created by a certain user.
        - ``assignee`` Finds issues that are assigned to a certain user.
        - ``mentions`` Finds issues that mention a certain user.
        - ``commenter`` Finds issues that a certain user commented on.
        - ``involves`` Finds issues that were either created by a certain user,
          assigned to that user, mention that user, or were commented on by
          that user.
        - ``state`` Filter issues based on whether they’re open or closed.
        - ``labels`` Filters issues based on their labels.
        - ``language`` Searches for issues within repositories that match a
          certain language.
        - ``created`` or ``updated`` Filters issues based on times of creation,
          or when they were last updated.
        - ``comments`` Filters issues based on the quantity of comments.
        - ``user`` or ``repo`` Limits searches to a specific user or
          repository.

        For more information about these qualifiers, see: http://git.io/d1oELA

        Example(s):
            gh search_issues "foo type:pr author:donnemartin"
            gh search_issues "foo in:title created:>=2015-01-01" | less

        Args:
            * query: A string representing the search query.

        Returns:
            None.
        """
        click.secho('Searching issues on GitHub...', fg='blue')
        issues = github.api.search_issues(query)
        table = []
        try:
            for issue in issues:
                table.append([issue.score,
                             issue.issue.number,
                             github.format_repo(issue.issue.repository),
                             issue.issue.title])
        except AttributeError:
            # github3.py sometimes throws the following during iteration:
            # AttributeError: 'NoneType' object has no attribute 'get'
            pass
        # Sort by score, repo, issue number
        table = sorted(table, key=itemgetter(0, 2, 1), reverse=True)
        github.print_table(table, headers=['score', '#', 'repo', 'title'])

    @cli.command('search_repos')
    @click.argument('query')
    @pass_github
    def search_repositories(github, query):
        """Searches all repos with the given query.

        The query can contain any combination of the following supported
        qualifers:

        - ``in`` Qualifies which fields are searched. With this qualifier you
          can restrict the search to just the repository name, description,
          readme, or any combination of these.
        - ``size`` Finds repositories that match a certain size (in
          kilobytes).
        - ``forks`` Filters repositories based on the number of forks, and/or
          whether forked repositories should be included in the results at
          all.
        - ``created`` or ``pushed`` Filters repositories based on times of
          creation, or when they were last updated. Format: ``YYYY-MM-DD``.
          Examples: ``created:<2011``, ``pushed:<2013-02``,
          ``pushed:>=2013-03-06``
        - ``user`` or ``repo`` Limits searches to a specific user or
          repository.
        - ``language`` Searches repositories based on the language they're
          written in.
        - ``stars`` Searches repositories based on the number of stars.

        For more information about these qualifiers, see: http://git.io/4Z8AkA

        Args:
            * query: A string representing the search query.

        Returns:
            None.
        """
        click.secho('Searching repos on GitHub...', fg='blue')
        repos = github.api.search_repositories(query)
        table = []
        number = 0
        try:
            for repo in repos:
                table.append([number,
                              repo.score,
                              repo.repository.full_name,
                              repo.repository.stargazers_count,
                              repo.repository.forks_count])
                number += 1
        except AttributeError:
            # github3.py sometimes throws the following during iteration:
            # AttributeError: 'NoneType' object has no attribute 'get'
            pass
        # Sort by score, repo
        table = sorted(table, key=itemgetter(1, 2), reverse=True)
        github.build_repo_urls(table, url_index=0, repo_index=2)
        github.print_table(table, headers=['#', 'score', 'repo',
                                           'stars', 'forks'])

    @cli.command()
    @click.argument('repo_filter', required=False, default='')
    @pass_github
    def starred(github, repo_filter):
        """Outputs starred repos.

        Example(s):
            gh starred foo

        Args:
            * repo_filter: A string representing a filter for repo names.
                Only repos matching the filter will be returned.
                If None, outputs all starred repos.

        Returns:
            None.
        """
        github.repositories(github.api.starred(), repo_filter.lower())
