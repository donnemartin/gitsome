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

from __future__ import unicode_literals
from __future__ import print_function

import click
from getpass import getpass
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .compat import configparser
from .lib.github3 import authorize, enterprise_login, login
from .lib.github3.exceptions import AuthenticationFailed, UnprocessableEntity


class Config(object):
    """Gitsome config.

    :type api: :class:`github3.github.Github`
    :param api: An instance of github3.github.Github.

    :type clr_x: str
    :param clr_x: Various ansi color config colors to use for highlights.

    :type CONFIG: str
    :param CONFIG: The config file name.

    :type CONFIG_SECTION: str
    :param CONFIG_SECTION: The main config file section label.

    :type CONFIG_CLR_X: str
    :param CONFIG_CLR_X: Various ansi color config labels to use for highlights.

    :type CONFIG_ENTERPRISE_URL: str
    :param CONFIG_ENTERPRISE_URL: The GitHub Enterprise url.

    :type CONFIG_USER_LOGIN: str
    :param CONFIG_USER_LOGIN: The user login.

    :type CONFIG_USER_PASS: str
    :param CONFIG_USER_PASS: The user password.

    :type CONFIG_USER_TOKEN: str
    :param CONFIG_USER_TOKEN: The user token.

    :type CONFIG_USER_FEED: str
    :param CONFIG_USER_FEED: The user feed config.  This is the feed on
        https://github.com/ when logged in and requires the basic auth model,
        which doesn't work when logging in with tokens or 2FA.  This config
        listed the pre-signed url to access the feed.

    :type CONFIG_URL: str
    :param CONFIG_URL: The config file name that contains urls used in the
        `gh view` command.

    :type CONFIG_URL_SECTION: str
    :param CONFIG_URL_SECTION: The config file section that contains urls used
        in the `gh view  [url_index]` command.

    :type CONFIG_URL_LIST: str
    :param CONFIG_URL_LIST: The config containing a list of the last set of
        urls the user has seen, which allows the user to quickly access a repo
        url with the `gh view [url_index]` command.

    :type CONFIG_VERIFY_SSL: str
    :param CONFIG_VERIFY_SSL: Determines whether to verify SSL certs.

    :type enterprise_url: str
    :param enterprise_url: The GitHub Enterprise url.

    :type urls: list
    :param urls: The last set of urls the user has seen, which allows the user
        to quickly access a repo url with the gh view [url_index] command.

    :type user_login: str
    :param user_login: The user's login in ~/.gitsomeconfig.

    :type user_pass: str
    :param user_pass: The user's pass in ~/.gitsomeconfig.
        This is only stored for GitHub Enterprise users since using only a
        personal access token does not seem to be supported.

    :type user_token: str
    :param user_token: The user's token in ~/.gitsomeconfig.

    :type verify_ssl: bool
    :param verify_ssl: Determines whether to verify SSL certs.
    """

    CONFIG = '.gitsomeconfig'
    CONFIG_CLR_PRIMARY = 'clr_primary'
    CONFIG_CLR_SECONDARY = 'clr_secondary'
    CONFIG_CLR_TERTIARY = 'clr_tertiary'
    CONFIG_CLR_QUATERNARY = 'clr_quaternary'
    CONFIG_CLR_BOLD = 'clr_bold'
    CONFIG_CLR_CODE = 'clr_code'
    CONFIG_CLR_ERROR = 'clr_error'
    CONFIG_CLR_HEADER = 'clr_header'
    CONFIG_CLR_LINK = 'clr_link'
    CONFIG_CLR_LIST = 'clr_list'
    CONFIG_CLR_MESSAGE = 'clr_message'
    CONFIG_CLR_NUM_COMMENTS = 'clr_num_comments'
    CONFIG_CLR_NUM_POINTS = 'clr_num_points'
    CONFIG_CLR_TAG = 'clr_tag'
    CONFIG_CLR_TIME = 'clr_time'
    CONFIG_CLR_TITLE = 'clr_title'
    CONFIG_CLR_TOOLTIP = 'clr_tooltip'
    CONFIG_CLR_USER = 'clr_user'
    CONFIG_CLR_VIEW_LINK = 'clr_view_link'
    CONFIG_CLR_VIEW_INDEX = 'clr_view_index'
    CONFIG_SECTION = 'github'
    CONFIG_USER_LOGIN = 'user_login'
    CONFIG_USER_PASS = 'user_pass'
    CONFIG_USER_TOKEN = 'user_token'
    CONFIG_USER_FEED = 'user_feed'
    CONFIG_ENTERPRISE_URL = 'enterprise_url'
    CONFIG_VERIFY_SSL = 'verify_ssl'
    CONFIG_URL = '.gitsomeconfigurl'
    CONFIG_URL_SECTION = 'url'
    CONFIG_URL_LIST = 'url_list'
    CONFIG_AVATAR = '.gitsomeconfigavatar.png'

    def __init__(self):
        self.api = None
        self.user_login = None
        self.user_pass = None
        self.user_token = None
        self.user_feed = None
        self.enterprise_url = None
        self.verify_ssl = True
        self.urls = []
        self._init_colors()
        self.load_configs([
            self.load_config_colors,
        ])
        self.login = login
        self.authorize = authorize
        self.getpass = getpass

    def _init_colors(self):
        """Initialize colors to their defaults."""
        self.clr_primary = None
        self.clr_secondary = 'green'
        self.clr_tertiary = 'cyan'
        self.clr_quaternary = 'yellow'
        self.clr_bold = 'cyan'
        self.clr_code = 'cyan'
        self.clr_error = 'red'
        self.clr_header = 'yellow'
        self.clr_link = 'green'
        self.clr_list = 'cyan'
        self.clr_message = None
        self.clr_num_comments = 'green'
        self.clr_num_points = 'green'
        self.clr_tag = 'cyan'
        self.clr_time = 'yellow'
        self.clr_title = None
        self.clr_tooltip = None
        self.clr_user = 'cyan'
        self.clr_view_link = 'magenta'
        self.clr_view_index = 'magenta'

    def authenticate_cached_credentials(self, config, parser,
                                        enterprise_auth=enterprise_login):
        """Authenticate with the user's credentials in ~/.gitsomeconfig.

        :type config: str
        :param config: The config path.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser.
        """
        with open(config) as config_file:
            try:
                parser.read_file(config_file)
            except AttributeError:
                parser.readfp(config_file)
            self.user_login = self.load_config(
                parser=parser,
                cfg_label=self.CONFIG_USER_LOGIN)
            self.user_pass = self.load_config(
                parser=parser,
                cfg_label=self.CONFIG_USER_PASS)
            self.user_token = self.load_config(
                parser=parser,
                cfg_label=self.CONFIG_USER_TOKEN)
            self.enterprise_url = self.load_config(
                parser=parser,
                cfg_label=self.CONFIG_ENTERPRISE_URL)
            self.verify_ssl = self.load_config(
                parser=parser,
                cfg_label=self.CONFIG_VERIFY_SSL,
                boolean_config=True)
            self.user_feed = self.load_config(
                parser=parser,
                cfg_label=self.CONFIG_USER_FEED)
            if not self.verify_ssl:
                # The user has chosen not to verify SSL certs.
                # Disable warnings related to this option.
                requests.packages.urllib3.disable_warnings(
                    InsecureRequestWarning)
            login_kwargs = {
                'username': self.user_login,
                'two_factor_callback': self.request_two_factor_code,
            }
            if self.enterprise_url is not None:
                self.login = enterprise_auth
                login_kwargs.update({
                    'url': self.enterprise_url,
                    'verify': self.verify_ssl,
                })
                if self.user_token is not None:
                    login_kwargs.update({'token': self.user_token})
                elif self.user_pass is not None:
                    login_kwargs.update({'password': self.user_pass})
                else:
                    self.print_auth_error()
                    return
            else:
                login_kwargs.update({'token': self.user_token})
            self.api = self.login(**login_kwargs)

    def authenticate(self, enterprise=False,
                     enterprise_auth=enterprise_login, overwrite=False):
        """Log into GitHub.

        Adapted from https://github.com/sigmavirus24/github-cli.

        :type enterprise: bool
        :param enterprise: Determines whether to configure GitHub Enterprise.
            Default: False.

        :type overwrite: bool
        :param overwrite: indicates whether we cant to overwrite the current
            set of credentials.  Default: False.
        """
        if self.api is not None and not overwrite:
            return
        # Get the full path to the configuration file.
        config = self.get_github_config_path(self.CONFIG)
        parser = configparser.RawConfigParser()
        # Check to make sure the file exists and we are allowed to read it.
        # Skip if we want to overwrite the auth settings.
        if os.path.isfile(config) and os.access(config, os.R_OK | os.W_OK) and \
                not overwrite:
            with open(config) as config_file:
                try:
                    parser.read_file(config_file)
                except AttributeError:
                    parser.readfp(config_file)
            self.authenticate_cached_credentials(config, parser)
        else:
            # The file didn't exist or we don't have the correct permissions.
            login_kwargs = {
                'two_factor_callback': self.request_two_factor_code,
            }
            if enterprise:
                self.login = enterprise_auth
                while not self.enterprise_url:
                    self.enterprise_url = input('Enterprise URL: ')
                if click.confirm('Do you want to verify SSL certs?',
                                 default=True):
                    self.verify_ssl = True
                else:
                    self.verify_ssl = False
                login_kwargs.update({
                    'url': self.enterprise_url,
                    'verify': self.verify_ssl,
                })
            while not self.user_login:
                self.user_login = input('User Login: ')
            login_kwargs.update({'username': self.user_login})
            if click.confirm(('Do you want to log in with a password [Y] or '
                              'a personal access token [n]?'),
                             default=True):
                user_pass = None
                while not user_pass:
                    user_pass = self.getpass('Password: ')
                login_kwargs.update({'password': user_pass})
                try:
                    if not enterprise:
                        # Trade the user password for a personal access token.
                        # This does not seem to be available for Enterprise.
                        auth = self.authorize(
                            self.user_login,
                            user_pass,
                            scopes=['user', 'repo'],
                            note='gitsome',
                            note_url='https://github.com/donnemartin/gitsome',
                            two_factor_callback=self.request_two_factor_code
                        )
                        self.user_token = auth.token
                    else:
                        self.user_pass = user_pass
                except (UnprocessableEntity, AuthenticationFailed):
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
                    self.print_auth_error()
                    return
            else:
                # The user has chosen to authenticate with a token.
                while not self.user_token:
                    self.user_token = input('Token: ')
                login_kwargs.update({'token': self.user_token})
            self.api = self.login(**login_kwargs)
            if self.user_feed:
                parser.set(self.CONFIG_SECTION,
                           self.CONFIG_USER_FEED,
                           self.user_feed)

    def check_auth(self):
        """Check if the current authorization is valid.

        This method uses the ratelimit_remaining api to check whether
        the currently authenticated user's credentials are valid without
        deducting from the rate limit.  The ratelimit_remaining api does not
        seem to be available for GitHub Enterprise.

        github3.py's method check_authorization seems to only work given
        an authorization created by a registered application.

        TODO: Determine a better way to check the authorization for
        GitHub Enterprise.

        :type enterprise: bool
        :param enterprise: Determines whether we are authenticating with
            GitHub Enterprise.
        """
        if self.enterprise_url is not None:
            return True
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
        """Attempt to find the github config file.

        Adapted from https://github.com/sigmavirus24/github-cli.

        :type config_file_name: str
        :param config_file_name: The config file name.

        :rtype: str
        :return: The github config file path.
        """
        home = os.path.abspath(os.environ.get('HOME', ''))
        config_file_path = os.path.join(home, config_file_name)
        return config_file_path

    def load_config(self, parser, cfg_label, default=None,
                    color_config=False, boolean_config=False):
        """Load the specified config from ~/.gitsomeconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.

        :type cfg_label: str
        :param cfg_label: The config label to load.

        :type default: str
        :param default: The default color if no color config exists.
            Default: None.

        :type color_config: bool
        :param color_config: Determines whether this is a color config.
            Default: False.

        :type boolean_config: bool
        :param boolean_config: Determines whether to load a boolean config.
            Default: False.
        """
        try:
            if boolean_config:
                cfg = parser.getboolean(self.CONFIG_SECTION, cfg_label)
            else:
                cfg = parser.get(self.CONFIG_SECTION, cfg_label)
                if color_config:
                    if cfg == 'none':
                        cfg = None
                    # Check if the user input a valid color.
                    # If invalid, this will throw a TypeError
                    click.style('', fg=cfg)
        except (TypeError, configparser.NoOptionError):
            return default
        return cfg

    def load_configs(self, config_funcs):
        """Load the specified config from ~/.gitsomeconfig.

        :type foo: list
        :param foo: The config methods to run.
        """
        config_file_path = self.get_github_config_path(self.CONFIG)
        parser = configparser.RawConfigParser()
        try:
            with open(config_file_path) as config_file:
                try:
                    parser.read_file(config_file)
                except AttributeError:
                    parser.readfp(config_file)
                for config_func in config_funcs:
                    config_func(parser)
        except IOError:
            # There might not be a cache yet, just silently return.
            return None

    def load_config_colors(self, parser):
        """Load the color config from ~/.gitsomeconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.load_colors(parser)

    def load_colors(self, parser):
        """Load all colors from ~/.gitsomeconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.clr_primary = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_PRIMARY,
            default=self.clr_primary,
            color_config=True)
        self.clr_secondary = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_SECONDARY,
            default=self.clr_secondary,
            color_config=True)
        self.clr_tertiary = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_TERTIARY,
            default=self.clr_tertiary,
            color_config=True)
        self.clr_quaternary = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_QUATERNARY,
            default=self.clr_quaternary,
            color_config=True)
        self.clr_bold = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_BOLD,
            default=self.clr_bold,
            color_config=True)
        self.clr_code = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_CODE,
            default=self.clr_code,
            color_config=True)
        self.clr_code = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_ERROR,
            default=self.clr_code,
            color_config=True)
        self.clr_header = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_HEADER,
            default=self.clr_header,
            color_config=True)
        self.clr_link = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_LINK,
            default=self.clr_link,
            color_config=True)
        self.clr_list = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_LIST,
            default=self.clr_list,
            color_config=True)
        self.clr_message = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_MESSAGE,
            default=self.clr_message,
            color_config=True)
        self.clr_num_comments = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_NUM_COMMENTS,
            default=self.clr_num_comments,
            color_config=True)
        self.clr_num_points = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_NUM_POINTS,
            default=self.clr_num_points,
            color_config=True)
        self.clr_tag = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_TAG,
            default=self.clr_tag,
            color_config=True)
        self.clr_time = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_TIME,
            default=self.clr_time,
            color_config=True)
        self.clr_title = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_TITLE,
            default=self.clr_title,
            color_config=True)
        self.clr_tooltip = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_TOOLTIP,
            default=self.clr_tooltip,
            color_config=True)
        self.clr_user = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_USER,
            default=self.clr_user,
            color_config=True)
        self.clr_view_link = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_VIEW_LINK,
            default=self.clr_view_link,
            color_config=True)
        self.clr_view_index = self.load_config(
            parser=parser,
            cfg_label=self.CONFIG_CLR_VIEW_INDEX,
            default=self.clr_view_index,
            color_config=True)

    def load_urls(self, view_in_browser):
        """Load the current set of urls from ~/.gitsomeconfigurl.

        :type view_in_browser: bool
        :param view_in_browser: Determines whether to view the urls in a
            browser.

        :rtype: list
        :return: Collection of urls.
        """
        config = self.get_github_config_path(self.CONFIG_URL)
        parser = configparser.RawConfigParser()
        with open(config) as config_file:
            try:
                parser.read_file(config_file)
            except AttributeError:
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
        """Print a message the authorization has failed."""
        click.secho('Authentication error.', fg=self.clr_error)
        click.secho(('Update your credentials in ~/.gitsomeconfig '
                     'or run:\n  gh configure'),
                    fg=self.clr_message)

    def prompt_news_feed(self):
        """Prompt the user to enter a news feed url."""
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
        """Request two factor authentication code.

        Callback if two factor authentication is requested.

        :rtype: str
        :return: The user input two factor authentication code.
        """
        code = ''
        while not code:
            code = input('Enter 2FA code: ')
        return code

    def save_config(self):
        """Saves the config to ~/.gitsomeconfig."""
        if self.check_auth():
            config = self.get_github_config_path(self.CONFIG)
            parser = configparser.RawConfigParser()
            parser.add_section(self.CONFIG_SECTION)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_USER_LOGIN,
                       self.user_login)
            if self.user_token is not None:
                parser.set(self.CONFIG_SECTION,
                           self.CONFIG_USER_TOKEN,
                           self.user_token)
            if self.user_feed is not None:
                parser.set(self.CONFIG_SECTION,
                           self.CONFIG_USER_FEED,
                           self.user_feed)
            if self.enterprise_url is not None:
                parser.set(self.CONFIG_SECTION,
                           self.CONFIG_ENTERPRISE_URL,
                           self.enterprise_url)
                if self.user_pass is not None:
                    parser.set(self.CONFIG_SECTION,
                               self.CONFIG_USER_PASS,
                               self.user_pass)
            else:
                parser.remove_option(self.CONFIG_SECTION,
                                     self.CONFIG_USER_PASS)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_VERIFY_SSL,
                       self.verify_ssl)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_PRIMARY,
                       self.clr_primary)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_SECONDARY,
                       self.clr_secondary)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_TERTIARY,
                       self.clr_tertiary)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_QUATERNARY,
                       self.clr_quaternary)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_BOLD,
                       self.clr_bold)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_CODE,
                       self.clr_code)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_ERROR,
                       self.clr_error)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_HEADER,
                       self.clr_header)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_LINK,
                       self.clr_link)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_LIST,
                       self.clr_list)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_MESSAGE,
                       self.clr_message)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_NUM_COMMENTS,
                       self.clr_num_comments)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_NUM_POINTS,
                       self.clr_num_points)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_TAG,
                       self.clr_tag)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_TIME,
                       self.clr_time)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_TITLE,
                       self.clr_title)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_TOOLTIP,
                       self.clr_tooltip)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_USER,
                       self.clr_user)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_VIEW_LINK,
                       self.clr_view_link)
            parser.set(self.CONFIG_SECTION,
                       self.CONFIG_CLR_VIEW_INDEX,
                       self.clr_view_index)
            with open(config, 'w+') as config_file:
                parser.write(config_file)

    def save_urls(self):
        """Save the current set of urls to ~/.gitsomeconfigurl."""
        config = self.get_github_config_path(self.CONFIG_URL)
        parser = configparser.RawConfigParser()
        try:
            parser.add_section(self.CONFIG_URL_SECTION)
        except configparser.DuplicateSectionError:
            pass
        parser.set(self.CONFIG_URL_SECTION, self.CONFIG_URL_LIST, self.urls)
        with open(config, 'w+') as config_file:
            parser.write(config_file)

    def show_bash_completions_info(self):
        """Show info on how to enable bash completions"""
        click.secho(('By default, gitsome looks at the following locations '
                     'to enable bash completions:\n'
                     '  https://github.com/donnemartin/gitsome/blob/master/xonsh/environ.py#L123-L130\n'  # NOQA
                     'If bash completions are not working for you, check out '
                     'the following link:\n'
                     '  https://github.com/donnemartin/gitsome#enabling-bash-completions'),  # NOQA
                    fg=self.clr_message)
