# -*- coding: utf-8 -*-
"""
github3
=======

See http://github3.readthedocs.org/ for documentation.

:copyright: (c) 2012-2016 by Ian Cordasco
:license: Modified BSD, see LICENSE for more details

"""

from .__about__ import (
    __package_name__, __title__, __author__, __author_email__,
    __license__, __copyright__, __version__, __version_info__,
    __url__,
)
from .api import (
    authorize, login, enterprise_login, emojis, gist, gitignore_template,
    create_gist, issue, markdown, octocat, organization, pull_request,
    followers_of, followed_by, public_gists, gists_by, issues_on,
    gitignore_templates, all_repositories, all_users, all_events,
    organizations_with, repositories_by, starred_by, subscriptions_for,
    rate_limit, repository, search_code, search_repositories, search_users,
    search_issues, user, zen
)
from .github import GitHub, GitHubEnterprise, GitHubStatus
from .exceptions import (
    BadRequest, AuthenticationFailed, ForbiddenError, GitHubError,
    MethodNotAllowed, NotFoundError, ServerError, NotAcceptable,
    UnprocessableEntity
)

__all__ = (
    'AuthenticationFailed',  'BadRequest', 'ForbiddenError', 'GitHub',
    'GitHubEnterprise', 'GitHubError', 'GitHubStatus',
    'MethodNotAllowed', 'NotAcceptable', 'NotFoundError', 'ServerError',
    'UnprocessableEntity', 'authorize', 'login', 'enterprise_login', 'emojis',
    'gist', 'gitignore_template', 'create_gist', 'issue', 'markdown',
    'octocat', 'organization', 'pull_request', 'followers_of', 'followed_by',
    'public_gists', 'gists_by', 'issues_on', 'gitignore_templates',
    'all_repositories', 'all_users', 'all_events', 'organizations_with',
    'repositories_by', 'starred_by', 'subscriptions_for', 'rate_limit',
    'repository', 'search_code', 'search_repositories', 'search_users',
    'search_issues', 'user', 'zen',
    # Metadata attributes
    '__package_name__', '__title__', '__author__', '__author_email__',
    '__license__', '__copyright__', '__version__', '__version_info__',
    '__url__',
)
