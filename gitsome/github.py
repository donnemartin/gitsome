import re
import requests
import os
import re
import builtins
import pickle
import subprocess
import sys
from operator import itemgetter

from github3 import login, null
from tabulate import tabulate
from gitsome.gitsome_command import GitSomeCommand
from xonsh.built_ins import iglobpath
from xonsh.tools import subexpr_from_unbalanced
from xonsh.tools import ON_WINDOWS
from xonsh.environ import repo_from_remote


class GitSome(object):
    """Provides integration with the GitHub API.

    Attributes:
        * repo: A string that represents the user's current repo, as
            determined by the .git/ configured remote repo.
    """

    EMAILS = 'emails'
    EMOJIS = 'emojis'
    EVENTS = 'events'
    FEEDS = 'feeds'
    FOLLOWERS = 'followers'
    FOLLOWING = 'following'
    GITIGNORE_TEMPLATE = 'gitignore_template'
    GITIGNORE_TEMPLATES = 'gitignore_templates'
    ISSUE = 'issue'
    ISSUES = 'issues'
    ME = 'me'
    NOTIFICATIONS = 'notifications'
    OCTOCAT = 'octocat'
    RATE_LIMIT = 'rate_limit'
    REPO = 'repo'
    REPOS = 'repos'
    SEARCH_ISSUES = 'search_issues'
    SEARCH_REPOSITORIES = 'search_repositories'
    STARRED = 'starred'
    STARS = 'stars'

    def __init__(self):
        """Inits GitSome.

        Args:
            * None.

        Returns:
            None.
        """
        self._login()
        self.repo = repo_from_remote()
        self.rate_limit()
        self._init_dispatch()

    def _extract_args(self, input_args, command):
        """Extracts arguments using the input or default args.

        Args:
            * input_args: A list that represents the user's input args.
            * default_args: A list that represents the default args to be used
                if the input_args are not provided.
            * expected_args_count: An int represents the number of expected
                args to be passed in for the method to work properly.

        Returns:
            An single arg if there is one valid arg.
            A list of args if there are multiple args.
            None if the args are invalid.
        """
        default_args = self.dispatch[command].default_args
        expected_args_count = self.dispatch[command].expected_args_count
        # If we don't have input args, use the default args if they exist
        if not input_args and default_args is not None:
            return self._return_elem_or_list(default_args)
        valid_args = True
        # If we expect args and the we don't get any args or
        # if the number of input args doesn't match the number of expected args
        if (expected_args_count != 0 and input_args is None) or \
            len(input_args) != expected_args_count:
            valid_args = False
        if not valid_args:
            expected_args_desc = self.dispatch[command].expected_args_desc
            print('Error, expected arguments:', expected_args_desc)
            return None
        else:
            # All checks pass on the input args for use
            return self._return_elem_or_list(input_args)
        return None

    def _format_repo(self, repo):
        """Formats a repo tuple for pretty print.

        Example:
            Input:  ('donnemartin', 'gitsome')
            Output: donnemartin/gitsome

        Args:
            * arg: A tuple that contains the user and repo.

        Returns:
            A string of the form user/repo.
        """
        return '/'.join(repo)

    def _init_dispatch(self):
        """Initializes the dispatch dictionary.

        The dictionary keys are commands and values are methods.

        Args:
            * None.

        Returns:
            None.
        """
        self.dispatch = {
            self.EMAILS: GitSomeCommand(
                command=self.EMAILS,
                expected_args_count=0,
                expected_args_desc='',
                default_args=None,
                method=self.emails),
            self.EMOJIS: GitSomeCommand(
                command=self.EMOJIS,
                expected_args_count=0,
                expected_args_desc='',
                default_args=None,
                method=self.emojis),
            self.EVENTS: GitSomeCommand(
                command=self.EVENTS,
                expected_args_count=0,
                expected_args_desc='',
                default_args=None,
                method=self.events),
            self.FEEDS: GitSomeCommand(
                command=self.FEEDS,
                expected_args_count=0,
                expected_args_desc='',
                default_args=None,
                method=self.feeds),
            self.FOLLOWERS: GitSomeCommand(
                command=self.FOLLOWERS,
                expected_args_count=1,
                expected_args_desc=\
                    'user (optional)',
                default_args=[self.user_id],
                method=self.followers),
            self.FOLLOWING: GitSomeCommand(
                command=self.FOLLOWING,
                expected_args_count=1,
                expected_args_desc=\
                    'user (optional)',
                default_args=[self.user_id],
                method=self.following),
            self.GITIGNORE_TEMPLATE: GitSomeCommand(
                command=self.GITIGNORE_TEMPLATE,
                expected_args_count=1,
                expected_args_desc='language',
                default_args=None,
                method=self.gitignore_template),
            self.GITIGNORE_TEMPLATES: GitSomeCommand(
                command=self.GITIGNORE_TEMPLATES,
                expected_args_count=0,
                expected_args_desc='',
                default_args=None,
                method=self.gitignore_templates),
            self.ISSUE: GitSomeCommand(
                command=self.ISSUE,
                expected_args_count=3,
                expected_args_desc='user, repo, issue number',
                default_args=None,
                method=self.issue),
            self.ISSUES: GitSomeCommand(
                command=self.ISSUES,
                expected_args_count=1,
                expected_args_desc=\
                    'filter: assigned created mentioned or subscribed',
                default_args=['subscribed'],
                method=self.issues),
            self.ME: GitSomeCommand(
                command=self.ME,
                expected_args_count=0,
                expected_args_desc='',
                default_args=None,
                method=self.me),
            self.NOTIFICATIONS: GitSomeCommand(
                command=self.NOTIFICATIONS,
                expected_args_count=0,
                expected_args_desc='',
                default_args=None,
                method=self.notifications),
            self.OCTOCAT: GitSomeCommand(
                command=self.OCTOCAT,
                expected_args_count=1,
                expected_args_desc=\
                    'speak (optional)',
                default_args=[''],
                method=self.octocat),
            self.RATE_LIMIT: GitSomeCommand(
                command=self.RATE_LIMIT,
                expected_args_count=1,
                expected_args_desc=\
                    'threshold (optional)',
                default_args=[sys.maxsize],
                method=self.rate_limit),
            self.REPO: GitSomeCommand(
                command=self.REPO,
                expected_args_count=2,
                expected_args_desc='user, repo',
                default_args=[self.user_id, self.repo],
                method=self.repository),
            self.REPOS: GitSomeCommand(
                command=self.REPOS,
                expected_args_count=0,
                expected_args_desc='',
                default_args=None,
                method=self.repositories),
            self.SEARCH_ISSUES: GitSomeCommand(
                command=self.SEARCH_ISSUES,
                expected_args_count=1,
                expected_args_desc='query',
                default_args=[None],
                method=self.search_issues),
            self.SEARCH_REPOSITORIES: GitSomeCommand(
                command=self.SEARCH_REPOSITORIES,
                expected_args_count=1,
                expected_args_desc='query',
                default_args=[None],
                method=self.search_repositories),
            self.STARRED: GitSomeCommand(
                command=self.STARRED,
                expected_args_count=1,
                expected_args_desc='query (optional)',
                default_args=[''],
                method=self.starred),
            self.STARS: GitSomeCommand(
                command=self.STARS,
                expected_args_count=2,
                expected_args_desc=\
                    'user, repo',
                default_args=None,
                method=self.stars),
        }

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
        self.token = get_env('GITHUB_TOKEN', None)
        if self.token is not None and False:
            self.gh = login(token=self.token,
                            two_factor_callback=self._two_factor_code)
            print('Authenticated with token:', self.gh.me().login)
        else:
            self.gh = login(self.user_id,
                            self.user_pass,
                            two_factor_callback=self._two_factor_code)
            print('Authenticated with user id and password:',
                  self.gh.me().login)

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
        print(tabulate(table, headers, tablefmt='grid'))

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

    def emails(self, _=None):
        """Lists all the user's registered emails.

        Args:
            * None.

        Returns:
            None.
        """
        self._print_items(self.gh.emails(), headers='keys')

    def emojis(self, _=None):
        """Lists all GitHub supported emojis.

        Args:
            * None.

        Returns:
            None.
        """
        self._print_items(self._listify(self.gh.emojis()), headers=['emoji'])

    def events(self, _=None):
        """Lists all public events.

        Args:
            * None.

        Returns:
            None.
        """
        events = self.gh.all_events()
        table = []
        for event in events:
            table.append([event.created_at,
                          event.actor,
                          event.type,
                          self._format_repo(event.repo)])
        self._print_table(table,
                          headers=['created at', 'user', 'type', 'repo'])

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
        if args:
            self.repo = repo_from_remote()
            command = args[0]
            command_args = args[1:] if args[1:] else None
            self.dispatch[command].method(command_args)
            rate_limit_print_threshold = 20
            self.rate_limit([rate_limit_print_threshold])
        else:
            print("Available commands for 'gh':")
            table = []
            for command in self.dispatch.values():
                table.append([command.command, command.expected_args_desc])
            # Sort by command
            table = sorted(table, key=itemgetter(0))
            self._print_table(table, headers=['command', 'expected args'])

    def feeds(self, _=None):
        """Lists GitHub's timeline resources.

        Requires authentication with user/pass, cannot be used with tokens
        due to a limitation with the GitHub API itself.

        TODO: Results in an exception with github3.py.

        Args:
            * None.

        Returns:
            A type that does xxx.

        Raises:
            TypeError: github3.py bug.
        """
        self.gh.feeds()

    def followers(self, args):
        """Lists all followers and the total follower count.

        If args is None, returns the followers and count for the currently
            logged in user.
        Else, returns the followers and count for the specified user.

        Args:
            * args: A list containing a single user or None.

        Returns:
            None.
        """
        user = self._extract_args(args, self.FOLLOWERS)
        self._print_items(
            self._listify(self.gh.followers_of(user)), headers=['user'])
        print('Followers:', self.gh.user(user).followers_count)

    def following(self, args):
        """Lists all followed users and the total followed count.

        If args is None, returns the followed users and count for the currently
            logged in user.
        Else, returns the followed users and count for the specified user.

        Args:
            * args: A list containing a single user or None.

        Returns:
            None.
        """
        user = self._extract_args(args, self.FOLLOWING)
        self._print_items(
            self._listify(self.gh.followed_by(user)), headers=['user'])
        print('Following:', self.gh.user(user).following_count)

    def gitignore_template(self, args):
        """Outputs the gitignore template for the given language.

        Args:
            * arg: A string that represents the language.

        Returns:
            None.
        """
        language = self._extract_args(args, self.GITIGNORE_TEMPLATE)
        template = self.gh.gitignore_template(language)
        if template != '':
            print(template)
        else:
            print('Invalid template requested, run the following command to' \
                  ' see available templates:\n    gh gitignore_templates')

    def gitignore_templates(self, _=None):
        """Outputs all supported gitignore templates.

        Args:
            * None.

        Returns:
            None.
        """
        self._print_items(
            self._listify(self.gh.gitignore_templates()), headers=['language'])

    def issue(self, args):
        """Outputs detailed information about the given issue.

        Args:
            * args: A list that contains the user, repo, and issue id.

        Returns:
            None.
        """
        result = self._extract_args(args, self.ISSUE)
        if result is None:
            return
        user, repo, issue_number = result
        issue = self.gh.issue(user, repo, issue_number)
        if type(issue) is null.NullObject:
            print('Error: Invalid issue.')
            return
        print('repo:', self._format_repo(issue.repository))
        print('title:', issue.title)
        print('issue url:', issue.html_url)
        print('issue number:', issue.number)
        print('state:', issue.state)
        print('comments:', issue.comments_count)
        print('labels:', issue.original_labels)
        print('milestone:', issue.milestone)
        print('')
        print(issue.body)
        comments = issue.comments()
        for comment in comments:
            print('')
            print('---Comment---')
            print('')
            print('user:', comment.user)
            print('comment url:', comment.html_url)
            print('created at:', comment.created_at)
            print('updated at:', comment.updated_at)
            print('')
            print(comment.body)

    def issues(self, args):
        """Lists all issues.

        Args:
            * args: A list that contains an issue filter:
                'assigned', 'created', 'mentioned', 'subscribed'.

        Returns:
            None.
        """
        issue_filter = self._extract_args(args, self.ISSUES)
        issues = self.gh.issues(filter=issue_filter)
        table = []
        for issue in issues:
            table.append([issue.number,
                          self._format_repo(issue.repository),
                          issue.title,
                          issue.comments_count])
        table = sorted(table, key=itemgetter(1, 0))
        self._print_table(table,
                          headers=['#', 'repo', 'title', 'comments'])

    def me(self, _=None):
        """Lists information about the logged in user.

        Args:
            * None.

        Returns:
            None.
        """
        user = self.gh.me()
        print(user.login)
        if user.company is not None:
            print('company:', user.company)
        if user.location is not None:
            print('location:', user.location)
        if user.email is not None:
            print('email:', user.email)
        print('joined on:', user.created_at)
        print('followers:', user.followers_count)
        print('following:', user.following_count)
        self.repositories()

    def notifications(self, args):
        """Lists all notifications.

        TODO: Always results in an empty list.

        Args:
            * arg: A type that does xxx.

        Returns:
            None.
        """
        notifs = self.gh.notifications(participating=True)
        self._print_items(self.gh.notifications(participating=True),
                          headers=['foo'])

    def octocat(self, args):
        """Outputs an Easter egg or the given message from Octocat.

        If args is None, Octocat responds with an Easter egg.
        Else, Octocats responds with the given string.

        Args:
            * args: A list that contains the string for octocat to say, or None.

        Returns:
            None.
        """
        say = self._extract_args(args, self.OCTOCAT)
        output = str(self.gh.octocat(say))
        output = output.replace('\\n', '\n')
        print(output)

    def rate_limit(self, args=None):
        """Outputs the rate limit.

        Args:
            * args: A list that contains an int representing the threshold.
                The rate limit is shown if it falls below the threshold.

        Returns:
            None.
        """
        threshold = int(self._extract_args(args, self.RATE_LIMIT))
        limit = self.gh.ratelimit_remaining
        if limit < threshold:
            print('Rate limit:', limit)

    def repository(self, args):
        """Outputs detailed information about the given repo.

        If args does not contain user and repo, attempts to display repo
        information from the .git/ configured remote repo.

        Args:
            * arg: A list that contains user and repo, or None.

        Returns:
            None.
        """
        user, repo = self._extract_args(args, self.REPO)
        repository = self.gh.repository(user, repo)
        print('description:', repository.description)
        print('stars:', repository.stargazers_count)
        print('forks:', repository.forks_count)
        print('created at:', repository.created_at)
        print('updated at:', repository.updated_at)
        print('clone url:', repository.clone_url)

    def repositories(self, _=None):
        """Lists all repos.

        Args:
            * None.

        Returns:
            None.
        """
        repos = self.gh.repositories()
        table = []
        for repo in repos:
            table.append([repo.name, repo.stargazers_count])
        table = sorted(table, key=itemgetter(1, 0), reverse=True)
        print(tabulate(table, headers=['repo', 'stars'], tablefmt='grid'))

    def search_issues(self, args):
        """Searches all issues with the given query.

        Args:
            * args: A list that contains a string representing the query.

        Returns:
            None.
        """
        query = self._extract_args(args, self.SEARCH_ISSUES)
        issues = self.gh.search_issues(query)
        table = []
        try:
            for issue in issues:
                table.append([issue.score,
                             issue.issue.number,
                             self._format_repo(issue.issue.repository),
                             issue.issue.title])
        except AttributeError:
            # github3.py sometimes throws the following during iteration:
            # AttributeError: 'NoneType' object has no attribute 'get'
            pass
        # Sort by score, repo, issue number
        table = sorted(table, key=itemgetter(0, 2, 1), reverse=True)
        self._print_table(table, headers=['score', '#', 'repo', 'title'])

    def search_repositories(self, args):
        """Searches all repos with the given query.

        Args:
            * args: A list that contains a string representing the query.

        Returns:
            None.
        """
        query = self._extract_args(args, self.SEARCH_REPOSITORIES)
        repos = self.gh.search_repositories(query)
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
        self._print_table(table, headers=['score', 'stars', 'forks', 'repo'])

    def starred(self, args):
        """Outputs starred repos.

        If args contains a query, it will output matching starred repos.
        Else, it will output all starred repos.

        Args:
            * args: A list that contains query, or None.

        Returns:
            None.
        """
        query = self._extract_args(args, self.STARRED)
        repos = self.gh.starred()
        table = []
        try:
            for repo in repos:
                if query in repo.full_name or \
                    query in repo.description:
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
        self._print_table(
            table, headers=['stars', 'forks', 'repo', 'url'])

    def stars(self, args):
        """Outputs the number of stars for the given repo.

        If no repo is given, attempts to display repo information from the
        .git/ configured remote repo.

        Args:
            * args: A list that contains a string representing the repo.

        Returns:
            None.
        """
        user, repo = self._extract_args(args, self.STARS)
        stars = str(self.gh.repository(user, repo).stargazers_count)
        print('Stars for ' + user + '/' + repo + ': ' + stars)
