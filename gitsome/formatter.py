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

import re

from .lib.pretty_date_time import pretty_date_time
import click


class Formatter(object):
    """Handle formatting of isssues, repos, threads, etc.

    :type config: :class:`config.Config`
    :param config: An instance of config.Config.

    :type event_handlers: dict
    :param event_handlers: A mapping of raw event types to format methods.

    :type event_type_mapping: dict
    :param event_type_mapping: A mapping of raw event types to more
        human readable text.

    :type pretty_dt: :class:`pretty_date_time`
    :param pretty_dt: An instance of pretty_date_time.
    """

    def __init__(self, config):
        self.config = config
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
            'ForkEvent': self._format_fork_event,
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
        self.pretty_dt = pretty_date_time

    def _format_time(self, event):
        """Format time.

        :type event: :class:`github3` Event.
        :param event: An instance of `github3` Event.
        """
        item = click.style(
            ' (' + str(self.pretty_dt(event.created_at)) + ')',
            fg=self.config.clr_time)
        return item

    def _format_issue_comment(self, event, key):
        """Format an issue comment.

        :type event: :class:`github3` Event.
        :param event: An instance of `github3` Event.
        """
        issue = '{repo[0]}/{repo[1]}#{num}'.format(
            repo=event.payload[key].repository,
            num=event.payload[key].number)
        return click.style(issue, fg=self.config.clr_tertiary)

    def _format_commit_comment(self, message, sha=''):
        """Format an issue comment.

        :type message: str
        :param message: The commit comment.

        :type sha: str
        :param sha: The commit hash.
        """
        indent = '         '
        subsequent_indent = indent if sha == '' else '                  '
        message = self.strip_line_breaks(message)
        formatted_message = click.wrap_text(
            text=click.style(sha, fg=self.config.clr_tertiary)+message,
            initial_indent=indent,
            subsequent_indent=subsequent_indent)
        return formatted_message

    def _format_sha(self, sha):
        """Format commit hash.

        :type sha: str
        :param sha: The commit hash.
        """
        return sha[:7]

    def _format_commit_comment_event(self, event):
        """Format commit comment and commit hash.

        :type event: :class:`github3` Event.
        :param event: An instance of `github3` Event.
        """
        item = click.style(self.event_type_mapping[event.type] + ' ',
                           fg=self.config.clr_secondary)
        item += click.style(
            self._format_sha(event.payload['comment'].commit_id),
            fg=self.config.clr_tertiary)
        item += click.style(' at ', fg=self.config.clr_secondary)
        item += click.style(self.format_user_repo(event.repo),
                            fg=self.config.clr_tertiary)
        item += self._format_time(event)
        item += click.style('\n')
        message = self._format_commit_comment(event.payload['comment'].body)
        item += click.style(message, fg=self.config.clr_message)
        return item

    def _format_create_delete_event(self, event):
        """Format a create or delete event.

        :type event: :class:`github3` Event.
        :param event: An instance of `github3` Event.
        """
        item = click.style(self.event_type_mapping[event.type],
                           fg=self.config.clr_secondary)
        item += click.style(' ' + event.payload['ref_type'],
                            fg=self.config.clr_secondary)
        if event.payload['ref']:
            item += click.style(' ' + event.payload['ref'],
                                fg=self.config.clr_tertiary)
        item += click.style(' at ', fg=self.config.clr_secondary)
        item += click.style(self.format_user_repo(event.repo),
                            fg=self.config.clr_tertiary)
        item += self._format_time(event)
        return item

    def _format_fork_event(self, event):
        """Format a repo fork event.

        :type event: :class:`github3` Event.
        :param event: An instance of `github3` Event.
        """
        item = click.style(self.event_type_mapping[event.type],
                           fg=self.config.clr_secondary)
        item += click.style(' ' + self.format_user_repo(event.repo),
                            fg=self.config.clr_tertiary)
        item += self._format_time(event)
        return item

    def _format_issue_commment_event(self, event):
        """Format a repo fork event.

        :type event: :class:`github3` Event.
        :param event: An instance of `github3` Event.
        """
        item = click.style(self.event_type_mapping[event.type] + ' ',
                           fg=self.config.clr_secondary)
        item += self._format_issue_comment(event, key='issue')
        item += self._format_time(event)
        item += click.style('\n')
        message = self._format_commit_comment(event.payload['comment'].body)
        item += click.style(message, fg=self.config.clr_message)
        return item

    def _format_issues_event(self, event):
        """Format an issue event.

        :type event: :class:`github3` Event.
        :param event: An instance of `github3` Event.
        """
        item = click.style(event.payload['action'] + ' issue ',
                           fg=self.config.clr_secondary)
        item += self._format_issue_comment(event, key='issue')
        item += self._format_time(event)
        return item

    def _format_pull_request_event(self, event):
        """Format a pull request event.

        :type event: :class:`github3` Event.
        :param event: An instance of `github3` Event.
        """
        item = click.style(event.payload['action'] + ' pull request ',
                           fg=self.config.clr_secondary)
        item += self._format_issue_comment(event, key='pull_request')
        item += self._format_time(event)
        return item

    def _format_push_event(self, event):
        """Format a push event.

        :type event: :class:`github3` Event.
        :param event: An instance of `github3` Event.
        """
        item = click.style(self.event_type_mapping[event.type],
                           fg=self.config.clr_secondary)
        branch = event.payload['ref'].split('/')[-1]
        item += click.style(' ' + branch, fg=self.config.clr_tertiary)
        item += click.style(' at ', fg=self.config.clr_secondary)
        item += click.style(self.format_user_repo(event.repo),
                            fg=self.config.clr_tertiary)
        item += self._format_time(event)
        for commit in event.payload['commits']:
            item += click.style('\n')
            sha = click.style(self._format_sha(commit['sha']) + ': ',
                              fg=self.config.clr_message)
            message = self._format_commit_comment(commit['message'], sha=sha)
            item += click.style(message, fg=self.config.clr_message)
        return item

    def _format_general_event(self, event):
        """Format an event, general case used by various event types.

        :type event: :class:`github3` Event.
        :param event: An instance of `github3` Event.
        """
        item = click.style(self.event_type_mapping[event.type] + ' ',
                           fg=self.config.clr_secondary)
        item += click.style(self.format_user_repo(event.repo),
                            fg=self.config.clr_tertiary)
        item += self._format_time(event)
        return item

    def format_email(self, view_entry):
        """Format an email.

        :type view_entry: :class:`github3` Email
        :param view_entry: An instance of `github3` Email.

        :rtype: str
        :return: The formattted email.
        """
        email = view_entry.item
        item = self.format_index_title(view_entry.index, email.email)
        item += '\n'
        item += click.style(('        ' + 'Primary: ' +
                             str(email.primary).ljust(7) + ' '),
                            fg=self.config.clr_secondary)
        item += click.style(('Verified: ' +
                             str(email.verified).ljust(5) + ' '),
                            fg=self.config.clr_tertiary)
        return item

    def format_emoji(self, view_entry):
        """Format an emoji.

        :type view_entry: str
        :param view_entry: The emoji name.

        :rtype: str
        :return: The formattted emoji.
        """
        emoji = view_entry.item
        item = self.format_index_title(view_entry.index, emoji)
        return item

    def format_event(self, view_entry):
        """Format an event.

        :type view_entry: :class:`github3` Event
        :param view_entry: An instance of `github3` Event.

        :rtype: str
        :return: The formattted event.
        """
        event = view_entry.item
        item = self.format_index_title(view_entry.index, str(event.actor))
        item += self.event_handlers[event.type](event)
        return item

    def format_gitignore_template_name(self, view_entry):
        """Format a gitignore template name.

        :type view_entry: str
        :param view_entry: The gitignore template name.

        :rtype: str
        :return: The formattted gitignore template name.
        """
        gitignore_template_name = view_entry.item
        item = self.format_index_title(view_entry.index,
                                       gitignore_template_name)
        return item

    def format_feed_entry(self, view_entry):
        """Format a feed entry.

        :type view_entry: dict
        :param view_entry: The URITemplates feed.

        :rtype: str
        :return: The formattted feed entry.
        """
        feed_entry = view_entry.item
        item_parts = feed_entry.title.split(' ')
        title = item_parts[0]
        action = item_parts[1:-1]
        repo = item_parts[-1]
        item = self.format_index_title(view_entry.index, title)
        if action[0] == 'forked':
            item += click.style(action[0] + ' ', fg=self.config.clr_secondary)
            item += click.style(action[1] + ' ', fg=self.config.clr_tertiary)
        else:
            item += click.style(' '.join(action), fg=self.config.clr_secondary)
            item += click.style(' ' + repo + ' ', fg=self.config.clr_tertiary)
        item += click.style(
            '(' + str(self.pretty_dt(feed_entry.updated_parsed)) + ')',
            fg=self.config.clr_time)
        if action[0] == 'commented':
            comment_parts = feed_entry['summary'].split('blockquote')
            if len(comment_parts) > 2:
                comment = comment_parts[-2]
                parts_mention = comment.split('class="user-mention">')
                if len(parts_mention) > 1:
                    comment = parts_mention[1]
                comment = self._format_commit_comment(comment)
                comment = re.sub(r'(</a>*)', r'', comment)
                comment = re.sub(r'(<p>*)', r'', comment)
                comment = re.sub(r'(</p>*)', r'', comment)
                comment = re.sub(r'(</*)', r'', comment)
                comment = re.sub(r'(>      *)', r'', comment)
                item += click.style('\n' + comment, fg=self.config.clr_message)
        return item

    def format_license_name(self, view_entry):
        """Format a license template name.

        :type view_entry: :class:`github3` License
        :param view_entry: An instance of `github3` License.

        :rtype: str
        :return: The formattted license template name.
        """
        license_template_name = view_entry.item
        item = self.format_index_title(view_entry.index,
                                       license_template_name.key)
        item += click.style('(' + license_template_name.name + ')',
                            fg=self.config.clr_secondary)
        return item

    def format_user(self, view_entry):
        """Format a user.

        :type view_entry: :class:`github3` User
        :param view_entry: An instance of `github3` User.

        :rtype: str
        :return: The formattted user.
        """
        user = view_entry.item
        item = self.format_index_title(view_entry.index, user.login)
        return item

    def format_issues_url_from_issue(self, issue):
        """Format the issue url based on the given issue.

        :type issue: :class:`github3` Issue
        :param issue: An instance of `github3` Issue.

        :rtype: str
        :return: The formattted issues url.
        """
        return self.format_user_repo(issue.repository) + '/' + \
            'issues/' + str(issue.number)

    def format_issues_url_from_thread(self, thread):
        """Format the issue url based on the given thread.

        :type issue: :class:`github3` Thread
        :param issue: An instance of `github3` Thread.

        :rtype: str
        :return: The formattted issues url.
        """
        url_parts = thread.subject['url'].split('/')
        user = url_parts[4]
        repo = url_parts[5]
        issues_uri = 'issues'
        issue_id = url_parts[7]
        return '/'.join([user, repo, issues_uri, issue_id])

    def format_index_title(self, index, title):
        """Format an item's index and title.

        :type index: str
        :param index: The index for the given item.

        :type title: str
        :param title: The item's title.

        :rtype: str
        :return: The formatted index and title.
        """
        formatted_index_title = click.style('  ' + (str(index) + '.').ljust(5),
                                            fg=self.config.clr_view_index)
        formatted_index_title += click.style(title + ' ',
                                             fg=self.config.clr_primary)
        return formatted_index_title

    def format_issue(self, view_entry):
        """Format an issue.

        :type view_entry: :class:`github3` Issue
        :param view_entry: An instance of `github3` Issue.

        :rtype: str
        :return: The formatted issue.
        """
        issue = view_entry.item
        item = self.format_index_title(view_entry.index, issue.title)
        item += click.style('@' + str(issue.user) + ' ',
                            fg=self.config.clr_primary)
        item += click.style(('(' +
                             self.format_issues_url_from_issue(issue) +
                             ')'),
                            fg=self.config.clr_view_link)
        item += '\n'
        indent = '        '
        if len(item) == 8:
            item += click.style(('        Score: ' +
                                 str(item[7]).ljust(10) + ' '),
                                fg=self.config.clr_quaternary)
            indent = '  '
        item += click.style((indent + 'State: ' +
                             str(issue.state).ljust(10) + ' '),
                            fg=self.config.clr_secondary)
        item += click.style(('Comments: ' +
                             str(issue.comments_count).ljust(5) + ' '),
                            fg=self.config.clr_tertiary)
        item += click.style(('Assignee: ' +
                             str(issue.assignee).ljust(10) + ' '),
                            fg=self.config.clr_quaternary)
        return item

    def format_repo(self, view_entry):
        """Format a repo.

        :type view_entry: :class:`github3` Repository
        :param view_entry: An instance of `github3` Repository.

        :rtype: str
        :return: The formatted repo.
        """
        repo = view_entry.item
        item = self.format_index_title(view_entry.index, repo.full_name)
        language = repo.language if repo.language is not None else 'Unknown'
        item += click.style('(' + language + ')',
                            fg=self.config.clr_message)
        item += '\n'
        item += click.style(('        ' + 'Stars: ' +
                             str(repo.stargazers_count).ljust(6) + ' '),
                            fg=self.config.clr_secondary)
        item += click.style('Forks: ' + str(repo.forks_count).ljust(6) + ' ',
                            fg=self.config.clr_tertiary)
        item += click.style(('Updated: ' +
                             str(self.pretty_dt(repo.updated_at)) + ' '),
                            fg=self.config.clr_time)
        return item

    def format_thread(self, view_entry):
        """Format a thread.

        :type view_entry: :class:`github3` Thread
        :param view_entry: An instance of `github3` Thread.

        :rtype: str
        :return: The formatted thread.
        """
        thread = view_entry.item
        item = self.format_index_title(view_entry.index,
                                       thread.subject['title'])
        item += click.style('(' + view_entry.url + ')',
                            fg=self.config.clr_view_link)
        item += '\n'
        item += click.style(('        ' + 'Seen: ' +
                             str(not thread.unread).ljust(7) + ' '),
                            fg=self.config.clr_secondary)
        item += click.style(('Type: ' +
                             str(thread.subject['type']).ljust(12) + ' '),
                            fg=self.config.clr_tertiary)
        item += click.style(('Updated: ' +
                             str(self.pretty_dt(thread.updated_at)) + ' '),
                            fg=self.config.clr_time)
        return item

    def format_trending_entry(self, view_entry):
        """Formats a trending repo entry.

        :type view_entry: dict
        :param view_entry: The URITemplates feed.

        :rtype: str
        :return: The formattted trending entry.
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
            '(' + str(self.pretty_dt(trending_entry.updated_parsed)) + ')',
            fg=self.config.clr_time)
        if summary:
            item += '\n'
            summary = click.wrap_text(
                text=summary,
                initial_indent='         ',
                subsequent_indent='         ')
        item += click.style(summary, self.config.clr_message)
        item += '\n'
        item += click.style('         Language: ' + language,
                            fg=self.config.clr_secondary)
        return item

    def format_user_repo(self, user_repo_tuple):
        """Format a repo tuple for pretty print.

        Example:
            Input:  ('donnemartin', 'gitsome')
            Output: donnemartin/gitsome
            Input:  ('repos/donnemartin', 'gitsome')
            Output: donnemartin/gitsome

        :type user_repo_tuple: tuple
        :param user_repo_tuple: The user and repo.

        :rtype: str
        :return: A string of the form user/repo.
        """
        result = '/'.join(user_repo_tuple)
        if result.startswith('repos/'):
            return result[len('repos/'):]
        return result

    def strip_line_breaks(self, text):
        """Strips \r and \n characters.

        :type text: str
        :param text: The text to strip of line breaks.

        :rtype: str
        :return: The input text without line breaks.
        """
        text = re.sub(r'(\r*)', r'', text)
        text = re.sub(r'(\n*)', r'', text)
        return text
