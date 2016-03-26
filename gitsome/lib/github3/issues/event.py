# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import GitHubCore
from ..users import User


class IssueEvent(GitHubCore):
    """The :class:`IssueEvent <IssueEvent>` object. This specifically deals
    with events described in the
    `Issues\>Events <http://developer.github.com/v3/issues/events>`_ section of
    the GitHub API.

    Two event instances can be checked like so::

        e1 == e2
        e1 != e2

    And is equivalent to::

        e1.commit_id == e2.commit_id
        e1.commit_id != e2.commit_id

    """
    def _update_attributes(self, event):
        # The type of event:
        #   ('closed', 'reopened', 'subscribed', 'merged', 'referenced',
        #    'mentioned', 'assigned')
        #: The type of event, e.g., closed
        self.event = event.get('event')
        #: SHA of the commit.
        self.commit_id = event.get('commit_id')
        self._api = event.get('url', '')

        #: :class:`Issue <github3.issues.Issue>` where this comment was made.
        self.issue = event.get('issue')
        if self.issue:
            from .issue import Issue
            self.issue = Issue(self.issue, self)

        #: :class:`User <github3.users.User>` who caused this event.
        self.actor = event.get('actor')
        if self.actor:
            self.actor = User(self.actor, self)

        #: :class:`User <github3.users.User>` that generated the event.
        self.actor = event.get('actor')
        if self.actor:
            self.actor = User(self.actor, self)

        #: Number of comments
        self.comments = event.get('comments', 0)

        #: datetime object representing when the event was created.
        self.created_at = self._strptime(event.get('created_at'))

        #: Dictionary of links for the pull request
        self.pull_request = event.get('pull_request', {})

        #: Dictionary containing label details
        self.label = event.get('label', {})

        #: The integer ID of the event
        self.id = event.get('id')

        #: :class:`User <github3.users.User>` that is assigned
        self.assignee = event.get('assignee')
        if self.assignee:
            self.assignee = User(self.assignee, self)

        #: Dictionary containing milestone details
        self.milestone = event.get('milestone', {})

        #: Dictionary containing to and from attributes
        self.rename = event.get('rename', {})

        self._uniq = self.commit_id

    def _repr(self):
        return '<Issue Event [{0} by {1}]>'.format(
            self.event, self.actor
            )
