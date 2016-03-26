# -*- coding: utf-8 -*-
from ..models import GitHubCore
"""
github3.repos.issue_import
==========================

This module contains the ImportedIssue object for Github's import issue API

"""


class ImportedIssue(GitHubCore):
    """
    The :class:`ImportedIssue <ImportedIssue>` object. This represents
    information from the Import Issue API.

    See also: https://gist.github.com/jonmagic/5282384165e0f86ef105
    """

    IMPORT_CUSTOM_HEADERS = {
        'Accept': 'application/vnd.github.golden-comet-preview+json'
    }

    def _update_attributes(self, json):
        self.id = json.get('id', None)
        self.status = json.get('status', None)
        self.url = json.get('url', None)
        # Since created_at and updated_at returns slightly different format
        # we can't use self._strptime
        # For example, repo correctly returns '2015-04-15T03:40:51Z'
        # For ImportedIssue, the format is '2016-01-14T10:57:56-08:00'
        self.created_at = json.get('created_at', None)
        self.updated_at = json.get('updated_at', None)
        self.import_issues_url = json.get('import_issues_url')
        self.repository_url = json.get('repository_url', None)
