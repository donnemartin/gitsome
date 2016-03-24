# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from json import dumps
from ..decorators import requires_auth
from ..models import GitHubCore


class Label(GitHubCore):
    """The :class:`Label <Label>` object. Succintly represents a label that
    exists in a repository.

    See also: http://developer.github.com/v3/issues/labels/
    """
    def _update_attributes(self, label):
        self._api = label.get('url', '')
        #: Color of the label, e.g., 626262
        self.color = label.get('color')
        #: Name of the label, e.g., 'bug'
        self.name = label.get('name')

        self._uniq = self._api

    def _repr(self):
        return '<Label [{0}]>'.format(self)

    def __str__(self):
        return self.name

    @requires_auth
    def delete(self):
        """Delete this label.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def update(self, name, color):
        """Update this label.

        :param str name: (required), new name of the label
        :param str color: (required), color code, e.g., 626262, no leading '#'
        :returns: bool
        """
        json = None

        if name and color:
            if color[0] == '#':
                color = color[1:]
            json = self._json(self._patch(self._api, data=dumps({
                'name': name, 'color': color})), 200)

        if json:
            self._update_attributes(json)
            return True

        return False
