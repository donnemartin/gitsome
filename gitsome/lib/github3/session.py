# -*- coding: utf-8 -*-
import requests

from collections import Callable
from . import __version__
from logging import getLogger
from contextlib import contextmanager

__url_cache__ = {}
__logs__ = getLogger(__package__)


def requires_2fa(response):
    if (response.status_code == 401 and 'X-GitHub-OTP' in response.headers and
            'required' in response.headers['X-GitHub-OTP']):
        return True
    return False


class GitHubSession(requests.Session):
    auth = None
    __attrs__ = requests.Session.__attrs__ + ['base_url', 'two_factor_auth_cb']

    def __init__(self):
        super(GitHubSession, self).__init__()
        self.headers.update({
            # Only accept JSON responses
            'Accept': 'application/vnd.github.v3.full+json',
            # Only accept UTF-8 encoded data
            'Accept-Charset': 'utf-8',
            # Always sending JSON
            'Content-Type': "application/json",
            # Set our own custom User-Agent string
            'User-Agent': 'github3.py/{0}'.format(__version__),
            })
        self.base_url = 'https://api.github.com'
        self.two_factor_auth_cb = None
        self.request_counter = 0

    def basic_auth(self, username, password):
        """Set the Basic Auth credentials on this Session.

        :param str username: Your GitHub username
        :param str password: Your GitHub password
        """
        if not (username and password):
            return

        self.auth = (username, password)

        # Disable token authentication
        self.headers.pop('Authorization', None)

    def build_url(self, *args, **kwargs):
        """Builds a new API url from scratch."""
        parts = [kwargs.get('base_url') or self.base_url]
        parts.extend(args)
        parts = [str(p) for p in parts]
        key = tuple(parts)
        __logs__.info('Building a url from %s', key)
        if key not in __url_cache__:
            __logs__.info('Missed the cache building the url')
            __url_cache__[key] = '/'.join(parts)
        return __url_cache__[key]

    def handle_two_factor_auth(self, args, kwargs):
        headers = kwargs.pop('headers', {})
        headers.update({
            'X-GitHub-OTP': str(self.two_factor_auth_cb())
            })
        kwargs.update(headers=headers)
        return super(GitHubSession, self).request(*args, **kwargs)

    def has_auth(self):
        return (self.auth or self.headers.get('Authorization'))

    def oauth2_auth(self, client_id, client_secret):
        """Use OAuth2 for authentication.

        It is suggested you install requests-oauthlib to use this.

        :param str client_id: Client ID retrieved from GitHub
        :param str client_secret: Client secret retrieved from GitHub
        """
        raise NotImplementedError('These features are not implemented yet')

    def request(self, *args, **kwargs):
        response = super(GitHubSession, self).request(*args, **kwargs)
        self.request_counter += 1
        if requires_2fa(response) and self.two_factor_auth_cb:
            # No need to flatten and re-collect the args in
            # handle_two_factor_auth
            new_response = self.handle_two_factor_auth(args, kwargs)
            new_response.history.append(response)
            response = new_response
        return response

    def retrieve_client_credentials(self):
        """Return the client credentials.

        :returns: tuple(client_id, client_secret)
        """
        client_id = self.params.get('client_id')
        client_secret = self.params.get('client_secret')
        return (client_id, client_secret)

    def two_factor_auth_callback(self, callback):
        if not callback:
            return

        if not isinstance(callback, Callable):
            raise ValueError('Your callback should be callable')

        self.two_factor_auth_cb = callback

    def token_auth(self, token):
        """Use an application token for authentication.

        :param str token: Application token retrieved from GitHub's
            /authorizations endpoint
        """
        if not token:
            return

        self.headers.update({
            'Authorization': 'token {0}'.format(token)
            })
        # Unset username/password so we stop sending them
        self.auth = None

    @contextmanager
    def temporary_basic_auth(self, *auth):
        old_basic_auth = self.auth
        old_token_auth = self.headers.get('Authorization')

        self.basic_auth(*auth)
        yield

        self.auth = old_basic_auth
        if old_token_auth:
            self.headers['Authorization'] = old_token_auth

    @contextmanager
    def no_auth(self):
        """Unset authentication temporarily as a context manager."""
        old_basic_auth, self.auth = self.auth, None
        old_token_auth = self.headers.pop('Authorization', None)

        yield

        self.auth = old_basic_auth
        if old_token_auth:
            self.headers['Authorization'] = old_token_auth
