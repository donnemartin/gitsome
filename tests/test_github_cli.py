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

    @mock.patch('gitsome.githubcli.GitHub.license')
    def test_license(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['license', 'l'])
        mock_gh_call.assert_called_with('l')
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.licenses')
    def test_licenses(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['licenses'])
        mock_gh_call.assert_called_with()
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.user_me')
    def test_me(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['me',
                                     '--browser', '--text_avatar',
                                     '--limit', 10,
                                     '--pager'])
        mock_gh_call.assert_called_with(True, True, 10, True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.notifications')
    def test_notifications(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['notifications',
                                     '--limit', 10,
                                     '--pager'])
        mock_gh_call.assert_called_with(10, True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.octocat')
    def test_octocat(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['octo', 'foo'])
        mock_gh_call.assert_called_with('foo')
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.issue')
    def test_pull_request(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['pull-request', 'u/r/n'])
        mock_gh_call.assert_called_with('u/r/n')
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.pull_requests')
    def test_pull_requests(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['pull-requests',
                                     '--limit', 10,
                                     '--pager'])
        mock_gh_call.assert_called_with(10, True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.rate_limit')
    def test_rate_limit(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['rate-limit'])
        mock_gh_call.assert_called_with()
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.repository')
    def test_repository(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['repo', 'u/r'])
        mock_gh_call.assert_called_with('u/r')
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.repositories_setup')
    def test_repositories(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['repos', 'foo',
                                     '--limit', 10,
                                     '--pager'])
        mock_gh_call.assert_called_with('foo', 10, True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.search_issues')
    def test_search_issues(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['search-issues', 'foo',
                                     '--limit', 10,
                                     '--pager'])
        mock_gh_call.assert_called_with('foo', 10, True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.search_repositories')
    def test_search_repositories(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['search-repos', 'foo',
                                     '--sort', 'stars',
                                     '--limit', 10,
                                     '--pager'])
        mock_gh_call.assert_called_with('foo', 'stars', 10, True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.starred')
    def test_starred(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['starred', 'foo',
                                     '--limit', 10,
                                     '--pager'])
        mock_gh_call.assert_called_with('foo', 10, True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.trending')
    def test_trending(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['trending', 'l',
                                     '--pager'])
        mock_gh_call.assert_called_with('l', False, False, False, False, True)
        result = self.runner.invoke(self.github_cli.cli,
                                    ['trending', 'l',
                                     '--weekly',
                                     '--pager'])
        mock_gh_call.assert_called_with('l', True, False, False, False, True)
        result = self.runner.invoke(self.github_cli.cli,
                                    ['trending', 'l',
                                     '--monthly',
                                     '--devs',
                                     '--browser',
                                     '--pager'])
        mock_gh_call.assert_called_with('l', False, True, True, True, True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.user')
    def test_user(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['user', 'foo',
                                     '--browser', '--text_avatar',
                                     '--limit', 10,
                                     '--pager'])
        mock_gh_call.assert_called_with('foo', True, True, 10, True)
        assert result.exit_code == 0

    @mock.patch('gitsome.githubcli.GitHub.view')
    def test_view(self, mock_gh_call):
        result = self.runner.invoke(self.github_cli.cli,
                                    ['view', '1',
                                     '--browser'])
        mock_gh_call.assert_called_with(1, True)
        assert result.exit_code == 0
