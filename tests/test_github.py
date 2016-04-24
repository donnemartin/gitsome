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

from __future__ import print_function
from __future__ import division

import mock

from compat import unittest

from gitsome.github import GitHub


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

    # @mock.patch('gitsome.github.click.secho')
    # @mock.patch('gitsome.config.Config')
    # def test_feed_user(self, mock_config, mock_click_secho):
    #     self.github.feed('user1')
    #     print(mock_click_secho.mock_calls)
    #     print(mock_config.api.mock_calls)
    #     mock_click_secho.assert_called_with(formatted_user_feed)

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
