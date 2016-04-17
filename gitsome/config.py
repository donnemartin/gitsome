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

import os

from .compat import configparser
from .lib.github3 import authorize, login


class Config(object):
    """GitSome config.

    Attributes:
        * CONFIG: A string representing the config file name.
        * CONFIG_SECTION: A string representing the main config file section.
        * CONFIG_USER_LOGIN: A string representing the user login config.
        * CONFIG_USER_PASS: A string representing the user pass config.
        * CONFIG_USER_TOKEN: A string representing the user token config.
        * CONFIG_USER_FEED: A string representing the user feed config.  This
            is the feed on https://github.com/ when logged in and requires the
            basic auth model, which doesn't work when logging in with tokens or
            2FA.  This config listed the pre-signed url to access the feed.
        * CONFIG_URL: A string representing the jump to url config file name.
        * CONFIG_URL_SECTION: A string representing the jump to url config
            file section.
        * CONFIG_URL_LIST: A string representing the jump to url list in the
            config.
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
    CONFIG_USER_FEED = 'user_feed'
    CONFIG_URL = '.githubconfigurl'
    CONFIG_URL_SECTION = 'url'
    CONFIG_URL_LIST = 'url_list'
    CONFIG_AVATAR = '.githubconfigavatar.png'

    def __init__(self):
        """Inits Config.

        Args:
            * None.

        Returns:
            None.
        """
        self.api = None
        self.user_login = None
        self.user_pass = None
        self.user_token = None
        self.user_feed = None
        self.authenticate()
        self.urls = []

    def authenticate(self, overwrite=False):
        """Logs into GitHub.

        Adapted from https://github.com/sigmavirus24/github-cli.

        Two factor authentication does not seem to be triggering the
        SMS code: https://github.com/sigmavirus24/github3.py/issues/387.
        To log in with 2FA enabled, use a token instead.

        Args:
            * overwrite: A boolean that indicates whether we cant to
                overwrite the current set of credentials.

        Returns:
            None.
        """
        if self.api is not None and not overwrite:
            return
        # Get the full path to the configuration file
        config = self.get_github_config_path(self.CONFIG)
        parser = configparser.RawConfigParser()
        # Check to make sure the file exists and we are allowed to read it
        if os.path.isfile(config) and os.access(config, os.R_OK | os.W_OK) and \
                    not overwrite:
                self.authenticate_cached_credentials(config, parser)
        else:
            # The file didn't exist or we don't have the correct permissions
            self.user_login = ''
            while not self.user_login:
                self.user_login = input('User Login: ')
            if click.confirm(('Do you want to log in with a password?\n '
                              'If not, you will be prompted for a '
                              'personal access token instead'),
                             default=True):
                self.user_pass = ''
                while not self.user_pass:
                    self.user_pass = getpass('Password: ')
                try:
                    # Get an authorization for this
                    auth = authorize(
                        self.user_login,
                        self.user_pass,
                        scopes=['user', 'repo', 'gist'],
                        note='gitsome',
                        note_url='https://github.com/donnemartin/github-cli'
                    )
                    self.user_token = auth.token
                except UnprocessableEntity:
                    click.secho('Error creating token.',
                                fg=self.clr_error)
                    click.secho(('Visit the following page and verify you do '
                                 'not have an existing token named "gitsome":\n'
                                 '  https://github.com/settings/tokens\n'
                                 'If a token already exists, update your '
                                 '~/.gitsomeconfig file with your token:\n'
                                 '  user_token = TOKEN\n'
                                 'You can also generate a new token.'),
                                fg=self.clr_message)
                    return
                except AuthenticationFailed:
                    self.print_auth_error()
                    return
            else:
                self.user_token = None
                while not self.user_token:
                    self.user_token = input('User Token: ')
            if self.user_feed:
                parser.set(self.CONFIG_SECTION,
                           self.CONFIG_USER_FEED,
                           self.user_feed)
            self.api = login(token=self.user_token,
                             two_factor_callback=self.request_two_factor_code)
            if self.check_auth():
                click.secho('Log in successful.')
            else:
                self.print_auth_error()

    def check_auth(self):
        """Checks if the current authorization is valid.

        Args:
            * None.

        Returns:
            None.
        """
        try:
            if self.api is not None:
                # Throws AuthenticationFailed if invalid credentials but
                # does not deduct from the rate limit.
                self.api.ratelimit_remaining
                return True
            else:
                self.print_auth_error()
        except AuthenticationFailed:
            self.print_auth_error()
        return False

    def get_github_config_path(self, config_file_name):
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

    def authenticate(self):
        """Logs into GitHub.

        Adapted from https://github.com/sigmavirus24/github-cli.

        Two factor authentication does not seem to be triggering the
        SMS code: https://github.com/sigmavirus24/github3.py/issues/387.
        To log in with 2FA enabled, use a token instead.

        Args:
            * None.

        Returns:
            None.
        """
        # Get the full path to the configuration file
        config = self.get_github_config_path(self.CONFIG)
        parser = configparser.RawConfigParser()
        # Check to make sure the file exists and we are allowed to read it
        if os.path.isfile(config) and os.access(config, os.R_OK | os.W_OK):
            with open(config) as config_file:
                parser.readfp(config_file)
                self.user_login = parser.get(self.CONFIG_SECTION,
                                             self.CONFIG_USER_LOGIN)
                try:
                    self.api = login(
                        username=parser.get(self.CONFIG_SECTION,
                                            self.CONFIG_USER_LOGIN),
                        token=parser.get(self.CONFIG_SECTION,
                                         self.CONFIG_USER_TOKEN),
                        two_factor_callback=self.request_two_factor_code)
                except configparser.NoOptionError:
                    self.api = login(
                        username=parser.get(self.CONFIG_SECTION,
                                            self.CONFIG_USER_LOGIN),
                        password=parser.get(self.CONFIG_SECTION,
                                            self.CONFIG_USER_PASS),
                        two_factor_callback=self.request_two_factor_code)
                self.user_feed = parser.get(self.CONFIG_SECTION,
                                            self.CONFIG_USER_FEED)
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
                             two_factor_callback=self.request_two_factor_code)
            # Create the file if it doesn't exist. Otherwise completely blank
            # out what was there before. Kind of dangerous and destructive but
            # somewhat necessary
            with open(config, 'w+') as config_file:
                parser.write(config_file)

    def load_section_list(self, parser, section):
        """Load the given section containing a list from ~/.haxornewsconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.

        :type section: str
        :param section: The section to load.

        :rtype: list
        :return: Collection of items stored in config.

        :raises: `Exception` if an error occurred reading from the parser.
        """
        items_ids = parser.get(self.CONFIG_SECTION, section)
        items_ids = items_ids.strip()
        excludes = ['[', ']', "'"]
        for exclude in excludes:
            items_ids = items_ids.replace(exclude, '')
        return items_ids.split(', ')

    def load_urls(self, view_in_browser):
        """Loads the current set of urls from ~/.githubconfigurl.

        Args:
            * None
            * view_in_browser: A boolean that determines whether to view
                in a web browser or a terminal.

        Returns:
            A list of urls.
        """
        config = self.get_github_config_path(self.CONFIG_URL)
        parser = configparser.RawConfigParser()
        with open(config) as config_file:
            parser.readfp(config_file)
            urls = parser.get(self.CONFIG_URL_SECTION,
                              self.CONFIG_URL_LIST)
            urls = urls.strip()
            excludes = ['[', ']', "'"]
            for exclude in excludes:
                urls = urls.replace(exclude, '')
                if not view_in_browser:
                    urls = urls.replace('https://github.com/', '')
            return urls.split(', ')

    def print_auth_error(self):
        """Prints a message the authorization has failed.

        Args:
            * None.

        Returns:
            None.
        """
        click.secho('Authentication error.', fg=self.clr_error)
        click.secho(('Update your credentials in ~/.gitsomeconfig '
                     'or run:\n  gh configure'),
                    fg=self.clr_message)

    def prompt_news_feed(self):
        """Prompts the user to enter a news feed url.

        Args:
            * None

        Returns:
            None.
        """
        if click.confirm(('No feed url detected.\n  Calling gh events without '
                          "an argument\n  displays the logged in user's "
                          'news feed.\nDo you want gitsome to track your '
                          'news feed?'),
                         default=True):
            click.secho(('Visit the following url while logged into GitHub:\n'
                         '  https://github.com\n'
                         'Enter the url found under "Subscribe to your '
                         'news feed".'),
                        fg=self.clr_message)
            self.user_feed = ''
            while not self.user_feed:
                self.user_feed = input('URL: ')

    def request_two_factor_code(self):
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

    def save_urls(self):
        """Saves the current set of urls to ~/.githubconfigurl.

        Args:
            * None

        Returns:
            None.
        """
        config = self.get_github_config_path(self.CONFIG_URL)
        parser = configparser.RawConfigParser()
        try:
            parser.add_section(self.CONFIG_URL_SECTION)
        except DuplicateSectionError:
            pass
        parser.set(self.CONFIG_URL_SECTION, self.CONFIG_URL_LIST, self.urls)
        with open(config, 'w+') as config_file:
            parser.write(config_file)
