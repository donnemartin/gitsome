# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import mock

from gitsome.lib.github3.exceptions import UnprocessableEntity


class MockEmail(object):

    def __init__(self, email, primary=False, verified=False):
        self.email = email
        self.primary = primary
        self.verified = verified


class MockUser(object):

    def __init__(self, login, user_type='User'):
        self.login = login
        self.repositories = {}
        self.emails = []
        self.avatar_url = 'https://www.github.com'
        self.company = 'bigcorp'
        self.location = 'interwebz'
        self.email = login + '@foo.com'
        self.type = user_type
        self.followers_count = 0
        self.following_count = 0

    def raise_mock_unprocessableentity(self):
        response = mock.Mock()
        response.json = lambda: exec('raise(Exception())')
        response.content = 'foobar'
        raise UnprocessableEntity(response)

    def create_repo(self, name, desc='', private=False):
        if name in self.repositories:
            self.raise_mock_unprocessableentity()
        repo = MockRepo(self, name, desc, private)
        self.repositories.update({repo.full_name: repo})
        return repo

    def events(self, public):
        return []


class MockRepo(object):

    def __init__(self, user, full_name, description='', private=False):
        self.user = user
        self.full_name = full_name
        self.description = description
        self.private = private
        self.issues = {}
        self.clone_url = 'https://github.com/octocat/spoon-knife'
        self.stargazers_count = 1
        self.forks_count = 1
        self.language = ''
        self.updated_at = ''
        self.repository = 'foobar'

    def __lt__(self, other):
        return self.full_name < other.full_name

    def gen_key(self):
        return len(self.issues) + 1

    def create_issue(self, issue_title, issue_desc=''):
        number = self.gen_key()
        issue = MockIssue(number, self, issue_title, issue_desc)
        self.issues.update({number: issue})
        return issue

    def pull_requests(self):
        return list(self.issues.values())


class MockIssue(object):

    def __init__(self, number, repository, title, body=''):
        self.number = number
        self.repository = (repository.user.login, repository.full_name)
        self.title = title
        self.body = body
        self.state = 'open'
        self.comments_count = 1
        self.assignee = 'user1'
        self.user = 'user2'
        self.created_at = ''
        self.comments = []
        self.issue = 'foobar'

    def create_comment(self, body):
        issue_comment = MockIssueComment(body)
        self.comments.append(issue_comment)
        return issue_comment
