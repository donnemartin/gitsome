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

import re

from .lib.pretty_date_time import pretty_date_time
import click


class Formatter(object):
    """Handles formatting of isssues, repos, threads, etc.

    Attributes:
        * event_type_mapping: A mapping of raw event types to more
            human readable text.
            See: https://developer.github.com/v3/activity/events/types/
    """

    def __init__(self):
        """Inits Formatter.

        Args:
            * None.

        Returns:
            None.
        """
        self.event_type_mapping = {
            'CommitCommentEvent': 'commented on commit',
            'CreateEvent': 'created',
            'DeleteEvent': 'deleted',
            'FollowEvent': 'followed',
            'ForkEvent': 'forked',
            'GistEvent': 'created/updated gist',
            'GollumEvent': 'created/updated wiki',
            'IssueCommentEvent': 'commented on',
            'IssuesEvent': '',
            'MemberEvent': 'added collaborator',
            'MembershipEvent': 'added/removed user',
            'PublicEvent': 'open sourced',
            'PullRequestEvent': '',
            'PullRequestReviewCommentEvent': 'commented on pull request',
            'PushEvent': 'pushed to',
            'ReleaseEvent': 'released',
            'RepositoryEvent': 'created repository',
            'WatchEvent': 'starred',
        }
        self.event_handlers = {
            'CommitCommentEvent': self._format_commit_comment_event,
            'CreateEvent': self._format_create_delete_event,
            'DeleteEvent': self._format_create_delete_event,
            'FollowEvent': self._format_general_event,
            'ForkEvent': self._format_general_event,
            'ForkApplyEvent': self._format_general_event,
            'GistEvent': self._format_general_event,
            'GollumEvent': self._format_general_event,
            'IssueCommentEvent': self._format_issue_commment_event,
            'IssuesEvent': self._format_issues_event,
            'MemberEvent': self._format_general_event,
            'MembershipEvent': self._format_general_event,
            'PublicEvent': self._format_general_event,
            'PullRequestEvent': self._format_pull_request_event,
            'PullRequestReviewCommentEvent': self._format_general_event,
            'PushEvent': self._format_push_event,
            'ReleaseEvent': self._format_general_event,
            'StatusEvent': self._format_general_event,
            'TeamAddEvent': self._format_general_event,
            'RepositoryEvent': self._format_general_event,
            'WatchEvent': self._format_general_event,
        }

    def _format_time(self, event):
        item = click.style(
            ' (' + str(pretty_date_time(event.created_at)) + ')',
            fg='yellow')
        return item

    def _format_issue_comment(self, event, key):
        issue = '{repo[0]}/{repo[1]}#{num}'.format(
            repo=event.payload[key].repository,
            num=event.payload[key].number)
        return click.style(issue, fg='cyan')

    def _format_commit_or_comment(self, message, sha=''):
        indent = '         '
        subsequent_indent = indent if sha == '' else '                  '
        message = self.strip_line_breaks(message)
        formatted_message = click.wrap_text(
            text=click.style(sha, fg='cyan')+message,
            initial_indent=indent,
            subsequent_indent=subsequent_indent)
        return formatted_message

    def _format_sha(self, sha):
        return sha[:7]

    def _format_commit_comment_event(self, event):
        item = click.style(self.event_type_mapping[event.type] + ' ',
                           fg='green')
        item += click.style(
            self._format_sha(event.payload['comment'].commit_id),
            fg='cyan')
        item += click.style(' at ', fg='green')
        item += click.style(self.format_user_repo(event.repo), fg='cyan')
        item += self._format_time(event)
        item += click.style('\n')
        message = self._format_commit_or_comment(event.payload['comment'].body)
        item += click.style(message, fg=None)
        return item

    def _format_create_delete_event(self, event):
        item = click.style(self.event_type_mapping[event.type], fg='green')
        item += click.style(' ' + event.payload['ref_type'], fg='green')
        if event.payload['ref']:
            item += click.style(' ' + event.payload['ref'], fg='cyan')
        item += click.style(' at ', fg='green')
        item += click.style(self.format_user_repo(event.repo), fg='cyan')
        item += self._format_time(event)
        return item

    def _format_issue_commment_event(self, event):
        item = click.style(self.event_type_mapping[event.type] + ' ',
                           fg='green')
        item += self._format_issue_comment(event, key='issue')
        item += self._format_time(event)
        item += click.style('\n')
        message = self._format_commit_or_comment(event.payload['comment'].body)
        item += click.style(message, fg=None)
        return item

    def _format_issues_event(self, event):
        item = click.style(event.payload['action'] + ' issue ', fg='green')
        item += self._format_issue_comment(event, key='issue')
        item += self._format_time(event)
        return item

    def _format_pull_request_event(self, event):
        item = click.style(event.payload['action'] + ' pull request ',
                           fg='green')
        item += self._format_issue_comment(event, key='pull_request')
        item += self._format_time(event)
        return item

    def _format_push_event(self, event):
        item = click.style(self.event_type_mapping[event.type], fg='green')
        branch = event.payload['ref'].split('/')[-1]
        item += click.style(' ' + branch, fg='cyan')
        item += click.style(' at ', fg='green')
        item += click.style(self.format_user_repo(event.repo), fg='cyan')
        item += self._format_time(event)
        for commit in event.payload['commits']:
            item += click.style('\n')
            sha = click.style(self._format_sha(commit['sha']) + ': ', fg=None)
            message = self._format_commit_or_comment(commit['message'], sha=sha)
            item += click.style(message, fg=None)
        return item

    def _format_general_event(self, event):
        item = click.style(self.event_type_mapping[event.type] + ' ',
                           fg='green')
        item += click.style(self.format_user_repo(event.repo), fg='cyan')
        item += self._format_time(event)
        return item

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

    def format_event(self, view_entry):
        """Formats an event.

        Args:
            * view_entry: An instance of github3.events.Event.

        Returns:
            A string representing the formatted item.
        """
        event = view_entry.item
        item = self.format_index_title(view_entry.index, str(event.actor))
        item += self.event_handlers[event.type](event)
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
        item_parts = feed_entry.title.split(' ')
        title = item_parts[0]
        action = item_parts[1:-1]
        repo = item_parts[-1]
        item = self.format_index_title(view_entry.index, title)
        item += click.style(' '.join(action), fg='green')
        item += click.style(' ' + repo + ' ', fg='cyan')
        item += click.style(
            '(' + str(pretty_date_time(feed_entry.updated_parsed)) + ')',
            fg='yellow')
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

    def format_user(self, view_entry):
        """Formats a user.

        Args:
            * view_entry: An instance of github3.users.User.

        Returns:
            A string representing the formatted item.
        """
        user = view_entry.item
        item = self.format_index_title(view_entry.index, user.login)
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

    def format_trending_entry(self, view_entry):
        """Formats a trending repo entry.

        Args:
            * view_entry: A dictionary parsed to include feed URITemplates.

        Returns:
            A string representing the formatted item.
        """
        trending_entry = view_entry.item
        item_parts = trending_entry.title.split(' ')
        title = item_parts[0]
        item = self.format_index_title(view_entry.index, title)
        summary_parts = trending_entry.summary.split('\n')
        summary = summary_parts[0] if len(summary_parts) > 1 else ''
        summary = self.strip_line_breaks(summary)
        language = summary_parts[-1]
        if language == '()':
            language = '(Unknown)'
        language = re.sub(r'(\()', r'', language)
        language = re.sub(r'(\))', r'', language)
        item += click.style(
            '(' + str(pretty_date_time(trending_entry.updated_parsed)) + ')',
            fg='yellow')
        if summary:
            item += '\n'
            summary = click.wrap_text(
                text=summary,
                initial_indent='         ',
                subsequent_indent='         ')
        item += click.style(summary, fg=None)
        item += '\n'
        item += click.style('         Language: ' + language, fg='green')
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

    def strip_line_breaks(self, text):
        """Strips \r and \n characters.

        Args:
            * text: A string representing the text to strip of line breaks.

        Returns:
            A string without line breaks.
        """
        text = re.sub(r'(\r*)', r'', text)
        text = re.sub(r'(\n*)', r'', text)
        return text
