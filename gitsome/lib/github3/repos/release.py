# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from ..decorators import requires_auth
from ..exceptions import error_for
from ..models import GitHubCore
from .. import utils
from uritemplate import URITemplate


class Release(GitHubCore):

    """The :class:`Release <Release>` object.

    It holds the information GitHub returns about a release from a
    :class:`Repository <github3.repos.repo.Repository>`.

    """

    CUSTOM_HEADERS = {'Accept': 'application/vnd.github.manifold-preview'}

    def _update_attributes(self, release):
        self._api = release.get('url')
        #: List of :class:`Asset <Asset>` objects for this release
        self.original_assets = [
            Asset(i, self) for i in release.get('assets', [])
        ]
        #: URL for uploaded assets
        self.assets_url = release.get('assets_url')
        #: Body of the release (the description)
        self.body = release.get('body')
        #: Date the release was created
        self.created_at = self._strptime(release.get('created_at'))
        #: Boolean whether value is True or False
        self.draft = release.get('draft')
        #: HTML URL of the release
        self.html_url = release.get('html_url')
        #: GitHub id
        self.id = release.get('id')
        #: Name given to the release
        self.name = release.get('name')
        #: Boolean whether release is a prerelease
        self.prerelease = release.get('prerelease')
        #: Date the release was published
        self.published_at = self._strptime(release.get('published_at'))
        #: Name of the tag
        self.tag_name = release.get('tag_name')
        #: URL to download a tarball of the release
        self.tarball_url = release.get('tarball_url')
        #: "Commit" that this release targets
        self.target_commitish = release.get('target_commitish')
        upload_url = release.get('upload_url')
        #: URITemplate to upload an asset with
        self.upload_urlt = URITemplate(upload_url) if upload_url else None
        #: URL to download a zipball of the release
        self.zipball_url = release.get('zipball_url')

    def _repr(self):
        return '<Release [{0}]>'.format(self.name)

    def archive(self, format, path=''):
        """Get the tarball or zipball archive for this release.

        :param str format: (required), accepted values: ('tarball',
            'zipball')
        :param path: (optional), path where the file should be saved
            to, default is the filename provided in the headers and will be
            written in the current directory.
            it can take a file-like object as well
        :type path: str, file
        :returns: bool -- True if successful, False otherwise

        """
        resp = None
        if format in ('tarball', 'zipball'):
            repo_url = self._api[:self._api.rfind('/releases')]
            url = self._build_url(format, self.tag_name, base_url=repo_url)
            resp = self._get(url, allow_redirects=True, stream=True)

        if resp and self._boolean(resp, 200, 404):
            utils.stream_response_to_file(resp, path)
            return True
        return False

    def asset(self, asset_id):
        """Retrieve the asset from this release with ``asset_id``.

        :param int asset_id: ID of the Asset to retrieve
        :returns: :class:`~github3.repos.release.Asset`
        """
        json = None
        if int(asset_id) > 0:
            i = self._api.rfind('/')
            url = self._build_url('assets', str(asset_id),
                                  base_url=self._api[:i])
            json = self._json(self._get(url), 200)
        return self._instance_or_null(Asset, json)

    def assets(self, number=-1, etag=None):
        """Iterate over the assets available for this release.

        :param int number: (optional), Number of assets to return
        :param str etag: (optional), last ETag header sent
        :returns: generator of :class:`Asset <Asset>` objects
        """
        url = self._build_url('assets', base_url=self._api)
        return self._iter(number, url, Asset, etag=etag)

    @requires_auth
    def delete(self):
        """Users with push access to the repository can delete a release.

        :returns: True if successful; False if not successful
        """
        url = self._api
        return self._boolean(
            self._delete(url, headers=Release.CUSTOM_HEADERS),
            204,
            404
        )

    @requires_auth
    def edit(self, tag_name=None, target_commitish=None, name=None, body=None,
             draft=None, prerelease=None):
        """Users with push access to the repository can edit a release.

        If the edit is successful, this object will update itself.

        :param str tag_name: (optional), Name of the tag to use
        :param str target_commitish: (optional), The "commitish" value that
            determines where the Git tag is created from. Defaults to the
            repository's default branch.
        :param str name: (optional), Name of the release
        :param str body: (optional), Description of the release
        :param boolean draft: (optional), True => Release is a draft
        :param boolean prerelease: (optional), True => Release is a prerelease
        :returns: True if successful; False if not successful
        """
        url = self._api
        data = {
            'tag_name': tag_name,
            'target_commitish': target_commitish,
            'name': name,
            'body': body,
            'draft': draft,
            'prerelease': prerelease,
        }
        self._remove_none(data)

        r = self.session.patch(
            url, data=json.dumps(data), headers=Release.CUSTOM_HEADERS
        )

        successful = self._boolean(r, 200, 404)
        if successful:
            # If the edit was successful, let's update the object.
            self._update_attributes(r.json())

        return successful

    @requires_auth
    def upload_asset(self, content_type, name, asset, label=None):
        """Upload an asset to this release.

        All parameters are required.

        :param str content_type: The content type of the asset. Wikipedia has
            a list of common media types
        :param str name: The name of the file
        :param asset: The file or bytes object to upload.
        :param label: (optional), An alternate short description of the asset.
        :returns: :class:`Asset <Asset>`
        """
        headers = {'Content-Type': content_type}
        params = {'name': name, 'label': label}
        self._remove_none(params)
        url = self.upload_urlt.expand(params)
        r = self._post(url, data=asset, json=False, headers=headers)
        if r.status_code in (201, 202):
            return Asset(r.json(), self)
        raise error_for(r)


