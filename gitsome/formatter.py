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

from .lib.pretty_date_time import pretty_date_time
import click


class Formatter(object):
    """Handles formatting of isssues, repos, threads, etc.

    Attributes:
        * None.
    """

    def format_email(self, view_entry):
        """Formats an email.

        Args:
            * view_entry: An instance of a github3.users.Email.

        Returns:
            A string representing the formatted item.
        """
        email = view_entry.item
        item = self.format_index_title(view_entry.index, email.email)
        item += '\n'
        item += click.style(('        ' + 'Primary: ' +
                             str(email.primary).ljust(7) + ' '),
                            fg='green')
        item += click.style(('Verified: ' +
                             str(email.verified).ljust(5) + ' '),
                            fg='cyan')
        return item

    def format_emoji(self, view_entry):
        """Formats an emoji.

        Args:
            * view_entry: A string representing an emoji name.

        Returns:
            A string representing the formatted item.
        """
        emoji = view_entry.item
        item = self.format_index_title(view_entry.index, emoji)
        return item

    def format_gitignore_template_name(self, view_entry):
        """Formats a gitignore template name.

        Args:
            * view_entry: A string representing a gitignore template name.

        Returns:
            A string representing the formatted item.
        """
        gitignore_template_name = view_entry.item
        item = self.format_index_title(view_entry.index,
                                       gitignore_template_name)
        return item

    def format_feed_entry(self, view_entry):
        """Formats a feed entry.

        Args:
            * view_entry: A dictionary parsed to include feed URITemplates.

        Returns:
            A string representing the formatted item.
        """
        feed_entry = view_entry.item
        item = self.format_index_title(view_entry.index,
                                       feed_entry.title)
        from datetime import datetime
        item += click.style(
            '(' + str(pretty_date_time(feed_entry.published_parsed)) + ')',
            fg=None)
        return item

    def format_license_name(self, view_entry):
        """Formats a license template name.

        Args:
            * view_entry: An instance of github3.licenses.License.

        Returns:
            A string representing the formatted item.
        """
        license_template_name = view_entry.item
        item = self.format_index_title(view_entry.index,
                                       license_template_name.key)
        item += click.style('(' + license_template_name.name + ')', fg=None)
        return item

    def format_issues_url_from_issue(self, issue):
        """Formats the issue url based on the given issue.

        Args:
            * thread: An instance of github3.issues.Issue.

        Returns:
            A string representing the formatted issues url.
        """
        return self.format_user_repo(issue.repository) + '/' + \
            'issues/' + str(issue.number)

    def format_issues_url_from_thread(self, thread):
        """Formats the issue url based on the given thread.

        Args:
            * thread: An instance of github3.notifications.Thread.

        Returns:
            A string representing the formatted issues url.
        """
        url_parts = thread.subject['url'].split('/')
        user = url_parts[4]
        repo = url_parts[5]
        issues_uri = 'issues'
        issue_id = url_parts[7]
        return '/'.join([user, repo, issues_uri, issue_id])

    def format_index_title(self, index, title):
        """Formats and item's index and title.

        Args:
            * index: An int that specifies the index for the given item.
            * title: A string that represents the item's title.

        Returns:
            A string representation of the formatted index and title.
        """
        formatted_index_title = click.style('  ' + (str(index) + '.').ljust(5),
                                            fg='magenta')
        formatted_index_title += click.style(title + ' ',
                                             fg='white')
        return formatted_index_title

    def format_issue(self, view_entry):
        """Formats an issue.

        Args:
            * view_entry: An instance of github3.issue.Issue.

        Returns:
            A string representing the formatted item.
        """
        issue = view_entry.item
        item = self.format_index_title(view_entry.index, issue.title)
        item += click.style('@' + str(issue.user) + ' ', fg='white')
        item += click.style(('(' +
                             self.format_issues_url_from_issue(issue) +
                             ')'),
                            fg='magenta')
        item += '\n'
        indent = '        '
        if len(item) == 8:
            item += click.style(('        Score: ' +
                                 str(item[7]).ljust(10) + ' '),
                                fg='yellow')
            indent = '  '
        item += click.style((indent + 'State: ' +
                             str(issue.state).ljust(10) + ' '),
                            fg='green')
        item += click.style(('Comments: ' +
                             str(issue.comments_count).ljust(5) + ' '),
                            fg='cyan')
        item += click.style(('Assignee: ' +
                             str(issue.assignee).ljust(10) + ' '),
                            fg='yellow')
        return item

    def format_repo(self, view_entry):
        """Formats a repo.

        Args:
            * view_entry: An instance of github3.repo.Repository.

        Returns:
            A string representing the formatted item.
        """
        repo = view_entry.item
        item = self.format_index_title(view_entry.index, repo.full_name)
        language = repo.language if repo.language is not None else 'Unknown'
        item += click.style('(' + language + ')',
                            fg=None)
        item += '\n'
        item += click.style(('        ' + 'Stars: ' +
                             str(repo.stargazers_count).ljust(5) + ' '),
                            fg='green')
        item += click.style('Forks: ' + str(repo.forks_count).ljust(4) + ' ',
                            fg='cyan')
        item += click.style(('Updated: ' +
                             str(pretty_date_time(repo.updated_at)) + ' '),
                            fg='yellow')
        return item

    def format_thread(self, view_entry):
        """Formats a thread.

        Args:
            * view_entry: An instance of github3.notifications.Thread.

        Returns:
            A string representing the formatted item.
        """
        thread = view_entry.item
        item = self.format_index_title(view_entry.index,
                                       thread.subject['title'])
        item += click.style('(' + view_entry.url + ')',
                            fg='magenta')
        item += '\n'
        item += click.style(('        ' + 'Seen: ' +
                             str(not thread.unread).ljust(7) + ' '),
                            fg='green')
        item += click.style(('Type: ' +
                             str(thread.subject['type']).ljust(12) + ' '),
                            fg='cyan')
        item += click.style(('Updated: ' +
                             str(pretty_date_time(thread.updated_at)) + ' '),
                            fg='yellow')
        return item

    def format_user_repo(self, repo):
        """Formats a repo tuple for pretty print.

        Example:
            Input:  ('donnemartin', 'gitsome')
            Output: donnemartin/gitsome
            Input:  ('repos/donnemartin', 'gitsome')
            Output: donnemartin/gitsome

        Args:
            * args: A tuple that contains the user and repo.

        Returns:
            A string of the form user/repo.
        """
        result = '/'.join(repo)
        if result.startswith('repos/'):
            return result[len('repos/'):]
        return result
