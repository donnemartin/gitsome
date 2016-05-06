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
import os
from gitsome.compat import configparser
from tests.compat import unittest

from gitsome.github import GitHub
from tests.mock_github_api import MockGitHubApi


class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.github = GitHub()
        self.github.config.api = MockGitHubApi()
        self.github.config.login = mock.Mock()
        self.github.config.authorize = mock.Mock()
        self.github.config.getpass = mock.Mock()

    def test_config(self):
        expected = os.path.join(os.path.abspath(os.environ.get('HOME', '')),
                                self.github.config.CONFIG)
        assert self.github.config \
            .get_github_config_path(self.github.config.CONFIG) == expected

    def test_authenticate_cached_credentials(self):
        self.github.config.user_login = 'foo'
        self.github.config.user_token = 'bar'
        self.github.config.save_config()
        self.github.config.user_login = ''
        self.github.config.user_token = ''
        self.github.config.api = None
        config = self.github.config.get_github_config_path(
            self.github.config.CONFIG)
        parser = configparser.RawConfigParser()
        self.github.config.authenticate_cached_credentials(config, parser)
        assert self.github.config.user_login == 'foo'
        assert self.github.config.user_token == 'bar'
        assert self.github.config.api
