# coding: utf-8
import builtins
from operator import itemgetter
import os
import pickle
import re
import subprocess
import sys
import webbrowser
try:
    # Python 3
    import configparser
except ImportError:
    # Python 2
    import ConfigParser as configparser

import click
from github3 import login, null
from tabulate import tabulate
from gitsome.gitsome_command import GitSomeCommand
from xonsh.built_ins import iglobpath
from xonsh.tools import subexpr_from_unbalanced
from xonsh.tools import ON_WINDOWS


class GitHub(object):
    """Provides integration with the GitHub API.

    Attributes:
        * api: An instance of github3 to interact with the GitHub API.
        * APP_NAME: A string representing the app name used for obtaining
            a GitHub authorization token.
        * CONFIG: A string representing the config file name.
        * CONFIG_SECTION: A string representing the main config file section.
        * CONFIG_USER_ID: A string representing the user id config.
        * CONFIG_USER_PASS: A string representing the user pass config.
        * CONFIG_USER_TOKEN: A string representing the user token config.
        * CONFIG_URL: A string representing the jump to url config file name.
        * CONFIG_URL_SECTION: A string representing the jump to url config
            file section.
        * CONFIG_URL_LIST: A string representing the jump to url list in the
            config.
        * user_id: A string that represents the user's id in ~/.xonshrc
        * user_pass: A string that represents the user's pass in ~/.xonshrc
        * user_token: A string that represents the user's token in ~/.xonshrc
    """

    APP_NAME = 'GitHubCli'
    CONFIG = '.githubconfig'
    CONFIG_SECTION = 'github'
    CONFIG_USER_ID = 'user_id'
    CONFIG_USER_PASS = 'user_pass'
    CONFIG_USER_TOKEN = 'user_token'
    CONFIG_URL = '.githubconfigurl'
    CONFIG_URL_SECTION = 'url'
    CONFIG_URL_LIST = 'url_list'

    def __init__(self):
        """Inits GitSome.

        Args:
            * None.

        Returns:
            None.
        """
        self._login()

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

    def _github_config(self, config):
        """Attempts to find the github config file.

        Adapted from https://github.com/sigmavirus24/github-cli.

        Args:
            * config: A String that represents the config file name.

        Returns:
            A string containing the github config file.
        """
        home = os.path.abspath(os.environ.get('HOME', ''))
        config = os.path.join(home, config)
        return config

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
            self.user_id = parser.get(self.CONFIG_SECTION,
                                      self.CONFIG_USER_ID)
            self.api = login(token=parser.get(self.CONFIG_SECTION,
                                              self.CONFIG_USER_TOKEN),
                             two_factor_callback=self._two_factor_code)
        else:
            # Either the file didn't exist or we didn't have the correct
            # permissions
            self.user_id = ''
            while not user_id:
                user_id = input('Username: ')
            user_pass = ''
            while not user_pass:
                user_pass = getpass('Password: ')
            auth = None
            try:
                # Get an authorization for this
                auth = authorize(
                    user_id,
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
            parser.set(self.CONFIG_SECTION, self.CONFIG_USER_ID, user_id)
            parser.set(self.CONFIG_SECTION, self.CONFIG_USER_PASS, user_pass)
            parser.set(self.CONFIG_SECTION, self.CONFIG_USER_TOKEN, auth.token)
            self.api = login(token=auth.token,
                             two_factor_callback=self._two_factor_code)
            # Create the file if it doesn't exist. Otherwise completely blank
            # out what was there before. Kind of dangerous and destructive but
            # somewhat necessary
            parser.write(open(config, 'w+'))

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
        click.echo('\n' + issue.body)
        comments = issue.comments()
        for comment in comments:
            click.secho('\n--Comment by @' + str(comment.user) + '---\n',
                        fg='blue')
            click.echo(comment.body)

    def repository(self, user, repo_name):
        """Outputs detailed information about the given repo.

        If args does not contain user and repo, attempts to display repo
        information from the .git/ configured remote repo.

        Args:
            * user: A string representing the user login.
            * repo_name: A string representing the repo name.

        Returns:
            None.
        """
        repo = self.api.repository(user, repo_name)
        click.secho(repo.full_name, fg='blue')
        if repo.description:
            click.secho(repo.description, fg='blue')
        click.secho('Stars: ' + str(repo.stargazers_count) + ' | '
                    'Forks: ' + str(repo.forks_count),
                    fg='blue')
        click.secho('Url: ' + repo.clone_url, fg='blue')

    def repositories(self):
        """Lists all repos.

        Args:
            * None.

        Returns:
            None.
        """
        repos = self.api.repositories()
        table = []
        for repo in repos:
            table.append([repo.name, repo.stargazers_count])
        table = sorted(table, key=itemgetter(1, 0), reverse=True)
        self._print_table(table, headers=['repo', 'stars'])


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
    @click.argument('user_id', required=False)
    @pass_github
    def followers(github, user_id):
        """Lists all followers and the total follower count.

        Args:
            * user_id: A string representing the user login.
                If None, returns followers of the logged in user.

        Returns:
            None.
        """
        if user_id is None:
            user_id = github.user_id
        users = github.api.followers_of(user_id)
        table = []
        for user in users:
            table.append([user.login, user.html_url])
        github._print_table(table, headers=['user', 'profile'])
        click.secho(
            'Followers: ' + str(github.api.user(user_id).followers_count),
            fg='blue')

    @cli.command()
    @click.argument('user', required=False)
    @pass_github
    def following(github, user):
        """Lists all followed users and the total followed count.

        Args:
            * user: A string representing the user login.
                If None, returns the followed users of the logged in user.

        Returns:
            None.
        """
        if user is None:
            user = github.user_id
        github._print_items(
            github._listify(github.api.followed_by(user)), headers=['user'])
        click.echo('Following ' + github.api.user(user).following_count)

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
        if template != '':
            click.secho(template, fg='red')
        else:
            click.echo('Invalid template requested, run the following ' \
                       'command to see available templates:\n' \
                       '    gh gitignore_templates')

    @cli.command()
    @pass_github
    def gitignore_templates(github):
        """Outputs all supported gitignore templates.

        Args:
            * None.

        Returns:
            None.
        """
        github._print_items(
            github._listify(github.api.gitignore_templates()),
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
    @pass_github
    def issues(github, issue_filter):
        """Lists all issues.

        Args:
            * filter: 'assigned', 'created', 'mentioned', 'subscribed'.

        Returns:
            None.
        """
        issues = github.api.issues(filter=issue_filter)
        table = []
        for issue in issues:
            table.append([issue.number,
                          github._format_repo(issue.repository),
                          issue.title,
                          issue.comments_count])
        # Sort by repo, issue number
        table = sorted(table, key=itemgetter(1, 0))
        github._print_table(table,
                            headers=['#', 'repo', 'title', 'comments'])

    @cli.command()
    @pass_github
    def me(github):
        """Lists information about the logged in user.

        Args:
            * None.

        Returns:
            None.
        """
        user = github.api.me()
        click.echo(user.login)
        if user.company is not None:
            click.echo('company:', user.company)
        if user.location is not None:
            click.echo('location:', user.location)
        if user.email is not None:
            click.echo('email: ' + user.email)
        click.echo('joined on: ' + str(user.created_at))
        click.echo('followers: ' + str(user.followers_count))
        click.echo('following: ' + str(user.following_count))
        github.repositories()

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
        github._print_items(github.api.notifications(participating=True),
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
        url = 'https://github.com/' + github.user_id
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
        github._print_table(table, headers=['#', 'repo', 'title'])

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

    @cli.command()
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
        repo = github.api.repository(user, repo_name)
        click.echo('description: ' + repo.description)
        click.echo('stars: ' + str(repo.stargazers_count))
        click.echo('forks: ' + str(repo.forks_count))
        click.echo('created at: ' + str(repo.created_at))
        click.echo('updated at: ' + str(repo.updated_at))
        click.echo('clone url: ' + repo.clone_url)

    @cli.command()
    @pass_github
    def repositories(github):
        """Lists all repos.

        Args:
            * None.

        Returns:
            None.
        """
        github.repositories()

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
        issues = github.api.search_issues(query)
        table = []
        try:
            for issue in issues:
                table.append([issue.score,
                             issue.issue.number,
                             github._format_repo(issue.issue.repository),
                             issue.issue.title])
        except AttributeError:
            # github3.py sometimes throws the following during iteration:
            # AttributeError: 'NoneType' object has no attribute 'get'
            pass
        # Sort by score, repo, issue number
        table = sorted(table, key=itemgetter(0, 2, 1), reverse=True)
        github._print_table(table, headers=['score', '#', 'repo', 'title'])

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
        repos = github.api.search_repositories(query)
        table = []
        try:
            for repo in repos:
                table.append([repo.score,
                              repo.repository.stargazers_count,
                              repo.repository.forks_count,
                              repo.repository.full_name])
        except AttributeError:
            # github3.py sometimes throws the following during iteration:
            # AttributeError: 'NoneType' object has no attribute 'get'
            pass
        # Sort by score, repo
        table = sorted(table, key=itemgetter(0, 1), reverse=True)
        github._print_table(table, headers=['score', 'stars', 'forks', 'repo'])

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
        repos = github.api.starred()
        table = []
        repo_filter = repo_filter.lower()
        try:
            for repo in repos:
                if repo_filter in repo.full_name.lower() or \
                    repo_filter in repo.description.lower():
                    table.append([repo.stargazers_count,
                                  repo.forks_count,
                                  repo.full_name,
                                  repo.clone_url])
        except AttributeError:
            # github3.py sometimes throws the following during iteration:
            # AttributeError: 'NoneType' object has no attribute 'get'
            pass
        # Sort by repo
        table = sorted(table, key=itemgetter(0), reverse=True)
        github._print_table(
            table, headers=['stars', 'forks', 'repo', 'url'])
