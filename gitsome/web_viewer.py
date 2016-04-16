# coding: utf-8

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

import platform
import re

from .compat import HTMLParser
from .lib.html2text.html2text import HTML2Text
import click
import requests


class WebViewer(object):
    """Handles viewing of web content within the terminal.

    Attributes:
        * html: .
        * html_to_text: .
    """

    def __init__(self, config):
        self.config = config
        try:
            self.html = HTMLParser.HTMLParser()
        except:
            self.html = HTMLParser
        self.html_to_text = None
        self._init_html_to_text()

    def _init_html_to_text(self):
        """Initializes HTML2Text.

        Args:
            * None.

        Returns:
            None.
        """
        self.html_to_text = HTML2Text()
        self.html_to_text.body_width = 0
        self.html_to_text.ignore_images = False
        self.html_to_text.ignore_emphasis = False
        self.html_to_text.ignore_links = False
        self.html_to_text.skip_internal_links = False
        self.html_to_text.inline_links = False
        self.html_to_text.links_each_paragraph = False

    def format_markdown(self, text):
        """Adds color to the input markdown using click.style.

        Args:
            * text: A string that represents the markdown text.

        Returns:
            A string that has been colorized.
        """
        pattern_url_name = r'[^]]*'
        pattern_url_link = r'[^)]+'
        pattern_url = r'([!]*\[{0}]\(\s*{1}\s*\))'.format(
            pattern_url_name,
            pattern_url_link)
        regex_url = re.compile(pattern_url)
        text = regex_url.sub(click.style(r'\1', fg='green'), text)
        pattern_url_ref_name = r'[^]]*'
        pattern_url_ref_link = r'[^]]+'
        pattern_url_ref = r'([!]*\[{0}]\[\s*{1}\s*\])'.format(
            pattern_url_ref_name,
            pattern_url_ref_link)
        regex_url_ref = re.compile(pattern_url_ref)
        text = regex_url_ref.sub(click.style(r'\1', fg='green'),
                                 text)
        regex_list = re.compile(r'(  \*.*)')
        text = regex_list.sub(click.style(r'\1', fg='cyan'),
                              text)
        regex_header = re.compile(r'(#+) (.*)')
        text = regex_header.sub(click.style(r'\2', fg='yellow'),
                                text)
        regex_bold = re.compile(r'(\*\*|__)(.*?)\1')
        text = regex_bold.sub(click.style(r'\2', fg='cyan'),
                              text)
        regex_code = re.compile(r'(`)(.*?)\1')
        text = regex_code.sub(click.style(r'\1\2\1', fg='cyan'),
                              text)
        text = re.sub(r'(\s*\r?\n\s*){2,}', r'\n\n', text)
        return text
