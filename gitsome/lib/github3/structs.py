# -*- coding: utf-8 -*-
import collections
import functools

from requests.compat import urlparse, urlencode

from . import exceptions
from . import models


class GitHubIterator(models.GitHubCore, collections.Iterator):
    """The :class:`GitHubIterator` class powers all of the iter_* methods."""
    def __init__(self, count, url, cls, session, params=None, etag=None,
                 headers=None):
        models.GitHubCore.__init__(self, {}, session)
        #: Original number of items requested
        self.original = count
        #: Number of items left in the iterator
        self.count = count
        #: URL the class used to make it's first GET
        self.url = url
        #: Last URL that was requested
        self.last_url = None
        self._api = self.url
        #: Class for constructing an item to return
        self.cls = cls
        #: Parameters of the query string
        self.params = params or {}
        self._remove_none(self.params)
        # We do not set this from the parameter sent. We want this to
        # represent the ETag header returned by GitHub no matter what.
        # If this is not None, then it won't be set from the response and
        # that's not what we want.
        #: The ETag Header value returned by GitHub
        self.etag = None
        #: Headers generated for the GET request
        self.headers = headers or {}
        #: The last response seen
        self.last_response = None
        #: Last status code received
        self.last_status = 0

        if etag:
            self.headers.update({'If-None-Match': etag})

        self.path = urlparse(self.url).path

    def _repr(self):
        return '<GitHubIterator [{0}, {1}]>'.format(self.count, self.path)

    def __iter__(self):
        self.last_url, params = self.url, self.params
        headers = self.headers

        if 0 < self.count <= 100 and self.count != -1:
            params['per_page'] = self.count

        if 'per_page' not in params and self.count == -1:
            params['per_page'] = 100

        cls = self.cls
        if issubclass(self.cls, models.GitHubCore):
            cls = functools.partial(self.cls, session=self)

        while (self.count == -1 or self.count > 0) and self.last_url:
            response = self._get(self.last_url, params=params,
                                 headers=headers)
            self.last_response = response
            self.last_status = response.status_code
            if params:
                params = None  # rel_next already has the params

            if not self.etag and response.headers.get('ETag'):
                self.etag = response.headers.get('ETag')

            json = self._get_json(response)

            if json is None:
                break

            # languages returns a single dict. We want the items.
            if isinstance(json, dict):
                if issubclass(self.cls, models.GitHubCore):
                    raise exceptions.UnprocessableResponseBody(
                        "GitHub's API returned a body that could not be"
                        " handled", json
                    )
                if json.get('ETag'):
                    del json['ETag']
                if json.get('Last-Modified'):
                    del json['Last-Modified']
                json = json.items()

            for i in json:
                yield cls(i)
                self.count -= 1 if self.count > 0 else 0
                if self.count == 0:
                    break

            rel_next = response.links.get('next', {})
            self.last_url = rel_next.get('url', '')

    def __next__(self):
        if not hasattr(self, '__i__'):
            self.__i__ = self.__iter__()
        return next(self.__i__)

    def _get_json(self, response):
        return self._json(response, 200)

    def refresh(self, conditional=False):
        self.count = self.original
        if conditional:
            self.headers['If-None-Match'] = self.etag
        self.etag = None
        self.__i__ = self.__iter__()
        return self

    def next(self):
        return self.__next__()


class SearchIterator(GitHubIterator):

    """This is a special-cased class for returning iterable search results.

    It inherits from :class:`GitHubIterator <github3.structs.GitHubIterator>`.
    All members and methods documented here are unique to instances of this
    class. For other members and methods, check its parent class.

    """

    def __init__(self, count, url, cls, session, params=None, etag=None,
                 headers=None):
        super(SearchIterator, self).__init__(count, url, cls, session, params,
                                             etag, headers)
        #: Total count returned by GitHub
        self.total_count = 0
        #: Items array returned in the last request
        self.items = []

    def _repr(self):
        return '<SearchIterator [{0}, {1}?{2}]>'.format(self.count, self.path,
                                                        urlencode(self.params))

    def _get_json(self, response):
        json = self._json(response, 200)
        # I'm not sure if another page will retain the total_count attribute,
        # so if it's not in the response, just set it back to what it used to
        # be
        self.total_count = json.get('total_count', self.total_count)
        self.items = json.get('items', [])
        # If we return None then it will short-circuit the while loop.
        return json.get('items')
