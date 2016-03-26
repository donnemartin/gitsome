# -*- coding: utf-8 -*-
"""
github3.models
==============

This module provides the basic models used in github3.py

"""
from __future__ import unicode_literals

from json import dumps, loads
from requests.compat import urlparse, is_py2
from datetime import datetime
from logging import getLogger

from . import exceptions
from .decorators import requires_auth
from .null import NullObject
from .session import GitHubSession
from .utils import UTC

__timeformat__ = '%Y-%m-%dT%H:%M:%SZ'
__logs__ = getLogger(__package__)


class GitHubCore(object):

    """The base object for all objects that require a session.

    The :class:`GitHubCore <GitHubCore>` object provides some
    basic attributes and methods to other sub-classes that are very useful to
    have.
    """

    def __init__(self, json, session=None):
        if hasattr(session, 'session'):
            # i.e. session is actually a GitHubCore instance
            session = session.session
        elif session is None:
            session = GitHubSession()
        self.session = session

        # set a sane default
        self._github_url = 'https://api.github.com'

        if json is not None:
            self.etag = json.pop('ETag', None)
            self.last_modified = json.pop('Last-Modified', None)
            self._uniq = json.get('url', None)
        self._json_data = json
        self._update_attributes(json)

    def _update_attributes(self, json):
        pass

    def __getattr__(self, attribute):
        """Proxy access to stored JSON."""
        if attribute not in self._json_data:
            raise AttributeError(attribute)
        value = self._json_data.get(attribute, None)
        setattr(self, attribute, value)
        return value

    def as_dict(self):
        """Return the attributes for this object as a dictionary.

        This is equivalent to calling::

            json.loads(obj.as_json())

        :returns: this object's attributes serialized to a dictionary
        :rtype: dict
        """
        return self._json_data

    def as_json(self):
        """Return the json data for this object.

        This is equivalent to calling::

            json.dumps(obj.as_dict())

        :returns: this object's attributes as a JSON string
        :rtype: str
        """
        return dumps(self._json_data)

    def _strptime(self, time_str):
        """Convert an ISO 8601 formatted string to a datetime object.

        We assume that the ISO 8601 formatted string is in UTC and we create
        the datetime object so that it is timezone-aware.

        :param str time_str: ISO 8601 formatted string
        :returns: timezone-aware datetime object
        :rtype: datetime or None
        """
        if time_str:
            # Parse UTC string into naive datetime, then add timezone
            dt = datetime.strptime(time_str, __timeformat__)
            return dt.replace(tzinfo=UTC())
        return None

    def __repr__(self):
        repr_string = self._repr()
        if is_py2:
            return repr_string.encode('utf-8')
        return repr_string

    @classmethod
    def from_dict(cls, json_dict):
        """Return an instance of this class formed from ``json_dict``."""
        return cls(json_dict)

    @classmethod
    def from_json(cls, json):
        """Return an instance of this class formed from ``json``."""
        return cls(loads(json))

    def __eq__(self, other):
        return self._uniq == other._uniq

    def __ne__(self, other):
        return self._uniq != other._uniq

    def __hash__(self):
        return hash(self._uniq)

    def _repr(self):
        return '<github3-core at 0x{0:x}>'.format(id(self))

    @staticmethod
    def _remove_none(data):
        if not data:
            return
        for (k, v) in list(data.items()):
            if v is None:
                del(data[k])

    def _instance_or_null(self, instance_class, json):
        if json is None:
            return NullObject(instance_class.__name__)
        if not isinstance(json, dict):
            return exceptions.UnprocessableResponseBody(
                "GitHub's API returned a body that could not be handled", json
            )
        try:
            return instance_class(json, self)
        except TypeError:  # instance_class is not a subclass of GitHubCore
            return instance_class(json)

    def _json(self, response, status_code, include_cache_info=True):
        ret = None
        if self._boolean(response, status_code, 404) and response.content:
            __logs__.info('Attempting to get JSON information from a Response '
                          'with status code %d expecting %d',
                          response.status_code, status_code)
            ret = response.json()
            headers = response.headers
            if (include_cache_info and
                    (headers.get('Last-Modified') or headers.get('ETag')) and
                    isinstance(ret, dict)):
                ret['Last-Modified'] = response.headers.get(
                    'Last-Modified', ''
                )
                ret['ETag'] = response.headers.get('ETag', '')
        __logs__.info('JSON was %sreturned', 'not ' if ret is None else '')
        return ret

    def _boolean(self, response, true_code, false_code):
        if response is not None:
            status_code = response.status_code
            if status_code == true_code:
                return True
            if status_code != false_code and status_code >= 400:
                raise exceptions.error_for(response)
        return False

    def _delete(self, url, **kwargs):
        __logs__.debug('DELETE %s with %s', url, kwargs)
        return self.session.delete(url, **kwargs)

    def _get(self, url, **kwargs):
        __logs__.debug('GET %s with %s', url, kwargs)
        return self.session.get(url, **kwargs)

    def _patch(self, url, **kwargs):
        __logs__.debug('PATCH %s with %s', url, kwargs)
        return self.session.patch(url, **kwargs)

    def _post(self, url, data=None, json=True, **kwargs):
        if json:
            data = dumps(data) if data is not None else data
        __logs__.debug('POST %s with %s, %s', url, data, kwargs)
        return self.session.post(url, data, **kwargs)

    def _put(self, url, **kwargs):
        __logs__.debug('PUT %s with %s', url, kwargs)
        return self.session.put(url, **kwargs)

    def _build_url(self, *args, **kwargs):
        """Builds a new API url from scratch."""
        return self.session.build_url(*args, **kwargs)

    @property
    def _api(self):
        return "{0.scheme}://{0.netloc}{0.path}".format(self._uri)

    @_api.setter
    def _api(self, uri):
        self._uri = urlparse(uri)
        self.url = uri

    def _iter(self, count, url, cls, params=None, etag=None, headers=None):
        """Generic iterator for this project.

        :param int count: How many items to return.
        :param int url: First URL to start with
        :param class cls: cls to return an object of
        :param params dict: (optional) Parameters for the request
        :param str etag: (optional), ETag from the last call
        :param dict headers: (optional) HTTP Headers for the request
        :returns: A lazy iterator over the pagianted resource
        :rtype: :class:`GitHubIterator <github3.structs.GitHubIterator>`
        """
        from .structs import GitHubIterator
        return GitHubIterator(count, url, cls, self, params, etag, headers)

    @property
    def ratelimit_remaining(self):
        """Number of requests before GitHub imposes a ratelimit.

        :returns: int
        """
        json = self._json(self._get(self._github_url + '/rate_limit'), 200)
        core = json.get('resources', {}).get('core', {})
        self._remaining = core.get('remaining', 0)
        return self._remaining

    def refresh(self, conditional=False):
        """Re-retrieve the information for this object.

        The reasoning for the return value is the following example: ::

            repos = [r.refresh() for r in g.repositories_by('kennethreitz')]

        Without the return value, that would be an array of ``None``'s and you
        would otherwise have to do: ::

            repos = [r for i in g.repositories_by('kennethreitz')]
            [r.refresh() for r in repos]

        Which is really an anti-pattern.

        .. versionchanged:: 0.5

        .. _Conditional Requests:
            http://developer.github.com/v3/#conditional-requests

        :param bool conditional: If True, then we will search for a stored
            header ('Last-Modified', or 'ETag') on the object and send that
            as described in the `Conditional Requests`_ section of the docs
        :returns: self
        """
        headers = {}
        if conditional:
            if self.last_modified:
                headers['If-Modified-Since'] = self.last_modified
            elif self.etag:
                headers['If-None-Match'] = self.etag

        headers = headers or None
        json = self._json(self._get(self._api, headers=headers), 200)
        if json is not None:
            self._update_attributes(json)
        return self


