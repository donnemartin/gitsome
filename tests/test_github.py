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

import mock

from compat import unittest

from gitsome.github import GitHub
from tests.mock_feed_parser import MockFeedParser
from tests.mock_github_api import MockGitHubApi
from tests.mock_pretty_date_time import pretty_date_time
from tests.data.email import formatted_emails
from tests.data.emoji import formatted_emojis
from tests.data.events import formatted_events
from tests.data.user import formatted_org, formatted_user, formatted_users
from tests.data.gitignores import formatted_gitignores, formatted_gitignores_tip
from tests.data.issue import formatted_issues, formatted_pull_requests
from tests.data.license import formatted_licenses, formatted_licenses_tip
from tests.data.thread import formatted_threads
from tests.data.trends import formatted_trends
from tests.data.user_feed import formatted_user_feed


class GitHubTest(unittest.TestCase):

    def setUp(self):
        self.github = GitHub()
        self.github.config.api = MockGitHubApi()
        self.github.formatter.pretty_dt = pretty_date_time
        self.github.trend_parser = MockFeedParser()

    def test_avatar_no_pil(self):
        avatar_text = self.github.avatar(
            'https://avatars.githubusercontent.com/u/583231?v=3', False)
        assert avatar_text == 'PIL not found.\n'

    @mock.patch('gitsome.github.click.secho')
    def test_create_comment(self, mock_click_secho):
        self.github.create_comment('user1/repo1/1', 'text')
        mock_click_secho.assert_called_with(
            'Created comment: text',
            fg=self.github.config.clr_message)

    @mock.patch('gitsome.github.click.secho')
    def test_create_comment_invalid_args(self, mock_click_secho):
        self.github.create_comment('invalid/repo1/1', 'text')
        mock_click_secho.assert_called_with(
            'Error creating comment',
            fg=self.github.config.clr_error)
        self.github.create_comment('user1/repo1/foo', 'text')
        mock_click_secho.assert_called_with(
            'Expected argument: user/repo/# and option -t "comment".',
            fg=self.github.config.clr_error)

    @mock.patch('gitsome.github.click.secho')
    def test_create_issue(self, mock_click_secho):
        self.github.create_issue('user1/repo1', 'title', 'desc')
        mock_click_secho.assert_called_with(
            'Created issue: title\ndesc',
            fg=self.github.config.clr_message)

    @mock.patch('gitsome.github.click.secho')
    def test_create_issue_invalid_args(self, mock_click_secho):
        self.github.create_issue('invalid/repo1', 'title', 'desc')
        mock_click_secho.assert_called_with(
            'Error creating issue.',
            fg=self.github.config.clr_error)
        self.github.create_issue('u', 'title', 'desc')
        mock_click_secho.assert_called_with(
            'Expected argument: user/repo and option -t "title".',
            fg=self.github.config.clr_error)

    @mock.patch('gitsome.github.click.secho')
    def test_create_repo(self, mock_click_secho):
        self.github.create_repo('name', 'desc', True)
        mock_click_secho.assert_called_with(
            'Created repo: name\ndesc',
            fg=self.github.config.clr_message)

    @mock.patch('gitsome.github.click.secho')
    def test_create_repo_invalid_args(self, mock_click_secho):
        self.github.create_repo('repo1', 'desc', True)
        mock_click_secho.assert_called_with(
            'Error creating repo: foobar',
            fg=self.github.config.clr_error)

    @mock.patch('gitsome.github.click.secho')
    def test_emails(self, mock_click_secho):
        self.github.emails()
        mock_click_secho.assert_called_with(formatted_emails)

    @mock.patch('gitsome.github.click.secho')
    @mock.patch('gitsome.config.Config.prompt_news_feed')
    def test_feed_config(self, mock_config_prompt_news_feed, mock_click_secho):
        self.github.feed()
        mock_config_prompt_news_feed.assert_called_with()

    @mock.patch('gitsome.github.click.secho')
    def test_feed(self, mock_click_secho):
        self.github.config.user_feed = 'user_feed'
        self.github.feed()
        mock_click_secho.assert_called_with(formatted_user_feed)

    @mock.patch('gitsome.github.click.secho')
    @mock.patch('gitsome.config.Config')
    def test_feed_user(self, mock_config, mock_click_secho):
        self.github.feed('user1')
        mock_click_secho.assert_called_with(formatted_events)

    @mock.patch('gitsome.github.click.secho')
    def test_emojis(self, mock_click_secho):
        self.github.emojis()
        mock_click_secho.assert_called_with(formatted_emojis)

    @mock.patch('gitsome.github.click.secho')
    def test_followers(self, mock_click_secho):
        self.github.followers('foo')
        mock_click_secho.assert_called_with(formatted_users)

    @mock.patch('gitsome.github.click.secho')
    def test_following(self, mock_click_secho):
        self.github.following('foo')
        mock_click_secho.assert_called_with(formatted_users)

    @mock.patch('gitsome.github.click.secho')
    def test_gitignore_template(self, mock_click_secho):
        self.github.gitignore_template('valid_language')
        mock_click_secho.assert_called_with(
            'template',
            fg=self.github.config.clr_message)

    @mock.patch('gitsome.github.click.secho')
    def test_gitignore_template_invalid(self, mock_click_secho):
        self.github.gitignore_template('invalid_language')
        mock_click_secho.assert_called_with(
            ('Invalid case-sensitive template requested, run the '
             'following command to see available templates:\n'
             '    gh gitignores'),
            fg=self.github.config.clr_error)

    @mock.patch('gitsome.github.click.secho')
    def test_gitignore_templates(self, mock_click_secho):
        self.github.gitignore_templates()
        mock_click_secho.assert_any_call(formatted_gitignores)
        mock_click_secho.assert_any_call(formatted_gitignores_tip,
                                         fg=self.github.config.clr_message)

    @mock.patch('gitsome.web_viewer.WebViewer.view_url')
    def test_issue(self, mock_view_url):
        self.github.issue('user1/repo1/1')
        mock_view_url.assert_called_with(
            'https://github.com/user1/repo1/issues/1')

    @mock.patch('gitsome.github.click.secho')
    def test_issue_invalid_args(self, mock_click_secho):
        self.github.issue('user1/repo1/foo')
        mock_click_secho.assert_called_with(
            'Expected argument: user/repo/#.',
            fg=self.github.config.clr_error)

    @mock.patch('gitsome.github.click.secho')
    def test_issues_setup(self, mock_click_secho):
        self.github.issues_setup()
        mock_click_secho.assert_called_with(formatted_issues)

    @mock.patch('gitsome.github.click.secho')
    def test_license(self, mock_click_secho):
        self.github.license('valid_license')
        mock_click_secho.assert_called_with(
            'template',
            fg=self.github.config.clr_message)

    @mock.patch('gitsome.github.click.secho')
    def test_license_invalid(self, mock_click_secho):
        self.github.license('invalid_license')
        mock_click_secho.assert_called_with(
            ('  Invalid case-sensitive license requested, run the '
             'following command to see available licenses:\n'
             '    gh licenses'),
            fg=self.github.config.clr_error)

    @mock.patch('gitsome.github.click.secho')
    def test_licenses(self, mock_click_secho):
        self.github.licenses()
        mock_click_secho.assert_any_call(formatted_licenses)
        mock_click_secho.assert_any_call(formatted_licenses_tip,
                                         fg=self.github.config.clr_message)

    @mock.patch('gitsome.github.click.secho')
    def test_notifications(self, mock_click_secho):
        self.github.notifications()
        mock_click_secho.assert_called_with(formatted_threads)

    @mock.patch('gitsome.github.click.secho')
    def test_octocat(self, mock_click_secho):
        self.github.octocat('foo\\nbar')
        mock_click_secho.assert_called_with(
            'foo\nbar',
            fg=self.github.config.clr_message)

    @mock.patch('gitsome.github.click.secho')
    def test_pull_requests(self, mock_click_secho):
        self.github.pull_requests()
        mock_click_secho.assert_called_with(formatted_pull_requests)

    @mock.patch('gitsome.github.click.secho')
    def test_rate_limit(self, mock_click_secho):
        self.github.rate_limit()
        mock_click_secho.assert_called_with(
            'Rate limit: 5000',
            fg=self.github.config.clr_message)

    @mock.patch('gitsome.web_viewer.WebViewer.view_url')
    def test_repository(self, mock_view_url):
        self.github.repository('user1/repo1')
        mock_view_url.assert_called_with(
            'https://github.com/user1/repo1')

    @mock.patch('gitsome.github.click.secho')
    def test_repository_invalid(self, mock_click_secho):
        self.github.repository('user1/repo1/1')
        mock_click_secho.assert_called_with(
            'Expected argument: user/repo.',
            fg=self.github.config.clr_error)

    @mock.patch('gitsome.github.click.secho')
    @mock.patch('gitsome.github.GitHub.issues')
    def test_search_issues(self, mock_github_issues, mock_click_secho):
        self.github.search_issues('foo')
        mock_github_issues.assert_called_with(
            ['foobar', 'foobar', 'foobar'], 1000, False, sort=False)

    @mock.patch('gitsome.github.click.secho')
    @mock.patch('gitsome.github.GitHub.repositories')
    def test_search_repos(self, mock_github_repositories, mock_click_secho):
        self.github.search_repositories('foo', 'stars')
        mock_github_repositories.assert_called_with(
            ['foobar'], 1000, False, sort=False)

    @mock.patch('gitsome.github.click.secho')
    def test_trending(self, mock_click_secho):
        self.github.trending('Python', False, False, False)
        mock_click_secho.assert_called_with(formatted_trends)

    @mock.patch('gitsome.github.click.secho')
    def test_user(self, mock_click_secho):
        self.github.user('user1')
        mock_click_secho.assert_called_with(formatted_user)
        self.github.user('user2')
        mock_click_secho.assert_called_with(formatted_org)

    @mock.patch('gitsome.github.click.secho')
    def test_user_invalid(self, mock_click_secho):
        self.github.user('invalid_user')
        mock_click_secho.assert_called_with(
            'Invalid user.',
            fg=self.github.config.clr_error)

    @mock.patch('gitsome.github.click.secho')
    @mock.patch('gitsome.github.webbrowser.open')
    def test_user_browser(self, mock_webbrowser_open, mock_click_secho):
        self.github.user('invalid_user', browser=True)
        mock_webbrowser_open.assert_called_with(
            'https://github.com/invalid_user')

    @mock.patch('gitsome.github.click.secho')
    @mock.patch('gitsome.github.webbrowser.open')
    def test_view_browser(self, mock_webbrowser_open, mock_click_secho):
        self.github.config.load_urls = lambda x: ['user1/foo']
        self.github.view(1, view_in_browser=True)
        mock_webbrowser_open.assert_called_with(
            'user1/foo')

    @mock.patch('gitsome.github.click.secho')
    @mock.patch('gitsome.github.GitHub.issue')
    def test_view_issue(self, mock_github_issue, mock_click_secho):
        self.github.config.load_urls = lambda x: ['user1/foo/issues/1']
        self.github.view(0)
        mock_github_issue.assert_called_with('user1/foo/1')

    @mock.patch('gitsome.github.click.secho')
    @mock.patch('gitsome.github.GitHub.repository')
    def test_view_repo(self, mock_github_repository, mock_click_secho):
        self.github.config.load_urls = lambda x: ['user1/foo']
        self.github.view(0)
        mock_github_repository.assert_called_with('user1/foo')

    @mock.patch('gitsome.github.click.secho')
    @mock.patch('gitsome.web_viewer.WebViewer.view_url')
    def test_view_user(self, mock_view_url, mock_click_secho):
        self.github.config.load_urls = lambda x: ['user1']
        self.github.view(0)
        mock_view_url.assert_called_with('https://github.com/user1')
