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
