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


class MockIssueComment(object):

    def __init__(self, body):
        self.body = body


class MockLicense(object):

    def __init__(self, key, name):
        self.key = key
        self.name = name


class MockThread(object):

    def __init__(self, thread_type, title, unread):
        self.subject = {
            'title': title,
            'type': thread_type,
            'url': 'https://api.github.com/repos/foo/bar/pulls/1',
        }
        self.unread = unread
        self.updated_at = ''


class MockGitHubApi(object):

    def __init__(self):
        self.users = {}
        self.current_user = 'user1'
        self.ratelimit_remaining = 5000
        self._generate_mock_data()

    def _generate_mock_data(self):
        user1 = MockUser(self.current_user, 'User')
        user1_repo1 = user1.create_repo('repo1')
        user1_repo2 = user1.create_repo('repo2')
        user1_repo3 = user1.create_repo('repo3')
        user1_repo1.create_issue('title1', 'body1')
        user1_repo1.create_issue('title2', 'body2')
        user1_repo1.create_issue('title3', 'body3')
        user1.emails.extend([
            MockEmail('foo@baz.com', True, False),
            MockEmail('bar@baz.com', False, True),
        ])
        user2 = MockUser('user2', 'Organization')
        self.users.update({
            user1.login: user1,
            user2.login: user2,
        })

    def create_issue(self, user_login, repo_name, issue_title, issue_desc):
        try:
            user = self.users[user_login]
            repo = user.repositories[repo_name]
            issue = repo.create_issue(issue_title, issue_desc)
            return issue
        except KeyError:
            return null.NullObject('Issue')

    def create_repository(self, repo_name, repo_desc='', private=False):
        user = self.users[self.current_user]
        return user.create_repo(repo_name, repo_desc, private)

    def emails(self):
        user = self.users[self.current_user]
        return user.emails

    def emojis(self, pager=False):
        return [
            'dolls',
            'palm_tree',
            'uk',
            '100',
            'baby_chick',
        ]

    def followers_of(self, user_login):
        return [
            MockUser('foo1'),
            MockUser('foo2'),
            MockUser('foo3'),
        ]
