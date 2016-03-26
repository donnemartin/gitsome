# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..models import GitHubCore


class PagesInfo(GitHubCore):
    def _update_attributes(self, info):
        self._api = info.get('url')

        #: Status of the pages site, e.g., built
        self.status = info.get('status')

        #: CName used for the pages site
        self.cname = info.get('cname')

        #: Boolean indicating whether there is a custom 404 for the pages site
        self.custom_404 = info.get('custom_404')

    def _repr(self):
        info = self.cname or ''
        if info:
            info += '/'
        info += self.status or ''
        return '<Pages Info [{0}]>'.format(info)


class PagesBuild(GitHubCore):
    def _update_attributes(self, build):
        self._api = build.get('url')

        #: Status of the pages build, e.g., building
        self.status = build.get('status')

        #: Error dictionary containing the error message
        self.error = build.get('error')

        from ..users import User
        #: :class:`User <github3.users.User>` representing who pushed the
        #: commit
        self.pusher = User(build.get('pusher'))

        #: SHA of the commit that triggered the build
        self.commit = build.get('commit')

        #: Time the build took to finish
        self.duration = build.get('duration')

        #: Datetime the build was created
        self.created_at = self._strptime(build.get('created_at'))

        #: Datetime the build was updated
        self.updated_at = self._strptime(build.get('updated_at'))

    def _repr(self):
        return '<Pages Build [{0}/{1}]>'.format(self.commit, self.status)