class BaseComment(GitHubCore):

    """A basic class for Gist, Issue and Pull Request Comments."""

    def _update_attributes(self, comment):
        #: Unique ID of the comment.
        self.id = comment.get('id')
        #: Body of the comment. (As written by the commenter)
        self.body = comment.get('body')
        #: Body of the comment formatted as plain-text. (Stripped of markdown,
        #: etc.)
        self.body_text = comment.get('body_text')
        #: Body of the comment formatted as html.
        self.body_html = comment.get('body_html')
        #: datetime object representing when the comment was created.
        self.created_at = self._strptime(comment.get('created_at'))
        #: datetime object representing when the comment was updated.
        self.updated_at = self._strptime(comment.get('updated_at'))

        self._api = comment.get('url', '')
        self.links = comment.get('_links')
        #: The url of this comment at GitHub
        self.html_url = ''
        #: The url of the pull request, if it exists
        self.pull_request_url = ''
        if self.links:
            self.html_url = self.links.get('html')
            self.pull_request_url = self.links.get('pull_request')

    @requires_auth
    def delete(self):
        """Delete this comment.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def edit(self, body):
        """Edit this comment.

        :param str body: (required), new body of the comment, Markdown
            formatted
        :returns: bool
        """
        if body:
            json = self._json(self._patch(self._api,
                              data=dumps({'body': body})), 200)
            if json:
                self._update_attributes(json)
                return True
        return False


class BaseCommit(GitHubCore):

    """This abstracts a lot of the common attributes for commit-like objects.

    The :class:`BaseCommit <BaseCommit>` object serves as the base for
    the various types of commit objects returned by the API.
    """

    def _update_attributes(self, commit):
        self._api = commit.get('url', '')
        #: SHA of this commit.
        self.sha = commit.get('sha')
        #: Commit message
        self.message = commit.get('message')
        #: List of parents to this commit.
        self.parents = commit.get('parents', [])
        #: URL to view the commit on GitHub
        self.html_url = commit.get('html_url', '')
        if not self.sha:
            i = self._api.rfind('/')
            self.sha = self._api[i + 1:]

        self._uniq = self.sha


class BaseAccount(GitHubCore):

    """This class holds the commonalities of Organizations and Users.

    The :class:`BaseAccount <BaseAccount>` object is used to do the
    heavy lifting for :class:`Organization <github3.orgs.Organization>` and
    :class:`User <github3.users.User>` objects.
    """

    def _update_attributes(self, acct):
        #: Tells you what type of account this is
        self.type = None
        if acct.get('type'):
            self.type = acct.get('type')
        self._api = acct.get('url', '')

        #: URL of the avatar at gravatar
        self.avatar_url = acct.get('avatar_url', '')
        #: URL of the blog
        self.blog = acct.get('blog', '')
        #: Name of the company
        self.company = acct.get('company', '')

        #: datetime object representing the date the account was created
        self.created_at = self._strptime(acct.get('created_at'))

        #: E-mail address of the user/org
        self.email = acct.get('email')

        # The number of people following this acct
        #: Number of followers
        self.followers_count = acct.get('followers', 0)

        # The number of people this acct follows
        #: Number of people the user is following
        self.following_count = acct.get('following', 0)

        #: Unique ID of the account
        self.id = acct.get('id', 0)
        #: Location of the user/org
        self.location = acct.get('location', '')
        #: User name of the user/organization
        self.login = acct.get('login', '')

        # e.g. first_name last_name
        #: Real name of the user/org
        self.name = acct.get('name') or ''
        self.name = self.name

        # The number of public_repos
        #: Number of public repos owned by the user/org
        self.public_repos_count = acct.get('public_repos', 0)

        # e.g. https://github.com/self._login
        #: URL of the user/org's profile
        self.html_url = acct.get('html_url', '')

        #: Markdown formatted biography
        self.bio = acct.get('bio')

    def _repr(self):
        return '<{s.type} [{s.login}:{s.name}]>'.format(s=self)
