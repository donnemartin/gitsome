# -*- coding: utf-8 -*-
"""
github3.users
=============

This module contains everything relating to Users.

"""
from __future__ import unicode_literals

from json import dumps
from .auths import Authorization
from uritemplate import URITemplate
from .events import Event
from .models import GitHubCore, BaseAccount
from .decorators import requires_auth


class Key(GitHubCore):
    """The :class:`Key <Key>` object. Please see GitHub's `Key Documentation
    <http://developer.github.com/v3/users/keys/>`_ for more information.

    Two key instances can be checked like so::

        k1 == k2
        k1 != k2

    And is equivalent to::

        k1.id == k2.id
        k1.id != k2.id
    """

    def _update_attributes(self, key, session=None):
        self._api = key.get('url', '')
        #: The text of the actual key
        self.key = key.get('key')
        #: The unique id of the key at GitHub
        self.id = key.get('id')
        #: The title the user gave to the key
        self.title = key.get('title')

    def _repr(self):
        return '<User Key [{0}]>'.format(self.title)

    def __str__(self):
        return self.key

    @requires_auth
    def delete(self):
        """Delete this Key"""
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def update(self, title, key):
        """Update this key.

        .. warning::

            As of 20 June 2014, the API considers keys to be immutable.
            This will soon begin to return MethodNotAllowed errors.

        :param str title: (required), title of the key
        :param str key: (required), text of the key file
        :returns: bool
        """
        json = None
        if title and key:
            data = {'title': title, 'key': key}
            json = self._json(self._patch(self._api, data=dumps(data)), 200)
        if json:
            self._update_attributes(json)
            return True
        return False


class Plan(GitHubCore):
    """The :class:`Plan <Plan>` object. This makes interacting with the plan
    information about a user easier. Please see GitHub's `Authenticated User
    <http://developer.github.com/v3/users/#get-the-authenticated-user>`_
    documentation for more specifics.
    """

    def _update_attributes(self, plan):
        #: Number of collaborators
        self.collaborators = plan.get('collaborators')
        #: Name of the plan
        self.name = plan.get('name')
        #: Number of private repos
        self.private_repos = plan.get('private_repos')
        #: Space allowed
        self.space = plan.get('space')

    def _repr(self):
        return '<Plan [{0}]>'.format(self.name)  # (No coverage)

    def __str__(self):
        return self.name

    def is_free(self):
        """Checks if this is a free plan.

        :returns: bool
        """
        return self.name == 'free'  # (No coverage)


class Email(GitHubCore):

    """The :class:`Email` object.

    Please see GitHub's `Emails documentation
    <https://developer.github.com/v3/users/emails/>` for more information.
    """

    def _update_attributes(self, email):
        #: Email address
        self.email = email.get('email')
        #: Whether the address has been verified
        self.verified = email.get('verified')
        #: Whether the address is the primary address
        self.primary = email.get('primary')

    def _repr(self):
        return '<Email [{0}]>'.format(self.email)

    def __str__(self):
        return self.email


