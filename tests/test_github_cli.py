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

from click.testing import CliRunner

from gitsome.githubcli import GitHubCli


class GitHubCliTest(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.github_cli = GitHubCli()
        self.limit = 1000

    def test_cli(self):
        result = self.runner.invoke(self.github_cli.cli)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.configure')
    def test_configure(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli, ['configure'])
        mock_gh_call.assert_called_with()
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.create_comment')
    def test_create_comment(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['create-comment', 'u/r/n',
                                     '--text', 'foo'])
        mock_gh_call.assert_called_with('u/r/n', 'foo')
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.create_issue')
    def test_create_issue(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['create-issue', 'u/r',
                                     '--issue_title', 'foo',
                                     '--issue_desc', 'bar'])
        mock_gh_call.assert_called_with('u/r', 'foo', 'bar')
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.create_repo')
    def test_create_repo(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['create-repo', 'r',
                                     '--repo_desc', 'foo',
                                     '--private'])
        mock_gh_call.assert_called_with('r', 'foo', True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.emails')
    def test_emails(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['emails'])
        mock_gh_call.assert_called_with()
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.emojis')
    def test_emojis(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['emojis',
                                     '--pager'])
        mock_gh_call.assert_called_with(True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.feed')
    def test_feed(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['feed', 'u',
                                     '--private', '--pager'])
        mock_gh_call.assert_called_with('u', True, True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.followers')
    def test_followers(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['followers', 'u',
                                     '--pager'])
        mock_gh_call.assert_called_with('u', True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.following')
    def test_following(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['following', 'u',
                                     '--pager'])
        mock_gh_call.assert_called_with('u', True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.gitignore_template')
    def test_gitignore_template(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['gitignore-template', 'l'])
        mock_gh_call.assert_called_with('l')
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.gitignore_templates')
    def test_gitignore_templates(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['gitignore-templates',
                                     '--pager'])
        mock_gh_call.assert_called_with(True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.issue')
    def test_issue(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['issue', 'u/r/n'])
        mock_gh_call.assert_called_with('u/r/n')
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.issues_setup')
    def test_issues(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['issues',
                                     '--issue_filter', 'mentioned',
                                     '--issue_state', 'closed',
                                     '--limit', '10',
                                     '--pager'])
        mock_gh_call.assert_called_with('mentioned', 'closed', 10, True)
        assert result.exit_code == 0
