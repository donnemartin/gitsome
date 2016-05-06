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

from __future__ import unicode_literals
from __future__ import print_function

from datetime import datetime
import mock
import pytz

from gitsome.lib.github3 import null
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
        self.feed_events = []

    def events(self, public):
        feed_events = []
        feed_events.append(MockEvent(
            event_type='CommitCommentEvent',
            payload={
                'comment': MockRepoComment(),
            }))
        feed_events.append(MockEvent(
            event_type='CreateEvent',
            payload={
                'ref_type': 'branch',
                'ref': 'master',
            }))
        feed_events.append(MockEvent(
            event_type='FollowEvent'))
        feed_events.append(MockEvent(
            event_type='ForkEvent'))
        feed_events.append(MockEvent(
            event_type='IssueCommentEvent',
            payload={
                'comment': MockIssueComment('foo'),
                'issue': MockIssue('1', MockRepo(self, 'repo1'), 'foo'),
            }))
        feed_events.append(MockEvent(
            event_type='IssuesEvent',
            payload={
                'action': 'closed',
                'issue': MockIssue('1', MockRepo(self, 'repo1'), 'foo'),
            }))
        feed_events.append(MockEvent(
            event_type='PullRequestEvent',
            payload={
                'action': 'closed',
                'pull_request': MockIssue('1', MockRepo(self, 'repo1'), 'foo'),
            }))
        feed_events.append(MockEvent(
            event_type='PushEvent',
            payload={
                'ref': 'refs/heads/master',
                'commits': [{'url': 'https://api.github.com/repos/donnemartin/gitsome/commits/5ee4d1b20ee7cb16cd5be19b103301541a41003f', 'message': 'Fix GitHubCli class docstring', 'distinct': True, 'author': {'email': 'donne.martin@gmail.com', 'name': 'Donne Martin'}, 'sha': '5ee4d1b20ee7cb16cd5be19b103301541a41003f'}, {'url': 'https://api.github.com/repos/donnemartin/gitsome/commits/fc2309b645313646a3792eca9e0e9168cf25b267', 'message': 'Update gh configure docstring', 'distinct': True, 'author': {'email': 'donne.martin@gmail.com', 'name': 'Donne Martin'}, 'sha': 'fc2309b645313646a3792eca9e0e9168cf25b267'}, {'url': 'https://api.github.com/repos/donnemartin/gitsome/commits/dde19b7685ad7a07872fea1b4dc8019585322fdb', 'message': 'Update gh create-comment docstring', 'distinct': True, 'author': {'email': 'donne.martin@gmail.com', 'name': 'Donne Martin'}, 'sha': 'dde19b7685ad7a07872fea1b4dc8019585322fdb'}]  # NOQA
            }))
        return feed_events

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


class MockRepoComment(object):

    def __init__(self):
        self.commit_id = 'AAA23e2c6cb6997d25cfe61673aea6d701e9bZZZ'
        self.body = 'foo'


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


class MockEvent(object):

    def __init__(self, event_type, payload=''):
        self.id = 1
        self.created_at = datetime.now(pytz.utc)
        self.actor = 'donnemartin'
        self.org = 'org'
        self.type = event_type
        self.payload = payload
        self.repo = ('user1', 'repo1')
        self.public = True


class MockGitHubApi(object):

    def __init__(self):
        self.users = {}
        self.current_user = 'user1'
        self.ratelimit_remaining = 5000
        self._generate_mock_data()

    def _generate_mock_data(self):
        user1 = MockUser(self.current_user, 'User')
        user1_repo1 = user1.create_repo('repo1')
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

    def followed_by(self, user_login):
        return self.followers_of(user_login)

    def gitignore_template(self, language):
        if language == 'valid_language':
            return 'template'
        else:
            return ''

    def gitignore_templates(self):
        return [
            'Actionscript',
            'Ada',
            'Agda',
            'Android',
            'AppEngine',
        ]

    def issue(self, user_login, repo_name, number):
        try:
            user = self.users[user_login]
            repo = user.repositories[repo_name]
            return repo.issues[int(number)]
        except KeyError:
            return null.NullObject('Issue')

    def issues(self, issue_filter='subscribed', issue_state='open'):
        user = self.users[self.current_user]
        repo = user.repositories['repo1']
        issues_dict = repo.issues
        issues = list(issues_dict.values())
        return issues

    def license(self, license):
        if license == 'valid_license':
            template = mock.Mock()
            template.body = 'template'
            return template
        else:
            return null.NullObject('License')

    def licenses(self):
        return [
            MockLicense('mit', '(MIT License)'),
            MockLicense('gpl-2.0', '(GNU General Public License v2.0)'),
            MockLicense('bsd-2-clause', '(BSD 2-clause "Simplified" License)'),
            MockLicense('isc', '(ISC License)'),
            MockLicense('epl-1.0', '(Eclipse Public License 1.0)'),
        ]

    def notifications(self, all=True, participating=False):
        return [
            MockThread('type1', 'title1', True),
            MockThread('type2', 'title2', False),
            MockThread('type3', 'title3', True),
        ]

    def octocat(self, say):
        return say

    def pull_request(self, owner, repository, number):
        pull_requests = self.issues()
        return pull_requests[0]

    def search_issues(self, query):
        return self.issues()

    def search_repositories(self, query, sort):
        return self.repositories()

    def repositories(self, user_id=None):
        if user_id is None:
            user_id = self.current_user
        user = self.users[user_id]
        repos = list(user.repositories.values())
        repos_sorted = sorted(repos)
        return repos_sorted

    def user(self, user_id):
        try:
            return self.users[user_id]
        except KeyError:
            return null.NullObject('User')
