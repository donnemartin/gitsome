# -*- coding: utf-8 -*-
"""
github3.gists.gist
==================

This module contains the Gist class alone for simplicity.

"""
from __future__ import unicode_literals

from json import dumps
from ..models import GitHubCore
from ..decorators import requires_auth
from .comment import GistComment
from .file import GistFile
from .history import GistHistory
from ..users import User


class Gist(GitHubCore):

    """This object holds all the information returned by Github about a gist.

    With it you can comment on or fork the gist (assuming you are
    authenticated), edit or delete the gist (assuming you own it).  You can
    also "star" or "unstar" the gist (again assuming you have authenticated).

    Two gist instances can be checked like so::

        g1 == g2
        g1 != g2

    And is equivalent to::

        g1.id == g2.id
        g1.id != g2.id

    See also: http://developer.github.com/v3/gists/

    """

    def _update_attributes(self, data):
        #: Number of comments on this gist
        self.comments_count = data.get('comments', 0)

        #: Unique id for this gist.
        self.id = '{0}'.format(data.get('id', ''))

        #: Description of the gist
        self.description = data.get('description', '')

        # e.g. https://api.github.com/gists/1
        self._api = data.get('url', '')

        #: URL of this gist at Github, e.g., https://gist.github.com/1
        self.html_url = data.get('html_url')
        #: Boolean describing if the gist is public or private
        self.public = data.get('public')

        self._forks = data.get('forks', [])

        #: Git URL to pull this gist, e.g., git://gist.github.com/1.git
        self.git_pull_url = data.get('git_pull_url', '')

        #: Git URL to push to gist, e.g., git@gist.github.com/1.git
        self.git_push_url = data.get('git_push_url', '')

        #: datetime object representing when the gist was created.
        self.created_at = self._strptime(data.get('created_at'))

        #: datetime object representing the last time this gist was updated.
        self.updated_at = self._strptime(data.get('updated_at'))

        owner = data.get('owner')
        #: :class:`User <github3.users.User>` object representing the owner of
        #: the gist.
        self.owner = User(owner, self) if owner else None

        self._files = [GistFile(data['files'][f]) for f in data['files']]

        #: History of this gist, list of
        #: :class:`GistHistory <github3.gists.history.GistHistory>`
        self.history = [GistHistory(h, self) for h in data.get('history', [])]

        # New urls

        #: Comments URL (not a template)
        self.comments_url = data.get('comments_url', '')

        #: Commits URL (not a template)
        self.commits_url = data.get('commits_url', '')

        #: Forks URL (not a template)
        self.forks_url = data.get('forks_url', '')

        #: Whether the content of this Gist has been truncated or not
        self.truncated = data.get('truncated')

    def __str__(self):
        return self.id

    def _repr(self):
        return '<Gist [{0}]>'.format(self.id)

    @requires_auth
    def create_comment(self, body):
        """Create a comment on this gist.

        :param str body: (required), body of the comment
        :returns: :class:`GistComment <github3.gists.comment.GistComment>`

        """
        json = None
        if body:
            url = self._build_url('comments', base_url=self._api)
            json = self._json(self._post(url, data={'body': body}), 201)
        return self._instance_or_null(GistComment, json)

    @requires_auth
    def delete(self):
        """Delete this gist.

        :returns: bool -- whether the deletion was successful

        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def edit(self, description='', files={}):
        """Edit this gist.

        :param str description: (optional), description of the gist
        :param dict files: (optional), files that make up this gist; the
            key(s) should be the file name(s) and the values should be another
            (optional) dictionary with (optional) keys: 'content' and
            'filename' where the former is the content of the file and the
            latter is the new name of the file.
        :returns: bool -- whether the edit was successful

        """
        data = {}
        json = None
        if description:
            data['description'] = description
        if files:
            data['files'] = files
        if data:
            json = self._json(self._patch(self._api, data=dumps(data)), 200)
        if json:
            self._update_attributes(json)
            return True
        return False

    @requires_auth
    def fork(self):
        """Fork this gist.

        :returns: :class:`Gist <Gist>` if successful, ``None`` otherwise

        """
        url = self._build_url('forks', base_url=self._api)
        json = self._json(self._post(url), 201)
        return self._instance_or_null(Gist, json)

    @requires_auth
    def is_starred(self):
        """Check to see if this gist is starred by the authenticated user.

        :returns: bool -- True if it is starred, False otherwise

        """
        url = self._build_url('star', base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def comments(self, number=-1, etag=None):
        """Iterate over comments on this gist.

        :param int number: (optional), number of comments to iterate over.
            Default: -1 will iterate over all comments on the gist
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of
            :class:`GistComment <github3.gists.comment.GistComment>`

        """
        url = self._build_url('comments', base_url=self._api)
        return self._iter(int(number), url, GistComment, etag=etag)

    def commits(self, number=-1, etag=None):
        """Iterate over the commits on this gist.

        These commits will be requested from the API and should be the same as
        what is in ``Gist.history``.

        .. versionadded:: 0.6

        .. versionchanged:: 0.9

            Added param ``etag``.

        :param int number: (optional), number of commits to iterate over.
            Default: -1 will iterate over all commits associated with this
            gist.
        :param str etag: (optional), ETag from a previous request to this
            endpoint.
        :returns: generator of
            :class:`GistHistory <github3.gists.history.GistHistory>`

        """
        url = self._build_url('commits', base_url=self._api)
        return self._iter(int(number), url, GistHistory)

    def files(self):
        """Iterator over the files stored in this gist.

        :returns: generator of :class`GistFile <github3.gists.file.GistFile>`

        """
        return iter(self._files)

    def forks(self, number=-1, etag=None):
        """Iterator of forks of this gist.

        .. versionchanged:: 0.9

            Added params ``number`` and ``etag``.

        :param int number: (optional), number of forks to iterate over.
            Default: -1 will iterate over all forks of this gist.
        :param str etag: (optional), ETag from a previous request to this
            endpoint.
        :returns: generator of :class:`Gist <Gist>`

        """
        url = self._build_url('forks', base_url=self._api)
        return self._iter(int(number), url, Gist, etag=etag)

    @requires_auth
    def star(self):
        """Star this gist.

        :returns: bool -- True if successful, False otherwise

        """
        url = self._build_url('star', base_url=self._api)
        return self._boolean(self._put(url), 204, 404)

    @requires_auth
    def unstar(self):
        """Un-star this gist.

        :returns: bool -- True if successful, False otherwise

        """
        url = self._build_url('star', base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)
