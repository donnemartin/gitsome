# -*- coding: utf-8 -*-
"""
github3.notifications
=====================

This module contains the classes relating to notifications.

See also: http://developer.github.com/v3/activity/notifications/
"""
from __future__ import unicode_literals

from json import dumps
from .models import GitHubCore


class Thread(GitHubCore):
    """The :class:`Thread <Thread>` object wraps notification threads. This
    contains information about the repository generating the notification, the
    subject, and the reason.

    Two thread instances can be checked like so::

        t1 == t2
        t1 != t2

    And is equivalent to::

        t1.id == t2.id
        t1.id != t2.id

    See also:
    http://developer.github.com/v3/activity/notifications/#view-a-single-thread
    """
    def _update_attributes(self, notif):
        self._api = notif.get('url')
        #: Comment responsible for the notification
        self.comment = notif.get('comment', {})
        #: Thread information
        self.thread = notif.get('thread', {})

        from .repos import Repository
        #: Repository the comment was made on
        self.repository = Repository(notif.get('repository', {}), self)
        #: When the thread was last updated
        self.updated_at = self._strptime(notif.get('updated_at'))
        #: Id of the thread
        self.id = notif.get('id')
        #: Dictionary of urls for the thread
        self.urls = notif.get('urls')
        #: datetime object representing the last time the user read the thread
        self.last_read_at = self._strptime(notif.get('last_read_at'))
        #: The reason you're receiving the notification
        self.reason = notif.get('reason')
        #: Subject of the Notification, e.g., which issue/pull/diff is this in
        #: relation to. This is a dictionary
        self.subject = notif.get('subject')
        self.unread = notif.get('unread')

    def _repr(self):
        return '<Thread [{0}]>'.format(self.subject.get('title'))

    def delete_subscription(self):
        """Delete subscription for this thread.

        :returns: bool
        """
        url = self._build_url('subscription', base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    def is_unread(self):
        """Tells you if the thread is unread or not."""
        return self.unread

    def mark(self):
        """Mark the thread as read.

        :returns: bool
        """
        return self._boolean(self._patch(self._api), 205, 404)

    def set_subscription(self, subscribed, ignored):
        """Set the user's subscription for this thread

        :param bool subscribed: (required), determines if notifications should
            be received from this thread.
        :param bool ignored: (required), determines if notifications should be
            ignored from this thread.
        :returns: :class:`Subscription <Subscription>`
        """
        url = self._build_url('subscription', base_url=self._api)
        sub = {'subscribed': subscribed, 'ignored': ignored}
        json = self._json(self._put(url, data=dumps(sub)), 200)
        return self._instance_or_null(Subscription, json)

    def subscription(self):
        """Checks the status of the user's subscription to this thread.

        :returns: :class:`Subscription <Subscription>`
        """
        url = self._build_url('subscription', base_url=self._api)
        json = self._json(self._get(url), 200)
        return self._instance_or_null(Subscription, json)


class Subscription(GitHubCore):

    """This object wraps thread and repository subscription information.

    See also:
    developer.github.com/v3/activity/notifications/#get-a-thread-subscription

    """

    def _update_attributes(self, sub):
        self._api = sub.get('url')
        #: reason user is subscribed to this thread/repository
        self.reason = sub.get('reason')
        #: datetime representation of when the subscription was created
        self.created_at = self._strptime(sub.get('created_at'))
        #: API url of the thread if it exists
        self.thread_url = sub.get('thread_url')
        #: API url of the repository if it exists
        self.repository_url = sub.get('repository_url')
        self.ignored = sub.get('ignored', False)
        self.subscribed = sub.get('subscribed', False)

    def _repr(self):
        return '<Subscription [{0}]>'.format(self.subscribed)

    def delete(self):
        return self._boolean(self._delete(self._api), 204, 404)

    def is_ignored(self):
        return self.ignored

    def is_subscribed(self):
        return self.subscribed

    def set(self, subscribed, ignored):
        """Set the user's subscription for this subscription

        :param bool subscribed: (required), determines if notifications should
            be received from this thread.
        :param bool ignored: (required), determines if notifications should be
            ignored from this thread.
        """
        sub = {'subscribed': subscribed, 'ignored': ignored}
        json = self._json(self._put(self._api, data=dumps(sub)), 200)
        self._update_attributes(json)
