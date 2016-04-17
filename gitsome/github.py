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

    @authenticate
    def issue(self, user_repo_number):
        """Outputs detailed information about the given issue.

        Args:
            * user_repo_number: A string representing the
                user/repo/issue number.

        Returns:
            None.
        """
        try:
            user, repo, number = user_repo_number.split('/')
            int(number)  # Check for int
        except ValueError:
            click.secho('Expected argument: user/repo/#.',
                        fg=self.config.clr_error)
            return
        url = ('https://github.com/' + user + '/' + repo + '/' +
               'issues/' + number)
        self.web_viewer.view_url(url)

    @authenticate
    def issues(self, issues_list, limit=1000, pager=False):
        """Lists all issues.

        Args:
            * issues_list: A list of github3.issue.issue.
            * limit: An int that specifies the number of items to show.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        view_entries = []
        for current_issue in issues_list:
            url = self.formatter.format_issues_url_from_issue(current_issue)
            repo_name = '/'.join(current_issue.repository)
            view_entries.append(
                ViewEntry(
                    current_issue,
                    url=url,
                    sort_key_primary=current_issue.state,
                    sort_key_secondary=current_issue.repository,
                    sort_key_tertiary=current_issue.created_at))
        view_entries = sorted(view_entries, reverse=False)
        self.table.build_table(view_entries,
                               limit,
                               pager,
                               self.formatter.format_issue)

    @authenticate
    def issues_setup(self, issue_filter='subscribed', issue_state='open',
                     limit=1000, pager=False):
        """Prepares to list all issues matching the filter.

        Args:
            * issue_filter: A string with the following accepted values:
                'assigned', 'created', 'mentioned', 'subscribed' (default).
            * issue_state: A string with the following accepted values:
                'all', 'open' (default), 'closed'.
            * limit: An int that specifies the number of items to show.
                Optional, defaults to 1000.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        self.issues(self.config.api.issues(issue_filter, issue_state),
                    limit,
                    pager)

    @authenticate
    def license(self, license_name):
        """Outputs the gitignore template for the given language.

        Args:
            * license_name: A string representing the license name.

        Returns:
            None.
        """
        result = self.config.api.license(license_name)
        if type(result) is not null.NullObject:
            click.secho(result.body, fg=self.config.clr_message)
        else:
            click.secho(('  Invalid case-sensitive license requested, run the '
                         'following command to see available licenses:\n'
                         '    gh licenses'),
                        fg=self.config.clr_error)

    @authenticate
    def licenses(self):
        """Outputs the gitignore template for the given language.

        Args:
            * None.

        Returns:
            None.
        """
        self.table.build_table_setup(
            self.config.api.licenses(),
            self.formatter.format_license_name,
            limit=sys.maxsize,
            pager=False,
            build_urls=False)
        click.secho(('  Run the following command to view or download a '
                     'LICENSE file:\n'
                     '    gh license apache-2.0\n'
                     '    gh license apache-2.0 > LICENSE\n'),
                    fg=self.config.clr_message)

    @authenticate
    def notifications(self, limit=1000, pager=False):
        """Lists all notifications.

        Args:
            * limit: An int that specifies the number of items to show.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        view_entries = []
        for thread in self.config.api.notifications(all=True,
                                                    participating=False):
            url = self.formatter.format_issues_url_from_thread(thread)
            view_entries.append(ViewEntry(thread, url=url))
        self.table.build_table(view_entries,
                               limit,
                               pager,
                               self.formatter.format_thread)

    @authenticate
    def octocat(self, say):
        """Outputs an Easter egg or the given message from Octocat.

        Args:
            * say: A string for octocat to say.
                If say is None, octocat speaks an Easter egg.

        Returns:
            None.
        """
        output = str(self.config.api.octocat(say))
        output = output.replace('\\n', '\n')
        click.secho(output, fg=self.config.clr_message)

    @authenticate
    def pull_requests(self, limit=1000, pager=False):
        """Lists all pull requests.

        Args:
            * limit: An int that specifies the number of items to show.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        issues_list = []
        repositories = self.config.api.repositories()
        for repository in repositories:
            repo_pulls = repository.pull_requests()
            for repo_pull in repo_pulls:
                issues_list.append(repo_pull)
        self.issues(issues_list, limit, pager)

    @authenticate
    def rate_limit(self):
        """Outputs the rate limit.

        Args:
            * None.

        Returns:
            None.
        """
        click.secho('Rate limit: ' + str(self.config.api.ratelimit_remaining),
                    fg=self.config.clr_message)

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

    @authenticate
    def repository(self, user_repo):
        """Outputs detailed information about the given repo.

        Args:
            * user_repo: A string representing the user/repo.

        Returns:
            None.
        """
        try:
            user, repo = user_repo.split('/')
        except ValueError:
            click.secho('Expected argument: user/repo.',
                        fg=self.config.clr_error)
            return
        self.web_viewer.view_url('https://github.com/' + user_repo)

    @authenticate
    def repositories(self, repos, limit=1000, pager=False,
                     repo_filter='', print_output=True):
        """Lists all repos matching the given filter.

        Args:
            * repos: A list of github3.repos.repo.
            * limit: An int that specifies the number of items to show.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.
            * repo_filter: A string representing a filter for repo names.
                Only repos matching the filter will be returned.
                If None, outputs all starred repos.
            * print_output: A bool that determines whether to print the output
                (True) or return the output as a string (False)

        Returns:
            A string representing the output if print_output is True
            else, returns None.
        """
        view_entries = []
        for repo in repos:
            url = repo.clone_url
            if (repo.full_name is not None and
                repo_filter in repo.full_name.lower()) or \
               (repo.description is not None and
                repo_filter in repo.description.lower()):
                view_entries.append(
                    ViewEntry(repo,
                              url=url,
                              sort_key_primary=repo.stargazers_count))
        view_entries = sorted(view_entries, reverse=True)
        return self.table.build_table(view_entries,
                                      limit,
                                      pager,
                                      self.formatter.format_repo,
                                      print_output=print_output)

    @authenticate
    def repositories_setup(self, repo_filter, limit=1000, pager=False):
        """Prepares to list all repos matching the given filter.

        Args:
            * repo_filter: A string representing a filter for repo names.
                Only repos matching the filter will be returned.
                If None, outputs all of the user's repos.
            * limit: An int that specifies the number of items to show.
                Optional, defaults to 1000.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        self.repositories(self.config.api.repositories(),
                          limit,
                          pager,
                          repo_filter)

    @authenticate
    def search_issues(self, query, limit=1000, pager=False):
        """Searches for all issues matching the given query.

        TODO: Fix sorting.

        Args:
            * query: A string representing the search query.
            * limit: An int that specifies the number of items to show.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        click.secho('Searching for all matching issues on GitHub...',
                    fg=self.config.clr_message)
        results = self.config.api.search_issues(query)
        issues_list = []
        for result in results:
            issues_list.append(result.issue)
        self.issues(issues_list, limit, pager)
