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
from tests.compat import unittest

from gitsome.github import GitHub
from tests.data.markdown import formatted_markdown, raw_markdown, ssl_error


class WebViewerTest(unittest.TestCase):

    def setUp(self):
        self.github = GitHub()

    def test_format_markdown(self):
        result = self.github.web_viewer.format_markdown(raw_markdown)
        assert result == formatted_markdown

    @mock.patch('gitsome.github.click.echo_via_pager')
    def test_view_url(self, mock_click_echo_via_pager):
        url = 'https://www.github.com/donnemartin/gitsome'
        self.github.web_viewer.view_url(url)
        assert mock_click_echo_via_pager.mock_calls

    @unittest.skip('Skipping test_view_url_ssl_error')
    @mock.patch('gitsome.github.click.echo_via_pager')
    def test_view_url_ssl_error(self, mock_click_echo_via_pager):
        """Temp skipping this test due to a change [undocumented?] in the way
        the requests ssl error sample website is handled:
            http://docs.python-requests.org/en/master/user/advanced/#ssl-cert-verification  # NOQA
        See https://github.com/donnemartin/gitsome/pull/64 for more details.
        """
        url = 'https://requestb.in'
        self.github.web_viewer.view_url(url)
        mock_click_echo_via_pager.assert_called_with(ssl_error, None)