class Asset(GitHubCore):

    def _update_attributes(self, asset):
        self._api = asset.get('url')
        #: Content-Type provided when the asset was created
        self.content_type = asset.get('content_type')
        #: Date the asset was created
        self.created_at = self._strptime(asset.get('created_at'))
        #: Number of times the asset was downloaded
        self.download_count = asset.get('download_count')
        #: URL to download the asset.
        #: Request headers must include ``Accept: application/octet-stream``.
        self.download_url = self._api
        # User friendly download URL
        self.browser_download_url = asset.get('browser_download_url')
        #: GitHub id of the asset
        self.id = asset.get('id')
        #: Short description of the asset
        self.label = asset.get('label')
        #: Name of the asset
        self.name = asset.get('name')
        #: Size of the asset
        self.size = asset.get('size')
        #: State of the asset, e.g., "uploaded"
        self.state = asset.get('state')
        #: Date the asset was updated
        self.updated_at = self._strptime(asset.get('updated_at'))

    def _repr(self):
        return '<Asset [{0}]>'.format(self.name)

    def download(self, path=''):
        """Download the data for this asset.

        :param path: (optional), path where the file should be saved
            to, default is the filename provided in the headers and will be
            written in the current directory.
            it can take a file-like object as well
        :type path: str, file
        :returns: name of the file, if successful otherwise ``None``
        :rtype: str
        """
        headers = {
            'Accept': 'application/octet-stream'
            }
        resp = self._get(self._api, allow_redirects=False, stream=True,
                         headers=headers)
        if resp.status_code == 302:
            # Amazon S3 will reject the redirected request unless we omit
            # certain request headers
            headers.update({
                'Content-Type': None,
                })

            with self.session.no_auth():
                resp = self._get(resp.headers['location'], stream=True,
                                 headers=headers)

        if self._boolean(resp, 200, 404):
            return utils.stream_response_to_file(resp, path)
        return None

    @requires_auth
    def delete(self):
        """Delete this asset if the user has push access.

        :returns: True if successful; False if not successful
        :rtype: boolean
        """
        url = self._api
        return self._boolean(
            self._delete(url, headers=Release.CUSTOM_HEADERS),
            204,
            404
        )

    def edit(self, name, label=None):
        """Edit this asset.

        :param str name: (required), The file name of the asset
        :param str label: (optional), An alternate description of the asset
        :returns: boolean
        """
        if not name:
            return False
        edit_data = {'name': name, 'label': label}
        self._remove_none(edit_data)
        r = self._patch(
            self._api,
            data=json.dumps(edit_data),
            headers=Release.CUSTOM_HEADERS
        )
        successful = self._boolean(r, 200, 404)
        if successful:
            self._update_attributes(r.json())

        return successful
