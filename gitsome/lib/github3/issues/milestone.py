# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from json import dumps
from ..decorators import requires_auth
from .label import Label
from ..models import GitHubCore
from ..users import User


class Milestone(GitHubCore):
    """The :class:`Milestone <Milestone>` object. This is a small class to
    handle information about milestones on repositories and issues.

    See also: http://developer.github.com/v3/issues/milestones/
    """
    def _update_attributes(self, mile):
        self._api = mile.get('url', '')
        #: Identifying number associated with milestone.
        self.number = mile.get('number')
        #: State of the milestone, e.g., open or closed.
        self.state = mile.get('state')
        #: Title of the milestone, e.g., 0.2.
        self.title = mile.get('title')
        #: Description of this milestone.
        self.description = mile.get('description')
        #: :class:`User <github3.users.User>` object representing the creator
        #: of the milestone.
        self.creator = None
        if mile.get('creator'):
            self.creator = User(mile.get('creator'), self)
        #: Number of issues associated with this milestone which are still
        #: open.
        self.open_issues = mile.get('open_issues')
        #: The number of closed issues associated with this milestone.
        self.closed_issues = mile.get('closed_issues')
        #: datetime object representing when the milestone was created.
        self.created_at = self._strptime(mile.get('created_at'))
        #: datetime representing when this milestone is due.
        self.due_on = self._strptime(mile.get('due_on'))
        #: datetime object representing when the milestone was updated.
        self.updated_at = self._strptime(mile.get('updated_at'))
        #: string representing the milestone's ID.
        self.id = mile.get('id')

    def _repr(self):
        return '<Milestone [{0}]>'.format(self)

    def __str__(self):
        return self.title

    @requires_auth
    def delete(self):
        """Delete this milestone.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    def labels(self, number=-1, etag=None):
        r"""Iterate over the labels of every associated issue.

        .. versionchanged:: 0.9

            Add etag parameter.

        :param int number: (optional), number of labels to return. Default: -1
            returns all available labels.
        :param str etag: (optional), ETag header from a previous response
        :returns: generator of :class:`Label <github3.issues.label.Label>`\ s
        """
        url = self._build_url('labels', base_url=self._api)
        return self._iter(int(number), url, Label, etag=etag)

    @requires_auth
    def update(self, title=None, state=None, description=None, due_on=None):
        """Update this milestone.

        All parameters are optional, but it makes no sense to omit all of them
        at once.

        :param str title: (optional), new title of the milestone
        :param str state: (optional), ('open', 'closed')
        :param str description: (optional)
        :param str due_on: (optional), ISO 8601 time format:
            YYYY-MM-DDTHH:MM:SSZ
        :returns: bool
        """
        data = {'title': title, 'state': state,
                'description': description, 'due_on': due_on}
        self._remove_none(data)
        json = None

        if data:
            json = self._json(self._patch(self._api, data=dumps(data)), 200)
        if json:
            self._update_attributes(json)
            return True
        return False
