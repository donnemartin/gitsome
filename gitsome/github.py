# coding: utf-8

# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

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

from .config import Config
from .formatter import Formatter
from .rss_feed import language_rss_map
from .table import Table
from .view_entry import ViewEntry
from .web_viewer import WebViewer


class GitHub(object):
    """Provides integration with the GitHub API.

    Attributes:
        * api: An instance of github3 to interact with the GitHub API.
        * config: An instance of Config.
        * formatter: An instance of Formatter.
        * table: An instance of Table.
        * trend_parser: An instance of feedparser.
        * web_viewer: An instance of WebViewer.
    """

    def __init__(self):
        """Inits GitHub.

        Args:
            * None.

        Returns:
            None.
        """
        self.config = Config()
        self.formatter = Formatter(self.config)
        self.table = Table(self.config)
        self.web_viewer = WebViewer(self.config)
        self.trend_parser = feedparser

    def authenticate(func):
        """Decorator that authenticates credentials.

        Args:
            * func: A method to execute if authorization passes.

        Returns:
            The return value of func if auth passes, or
                None if auth fails.
        """
        def auth_wrapper(self, *args, **kwargs):
            self.config.authenticate()
            self.config.save_config()
            if self.config.check_auth():
                return func(self, *args, **kwargs)
        return auth_wrapper

    def avatar(self, url, text_avatar):
        """Displays the user's avatar from the specified url.

        This method requires PIL.

        Args:
            * url: A string representing the user's avatar image.
            * text_avatar: A boolean that determines whether to view the profile
                avatar in plain text.

        Returns:
            avatar_text: A string representing the avatar.
        """
        avatar = self.config.get_github_config_path(
            self.config.CONFIG_AVATAR)
        urllib.request.urlretrieve(url, avatar)
        avatar_text = self.img2txt(avatar, ansi=(not text_avatar))
        avatar_text += '\n'
        os.remove(avatar)
        return avatar_text

    def avatar_setup(self, url, text_avatar):
        """Prepares to display the user's avatar from the specified url.

        This method requires PIL.

        Args:
            * url: A string representing the user's avatar image.
            * text_avatar: A boolean that determines whether to view the profile
                avatar in plain text.

        Returns:
            avatar_text: A string representing the avatar.
        """
        try:
            import PIL
            return self.avatar(url, text_avatar)
        except ImportError:
            avatar_text = click.style(('To view the avatar in your terminal, '
                                       'install the Python Image Library.\n'),
                                      fg=self.config.clr_message)
            return avatar_text

    def configure(self):
        """Configures gitsome.

        Args:
            * github: An instance of github.GitHub.

        Returns:
            None.
        """
        self.config.authenticate(overwrite=True)
        self.config.prompt_news_feed()
        self.save_config()

    @authenticate
    def create_comment(self, user_repo_number, text):
        """Creates a comment on the given issue.

        Args:
            * user_repo_number: A string representing the
                user/repo/issue number.
            * text: A string representing the comment text.

        Returns:
            None.
        """
        try:
            user, repo, number = user_repo_number.split('/')
            int(number)  # Check for int
        except ValueError:
            click.secho(('Expected argument: user/repo/# and option -t '
                         '"comment".'),
                        fg=self.config.clr_error)
            return
        issue = self.config.api.issue(user, repo, number)
        issue_comment = issue.create_comment(text)
        if type(issue_comment) is not null.NullObject:
            click.secho('Created comment: ' + issue_comment.body,
                        fg=self.config.clr_message)
        else:
            click.secho('Error creating comment',
                        fg=self.config.clr_error)

    @authenticate
    def create_issue(self, user_repo, issue_title, issue_desc=''):
        """Creates an issue.

        Args:
            * user_repo: A string representing the user/repo.
            * issue_title: A string representing the issue title.
            * issue_desc: A string representing the issue body (optional).

        Returns:
            None.
        """
        try:
            user, repo_name = user_repo.split('/')
        except ValueError:
            click.secho('Expected argument: user/repo and option -t "title".',
                        fg=self.config.clr_error)
            return
        issue = self.config.api.create_issue(user,
                                             repo_name,
                                             issue_title,
                                             issue_desc)
        if type(issue) is not null.NullObject:
            click.secho('Created issue: ' + issue.title + '\n' + issue.body,
                        fg=self.config.clr_message)
        else:
            click.secho('Error creating issue.', fg=self.config.clr_error)

    @authenticate
    def create_repo(self, repo_name, repo_desc='', private=False):
        """Creates a repo.

        Args:
            * repo_name: A string representing the repo name.
            * repo_desc: A string representing the repo description (optional).
            * private: A boolean that determines whether the repo is private.
                Default: False.

        Returns:
            None.
        """
        try:
            repo = self.config.api.create_repository(repo_name,
                                                     repo_desc,
                                                     private=private)
            click.secho(('Created repo: ' + repo.full_name + '\n' +
                         repo.description),
                        fg=self.config.clr_message)
        except UnprocessableEntity as e:
            click.secho('Error creating repo: ' + str(e.msg),
                        fg=self.config.clr_error)

    @authenticate
    def emails(self):
        """Lists all the user's registered emails.

        Args:
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        self.table.build_table_setup(self.config.api.emails(),
                                     self.formatter.format_email,
                                     limit=sys.maxsize,
                                     pager=False,
                                     build_urls=False)

    @authenticate
    def emojis(self, pager=False):
        """Lists all GitHub supported emojis.

        Args:
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        self.table.build_table_setup(self.config.api.emojis(),
                                     self.formatter.format_emoji,
                                     limit=sys.maxsize,
                                     pager=pager,
                                     build_urls=False)

    @authenticate
    def feed(self, user_or_repo='', private=False, pager=False):
        """Lists all activity for the given user or repo.

        If blank, lists the logged in user's news feed.

        Args:
            * user_or_repo: A string representing the user or repo to list
                events for.  If no entry, defaults to the logged in user's feed.
            * private: A boolean that determines whether to show the private
                events (True) or public events (False).
                Only works for the currently logged in user.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        click.secho('Listing events...', fg=self.config.clr_message)
        if user_or_repo == '':
            if self.config.user_feed is None:
                self.config.prompt_news_feed()
                self.config.save_config()
            if self.config.user_feed:
                items = self.trend_parser.parse(self.config.user_feed)
                self.table.build_table_setup_feed(
                    items,
                    self.formatter.format_feed_entry,
                    pager)
        else:
            if '/' in user_or_repo:
                user, repo = user_or_repo.split('/')
                repo = self.config.api.repository(user, repo)
                items = repo.events()
            else:
                public = False if private else True
                items = self.config.api.user(user_or_repo).events(public=public)
            self.table.build_table_setup(
                items,
                self.formatter.format_event,
                limit=sys.maxsize,
                pager=pager,
                build_urls=False)

    @authenticate
    def followers(self, user, pager=False):
        """Lists all followers and the total follower count.

        Args:
            * user: A string representing the user login.
                If None, returns followers of the logged in user.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        if user is None:
            user = self.config.user_login
        self.table.build_table_setup_user(
            self.config.api.followers_of(user),
            self.formatter.format_user,
            limit=sys.maxsize,
            pager=pager)

    @authenticate
    def following(self, user, pager=False):
        """Lists all followed users and the total followed count.

        Args:
            * user: A string representing the user login.
                If None, returns the followed users of the logged in user.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        if user is None:
            user = self.config.user_login
        self.table.build_table_setup_user(
            self.config.api.followed_by(user),
            self.formatter.format_user,
            limit=sys.maxsize,
            pager=pager)

    @authenticate
    def gitignore_template(self, language):
        """Outputs the gitignore template for the given language.

        Args:
            * language: A string representing the language.

        Returns:
            None.
        """
        template = self.config.api.gitignore_template(language)
        if template:
            click.secho(template, fg=self.config.clr_message)
        else:
            click.secho(('Invalid case-sensitive template requested, run the '
                         'following command to see available templates:\n'
                         '    gh gitignores'),
                        fg=self.config.clr_error)

    @authenticate
    def gitignore_templates(self, pager=False):
        """Outputs all supported gitignore templates.

        Args:
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        self.table.build_table_setup(
            self.config.api.gitignore_templates(),
            self.formatter.format_gitignore_template_name,
            limit=sys.maxsize,
            pager=pager,
            build_urls=False)
        click.secho(('  Run the following command to view or download a '
                     '.gitignore file:\n'
                     '    View:     gh gitignore Python\n'
                     '    Downlaod: gh gitignore Python > .gitignore\n'),
                    fg=self.config.clr_message)

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
