# -*- coding: utf-8 -*-
"""
github3.events
==============

This module contains the class(es) related to Events

"""
from __future__ import unicode_literals

from .models import GitHubCore


class Event(GitHubCore):

    """The :class:`Event <Event>` object. It structures and handles the data
    returned by via the `Events <http://developer.github.com/v3/events>`_
    section of the GitHub API.

    Two events can be compared like so::

        e1 == e2
        e1 != e2

    And that is equivalent to::

        e1.id == e2.id
        e1.id != e2.id

    """

    def _update_attributes(self, event):
        from .users import User
        from .orgs import Organization
        #: :class:`User <github3.users.User>` object representing the actor.
        self.actor = User(event.get('actor')) if event.get('actor') else None
        #: datetime object representing when the event was created.
        self.created_at = self._strptime(event.get('created_at'))
        #: Unique id of the event
        self.id = event.get('id')
        #: List all possible types of Events
        self.org = None
        if event.get('org'):
            self.org = Organization(event.get('org'))
        #: Event type http://developer.github.com/v3/activity/events/types/
        self.type = event.get('type')
        handler = _payload_handlers.get(self.type, identity)
        #: Dictionary with the payload. Payload structure is defined by type_.
        #  _type: http://developer.github.com/v3/events/types
        self.payload = handler(event.get('payload'), self)
        #: Return ``tuple(owner, repository_name)``
        self.repo = event.get('repo')
        if self.repo is not None:
            self.repo = tuple(self.repo['name'].split('/'))
        #: Indicates whether the Event is public or not.
        self.public = event.get('public')

    def _repr(self):
        return '<Event [{0}]>'.format(self.type[:-5])

    @staticmethod
    def list_types():
        """List available payload types."""
        return sorted(_payload_handlers.keys())


def _commitcomment(payload, session):
    from .repos.comment import RepoComment
    if payload.get('comment'):
        payload['comment'] = RepoComment(payload['comment'], session)
    return payload


def _follow(payload, session):
    from .users import User
    if payload.get('target'):
        payload['target'] = User(payload['target'], session)
    return payload


def _forkev(payload, session):
    from .repos import Repository
    if payload.get('forkee'):
        payload['forkee'] = Repository(payload['forkee'], session)
    return payload


def _gist(payload, session):
    from .gists import Gist
    if payload.get('gist'):
        payload['gist'] = Gist(payload['gist'], session)
    return payload


def _issuecomm(payload, session):
    from .issues import Issue
    from .issues.comment import IssueComment
    if payload.get('issue'):
        payload['issue'] = Issue(payload['issue'], session)
    if payload.get('comment'):
        payload['comment'] = IssueComment(payload['comment'], session)
    return payload


def _issueevent(payload, session):
    from .issues import Issue
    if payload.get('issue'):
        payload['issue'] = Issue(payload['issue'], session)
    return payload


def _member(payload, session):
    from .users import User
    if payload.get('member'):
        payload['member'] = User(payload['member'], session)
    return payload


def _pullreqev(payload, session):
    from .pulls import PullRequest
    if payload.get('pull_request'):
        payload['pull_request'] = PullRequest(payload['pull_request'],
                                              session)
    return payload


def _pullreqcomm(payload, session):
    from .pulls import PullRequest, ReviewComment
    # Transform the Pull Request attribute
    pull = payload.get('pull_request')
    if pull:
        payload['pull_request'] = PullRequest(pull, session)

    # Transform the Comment attribute
    comment = payload.get('comment')
    if comment:
        payload['comment'] = ReviewComment(comment, session)
    return payload


def _release(payload, session):
    from .repos.release import Release
    release = payload.get('release')
    if release:
        payload['release'] = Release(release, session)
    return payload


def _team(payload, session):
    from .orgs import Team
    from .repos import Repository
    from .users import User
    if payload.get('team'):
        payload['team'] = Team(payload['team'], session)
    if payload.get('repo'):
        payload['repo'] = Repository(payload['repo'], session)
    if payload.get('sender'):
        payload['sender'] = User(payload['sender'], session)
    return payload


def identity(x, session):
    return x


_payload_handlers = {
    'CommitCommentEvent': _commitcomment,
    'CreateEvent': identity,
    'DeleteEvent': identity,
    'FollowEvent': _follow,
    'ForkEvent': _forkev,
    'ForkApplyEvent': identity,
    'GistEvent': _gist,
    'GollumEvent': identity,
    'IssueCommentEvent': _issuecomm,
    'IssuesEvent': _issueevent,
    'MemberEvent': _member,
    'PublicEvent': identity,
    'PullRequestEvent': _pullreqev,
    'PullRequestReviewCommentEvent': _pullreqcomm,
    'PushEvent': identity,
    'ReleaseEvent': _release,
    'StatusEvent': identity,
    'TeamAddEvent': _team,
    'WatchEvent': identity,
}
