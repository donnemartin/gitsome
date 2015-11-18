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

    def __init__(self):
        """Inits GitHub.

        Args:
            * None.

        Returns:
            None.
        """
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

    def avatar(self, url, output_type):
        """Displays the user's avatar from the specified url.

        Args:
            * output_type: A string representing the profile output type:
                'text': Sets the output to render in plain text.
                'ansi': Sets the output to render in ansi.

        Returns:
            None.
        """
        avatar = self._github_config(self.CONFIG_AVATAR)
        urllib.request.urlretrieve (url, avatar)
        ansi = True
        if output_type == 'text':
            ansi = False
        img2txt(avatar, ansi=ansi)
        os.remove(avatar)

    def build_repo_urls(self, table, url_index, repo_index):
        """Builds the GitHub urls for the input table containing repo names.

        Note: This method modifies the table's url_index, adding a
        0-based index that allow you to access a repo url with the
        gh open [url_index] command.

        Args:
            * table: A list that contains repo information.
            * url_index: The index in the table that will allow you to
                access a repo url with the gh open [url_index] command.
            * repo_index: The index in the table containing the repo name.

        Returns:
            None.
        """
        click.secho('Tip: Open repo urls with the following command:\n' \
                    '    gh open [#].', fg='blue')
        number = 0
        for row in table:
            row[0] = number
            number += 1
            self.urls.append('https://github.com/' + row[repo_index])
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

    def issue(self, user, repo, issue_number):
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
        click.secho('#' + str(issue.number) + ': ' + \
                   issue.title + ' - ' + \
                   '@' + str(issue.user) + ' [' + \
                   issue.state + ']',
                   fg='blue')
        click.secho('Assignee: ' + str(issue.assignee), fg='blue')
        click.echo('\n' + issue.body)
        comments = issue.comments()
        for comment in comments:
            click.secho('\n--Comment by @' + str(comment.user) + '---\n',
                        fg='blue')
            click.echo(comment.body)

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

    def open(self, index):
        """Opens the given index in a browser.

        Loads urls from .githubconfigurl and stores them in self.urls.

        Args:
            * index: An int that specifies the index to open in a browser.

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
            self.urls = urls.split(', ')
            webbrowser.open(self.urls[index])
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

    def repository(self, user, repo_name, num_readme_lines=25):
        """Outputs detailed information about the given repo.

        If args does not contain user and repo, attempts to display repo
        information from the .git/ configured remote repo.

        Args:
            * user: A string representing the user login.
            * repo_name: A string representing the repo name.
            * num_readme_lines: An int that determines the number of lines
                to display for the README.

        Returns:
            None.
        """
        repo = self.api.repository(user, repo_name)
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
        click.secho('--First ' + str(num_readme_lines) + \
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
        # Create a GitHub object and remember it as as the context object.
        # From this point onwards other commands can refer to it by using the
        # @pass_github decorator.
        ctx.obj = GitHub()

    @cli.command()
    @click.argument('index')
    @pass_github
    def open(github, index):
        """Opens the given index in a browser.

        This method is meant to be called after one of the following commands
        which outputs a table of repos or issues:

            * gh repositories
            * gh search_repositories
            * gh starred

            * gh issues
            * gh pull_requests
            * gh search_issues

        Args:
            * index: An int that specifies the index to open in a browser.
                For example, calling gh repositories will list repos with a
                0-based index for each repo.  Calling gh open [index] will
                open the url for the associated repo in a browser.

        Returns:
            None.
        """
        github.open(int(index))

    @cli.command()
    @click.argument('user')
    @click.argument('repo')
    @click.argument('issue_title')
    @pass_github
    def create_issue(github, user, repo, issue_title):
        """Creates an issue.

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
    @click.argument('repo_name')
    @pass_github
    def create_repo(github, repo_name):
        """Creates a repo.

        Args:
            * repo_name: A string representing the repo name.

        Returns:
            None.
        """
        repo = github.api.create_repository(repo_name)
        click.secho('Created repo: ' + repo.full_name, fg='blue')

    @cli.command()
    @pass_github
    def emails(github):
        """Lists all the user's registered emails.

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

        Args:
            * None.

        Returns:
            None.

        Raises:
            TypeError: Seems to be a github3.py bug.
        """
        github.api.feeds()

    @cli.command()
    @click.argument('user_login', required=False)
    @pass_github
    def followers(github, user_login):
        """Lists all followers and the total follower count.

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

        Args:
            * None.

        Returns:
            None.
        """
        github.print_items(
            github.listify(github.api.gitignore_templates()),
                           headers=['language'])

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
        github.issue(user, repo, issue_number)

    @cli.command()
    @click.argument('issue_filter', required=False, default='subscribed')
    @click.argument('state', required=False, default='open')
    @pass_github
    def issues(github, issue_filter, state):
        """Lists all issues.

        Args:
            * filter: A string with the following accepted values:
                'assigned', 'created', 'mentioned', 'subscribed'.
            * state: A string with the following accepted values:
                'all', 'open', 'closed'.

        Returns:
            None.
        """
        issues = github.api.issues(filter=issue_filter, state=state)
        table = []
        for issue in issues:
            table.append([issue.state,
                          github.format_repo(issue.repository),
                          issue.number,
                          issue.title + ' @' + str(issue.user),
                          str(issue.assignee),
                          issue.comments_count])
        # Sort by repo, state, issue number
        table = sorted(table, key=itemgetter(1, 0, 2))
        github.print_table(table,
                           headers=['state', 'repo', '#',
                                    'title', 'assignee', 'comments'])

    @cli.command()
    @click.option('profile_output', '--text-profile',
                  flag_value='text', default=False,
                  help='Output profile in plain text.')
    @click.option('profile_output', '--ansi-profile',
                  flag_value='ansi', default=True,
                  help='Output profile in ansi.')
    @pass_github
    def me(github, profile_output):
        """Lists information about the logged in user.

        Args:
            * profile_output: A string representing the profile output type:
                --text-profile: profile_output = 'text'
                    Sets the output to render in plain text.
                --text-ansi: profile_output = 'ansi' (default)
                    Sets the output to render in ansi.

        Returns:
            None.
        """
        user = github.api.me()
        github.avatar(user.avatar_url, profile_output)
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

        Args:
            * None.

        Returns:
            None.
        """
        github.print_items(github.api.notifications(participating=True),
                           headers=['notification'])

    @cli.command()
    @click.argument('say', required=False)
    @pass_github
    def octocat(github, say):
        """Outputs an Easter egg or the given message from Octocat.

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
    @pass_github
    def profile(github):
        """Opens a web browser to your GitHub profile.

        Args:
            * None.

        Returns:
            None.
        """
        url = 'https://github.com/' + github.user_login
        webbrowser.open(url)

    @cli.command()
    @click.argument('user')
    @click.argument('repo')
    @click.argument('issue_number')
    @pass_github
    def pull_request(github, user, repo, issue_number):
        """Outputs detailed information about the given pull request.

        Args:
            * user: A string representing the user login.
            * repo: A string representing the repo name.
            * issue_number: An int representing the issue number.

        Returns:
            None.
        """
        github.issue(user, repo, issue_number)

    @cli.command()
    @pass_github
    def pull_requests(github):
        """Lists all pull requests.

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
            user, repo_name = pull_request.repository
            repo = user.strip('repos/') + '/' + repo_name
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

        Args:
            * None.

        Returns:
            None.
        """
        click.echo('Rate limit: ' + str(github.api.ratelimit_remaining))

    @cli.command('repo')
    @click.argument('user')
    @click.argument('repo_name')
    @pass_github
    def repository(github, user, repo_name):
        """Outputs detailed information about the given repo.

        If args does not contain user and repo, attempts to display repo
        information from the .git/ configured remote repo.

        Args:
            * user: A string representing the user login.
            * repo_name: A string representing the repo name.

        Returns:
            None.
        """
        github.repository(user, repo_name)

    @cli.command('repos')
    @pass_github
    def repositories(github):
        """Lists all repos.

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

    @cli.command()
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

        Args:
            * repo_filter: A string representing a filter for repo names.
                Only repos matching the filter will be returned.
                If None, outputs all starred repos.

        Returns:
            None.
        """
        github.repositories(github.api.starred(), repo_filter.lower())