class User(BaseAccount):
    """The :class:`User <User>` object. This handles and structures information
    in the `User section <http://developer.github.com/v3/users/>`_.

    Two user instances can be checked like so::

        u1 == u2
        u1 != u2

    And is equivalent to::

        u1.id == u2.id
        u1.id != u2.id

    """

    def _update_attributes(self, user):
        super(User, self)._update_attributes(user)
        if not self.type:
            self.type = 'User'

        #: ID of the user's image on Gravatar
        self.gravatar_id = user.get('gravatar_id', '')
        #: True -- for hire, False -- not for hire
        self.hireable = user.get('hireable', False)

        # The number of public_gists
        #: Number of public gists
        self.public_gists = user.get('public_gists', 0)

        # Private information
        #: How much disk consumed by the user
        self.disk_usage = user.get('disk_usage', 0)

        #: Number of private repos owned by this user
        self.owned_private_repos = user.get('owned_private_repos', 0)
        #: Number of private gists owned by this user
        self.total_private_gists = user.get('total_private_gists', 0)
        #: Total number of private repos
        self.total_private_repos = user.get('total_private_repos', 0)

        #: Which plan this user is on
        self.plan = Plan(user.get('plan', {}))

        events_url = user.get('events_url', '')
        #: Events URL Template. Expands with ``privacy``
        self.events_urlt = URITemplate(events_url) if events_url else None

        #: Followers URL (not a template)
        self.followers_url = user.get('followers_url', '')

        furl = user.get('following_url', '')
        #: Following URL Template. Expands with ``other_user``
        self.following_urlt = URITemplate(furl) if furl else None

        gists_url = user.get('gists_url', '')
        #: Gists URL Template. Expands with ``gist_id``
        self.gists_urlt = URITemplate(gists_url) if gists_url else None

        #: Organizations URL (not a template)
        self.organizations_url = user.get('organizations_url', '')

        #: Received Events URL (not a template)
        self.received_events_url = user.get('received_events_url', '')

        #: Repostories URL (not a template)
        self.repos_url = user.get('repos_url', '')

        starred_url = user.get('starred_url', '')
        #: Starred URL Template. Expands with ``owner`` and ``repo``
        self.starred_urlt = URITemplate(starred_url) if starred_url else None

        #: Subscriptions URL (not a template)
        self.subscriptions_url = user.get('subscriptions_url', '')

        #: Number of repo contributions. Only appears in ``repo.contributors``
        contributions = user.get('contributions')
        # The refresh method uses __init__ to replace the attributes on the
        # instance with what it receives from the /users/:username endpoint.
        # What that means is that contributions is no longer returned and as
        # such is changed because it doesn't exist. This guards against that.
        if contributions is not None:
            self.contributions = contributions

        self._uniq = user.get('id', None)

    def __str__(self):
        return self.login

    def is_assignee_on(self, username, repository):
        """Check if this user can be assigned to issues on username/repository.

        :param str username: owner's username of the repository
        :param str repository: name of the repository
        :returns: True if the use can be assigned, False otherwise
        :rtype: :class:`bool`
        """
        url = self._build_url('repos', username, repository, 'assignees',
                              self.login)
        return self._boolean(self._get(url), 204, 404)

    def is_following(self, username):
        """Checks if this user is following ``username``.

        :param str username: (required)
        :returns: bool

        """
        url = self.following_urlt.expand(other_user=username)
        return self._boolean(self._get(url), 204, 404)

    def events(self, public=False, number=-1, etag=None):
        """Iterate over events performed by this user.

        :param bool public: (optional), only list public events for the
            authenticated user
        :param int number: (optional), number of events to return. Default: -1
            returns all available events.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Event <github3.events.Event>`\ s
        """
        path = ['events']
        if public:
            path.append('public')
        url = self._build_url(*path, base_url=self._api)
        return self._iter(int(number), url, Event, etag=etag)

    def followers(self, number=-1, etag=None):
        """Iterate over the followers of this user.

        :param int number: (optional), number of followers to return. Default:
            -1 returns all available
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <User>`\ s
        """
        url = self._build_url('followers', base_url=self._api)
        return self._iter(int(number), url, User, etag=etag)

    def following(self, number=-1, etag=None):
        """Iterate over the users being followed by this user.

        :param int number: (optional), number of users to return. Default: -1
            returns all available users
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <User>`\ s
        """
        url = self._build_url('following', base_url=self._api)
        return self._iter(int(number), url, User, etag=etag)

    def keys(self, number=-1, etag=None):
        """Iterate over the public keys of this user.

        .. versionadded:: 0.5

        :param int number: (optional), number of keys to return. Default: -1
            returns all available keys
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Key <Key>`\ s
        """
        url = self._build_url('keys', base_url=self._api)
        return self._iter(int(number), url, Key, etag=etag)

    @requires_auth
    def organization_events(self, org, number=-1, etag=None):
        """Iterate over events as they appear on the user's organization
        dashboard. You must be authenticated to view this.

        :param str org: (required), name of the organization
        :param int number: (optional), number of events to return. Default: -1
            returns all available events
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Event <github3.events.Event>`\ s
        """
        url = ''
        if org:
            url = self._build_url('events', 'orgs', org, base_url=self._api)
        return self._iter(int(number), url, Event, etag=etag)

    def received_events(self, public=False, number=-1, etag=None):
        """Iterate over events that the user has received. If the user is the
        authenticated user, you will see private and public events, otherwise
        you will only see public events.

        :param bool public: (optional), determines if the authenticated user
            sees both private and public or just public
        :param int number: (optional), number of events to return. Default: -1
            returns all events available
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Event <github3.events.Event>`\ s
        """
        path = ['received_events']
        if public:
            path.append('public')
        url = self._build_url(*path, base_url=self._api)
        return self._iter(int(number), url, Event, etag=etag)

    def organizations(self, number=-1, etag=None):
        """Iterate over organizations the user is member of

        :param int number: (optional), number of organizations to return.
            Default: -1 returns all available organization
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Event <github3.orgs.Organization>`\ s
        """
        # Import here, because a toplevel import causes an import loop
        from .orgs import Organization
        url = self._build_url('orgs', base_url=self._api)
        return self._iter(int(number), url, Organization, etag=etag)

    def starred_repositories(self, sort=None, direction=None, number=-1,
                             etag=None):
        """Iterate over repositories starred by this user.

        .. versionchanged:: 0.5
           Added sort and direction parameters (optional) as per the change in
           GitHub's API.

        :param int number: (optional), number of starred repos to return.
            Default: -1, returns all available repos
        :param str sort: (optional), either 'created' (when the star was
            created) or 'updated' (when the repository was last pushed to)
        :param str direction: (optional), either 'asc' or 'desc'. Default:
            'desc'
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Repository <github3.repos.Repository>`
        """
        from .repos import Repository

        params = {'sort': sort, 'direction': direction}
        self._remove_none(params)
        url = self.starred_urlt.expand(owner=None, repo=None)
        return self._iter(int(number), url, Repository, params, etag,
                          headers=Repository.STAR_HEADERS)

    def subscriptions(self, number=-1, etag=None):
        """Iterate over repositories subscribed to by this user.

        :param int number: (optional), number of subscriptions to return.
            Default: -1, returns all available
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Repository <github3.repos.Repository>`
        """
        from .repos import Repository
        url = self._build_url('subscriptions', base_url=self._api)
        return self._iter(int(number), url, Repository, etag=etag)

    @requires_auth
    def rename(self, login):
        """Rename the user. This is only available for administrators of
        a GitHub Enterprise instance.

        :param str login: (required), new name of the user
        :returns: bool
        """
        url = self._build_url('admin', 'users', self.id)
        payload = {'login': login}
        resp = self._boolean(self._patch(url, data=payload), 202, 403)
        return resp

    @requires_auth
    def impersonate(self, scopes=None):
        """Obtain an impersonation token for the user.

        The retrieved token will allow impersonation of the user.
        This is only available for admins of a GitHub Enterprise instance.

        :param list scopes: (optional), areas you want this token to apply to,
            i.e., 'gist', 'user'
        :returns: :class:`Authorization <Authorization>`
        """
        url = self._build_url('admin', 'users', self.id, 'authorizations')
        data = {}

        if scopes:
            data['scopes'] = scopes

        json = self._json(self._post(url, data=data), 201)

        return self._instance_or_null(Authorization, json)

    @requires_auth
    def revoke_impersonation(self):
        """Revoke all impersonation tokens for the current user.

        This is only available for admins of a GitHub Enterprise instance.

        :returns: bool -- True if successful, False otherwise
        """
        url = self._build_url('admin', 'users', self.id, 'authorizations')

        return self._boolean(self._delete(url), 204, 403)

    @requires_auth
    def promote(self):
        """Promote a user to site administrator.

        This is only available for admins of a GitHub Enterprise instance.

        :returns: bool -- True if successful, False otherwise
        """
        url = self._build_url('site_admin', base_url=self._api)

        return self._boolean(self._put(url), 204, 403)

    @requires_auth
    def demote(self):
        """Demote a site administrator to simple user.

        You can demote any user account except your own.

        This is only available for admins of a GitHub Enterprise instance.

        :returns: bool -- True if successful, False otherwise
        """
        url = self._build_url('site_admin', base_url=self._api)

        return self._boolean(self._delete(url), 204, 403)

    @requires_auth
    def suspend(self):
        """Suspend the user.

        This is only available for admins of a GitHub Enterprise instance.

        This API is disabled if you use LDAP, check the GitHub API dos for more
        information.

        :returns: bool -- True if successful, False otherwise
        """
        url = self._build_url('suspended', base_url=self._api)

        return self._boolean(self._put(url), 204, 403)

    @requires_auth
    def unsuspend(self):
        """Unsuspend the user.

        This is only available for admins of a GitHub Enterprise instance.

        This API is disabled if you use LDAP, check the GitHub API dos for more
        information.

        :returns: bool -- True if successful, False otherwise
        """
        url = self._build_url('suspended', base_url=self._api)

        return self._boolean(self._delete(url), 204, 403)

    @requires_auth
    def delete(self):
        """Delete the user. Per GitHub API documentation, it is often preferable
        to suspend the user.

        This is only available for admins of a GitHub Enterprise instance.

        :returns: bool -- True if successful, False otherwise
        """
        url = self._build_url('admin', 'users', self.id)
        return self._boolean(self._delete(url), 204, 403)
