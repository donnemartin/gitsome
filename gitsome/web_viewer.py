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

from __future__ import unicode_literals
from __future__ import print_function

import platform
import re

from .compat import HTMLParser
import click
from .lib.html2text.html2text import HTML2Text
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

    def generate_url_contents(self, url):
        """Generates the formatted contents of the given item's url.

        Converts the HTML to text using HTML2Text, colors it, then displays
            the output in a pager.

        Args:
            * url: A string representing the url.

        Returns:
            A string representation of the formatted url contents.
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}  # NOQA
            raw_response = requests.get(url, headers=headers)
        except (requests.exceptions.SSLError,
                requests.exceptions.ConnectionError) as e:
            contents = 'Error: ' + str(e) + '\n'
            contents += 'Try running hn view # with the --browser/-b flag\n'
            return contents
        contents = self.html_to_text.handle(raw_response.text)
        contents = self.format_markdown(contents)
        return contents

    def view_url(self, url):
        """Views the specified url by displaying it in the terminal.

        Args:
            * url: A string representing the url.

        Returns:
            None.
        """
        contents = self.generate_url_contents(url)
        header = click.style('Viewing ' + url + '\n\n',
                             fg=self.config.clr_message)
        contents = header + contents
        contents += click.style(('\nView this article in a browser with'
                                 ' the -b/--browser flag.\n'),
                                fg=self.config.clr_message)
        contents += click.style(('\nPress q to quit viewing this '
                                 'article.\n'),
                                fg=self.config.clr_message)
        if contents == '{"error":"Not Found"}\n':
            click.secho('Invalid user/repo combination.')
            return
        if platform.system() == 'Windows':
            try:
                click.secho(contents)
            except IOError:
                sys.stderr.close()
        else:
            click.echo_via_pager(contents)
