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

import click

from .github import GitHub


click.disable_unicode_literals_warning = True
pass_github = click.make_pass_decorator(GitHub)


class GitHubCli(object):
    """The GitHubCli, builds `click` commands and runs `GitHub` methods."""

    @click.group()
    @click.pass_context
    def cli(ctx):
        """Main entry point for GitHubCli.

        :type ctx: :class:`click.core.Context`
        :param ctx: An instance of click.core.Context that stores an instance
            of `github.GitHub`.
        """
        # Create a GitHub object and remember it as the context object.
        # From this point onwards other commands can refer to it by using the
        # @pass_github decorator.
        ctx.obj = GitHub()

    @cli.command()
    @click.option('-e', '--enterprise', is_flag=True)
    @pass_github
    def configure(github, enterprise):
        """Configure gitsome.

        Attempts to authenticate the user and to set up the user's news feed.

        Usage/Example(s):
            gh configure
            gh configure -e
            gh configure --enterprise

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.
        :type enterprise: bool
        :param enterprise: Determines whether to configure GitHub Enterprise.
            Default: False.
        """
        github.configure(enterprise)

    @cli.command('create-comment')
    @click.argument('user_repo_number')
    @click.option('-t', '--text')
    @pass_github
    def create_comment(github, user_repo_number, text):
        """Create a comment on the given issue.

        Usage:
            gh create-comment [user_repo_number] [-t/--text]

        Example(s):
            gh create-comment donnemartin/saws/1 -t "hello world"
            gh create-comment donnemartin/saws/1 --text "hello world"

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type user_repo_number: str
        :param user_repo_number: The user/repo/issue_number.

        :type text: str
        :param text: The comment text.
        """
        github.create_comment(user_repo_number, text)

    @cli.command('create-issue')
    @click.argument('user_repo')
    @click.option('-t', '--issue_title')
    @click.option('-d', '--issue_desc', required=False)
    @pass_github
    def create_issue(github, user_repo, issue_title, issue_desc):
        """Create an issue.

        Usage:
            gh create-issue [user_repo] [-t/--issue_title] [-d/--issue_desc]

        Example(s):
            gh create-issue donnemartin/gitsome -t "title"
            gh create-issue donnemartin/gitsome -t "title" -d "desc"
            gh create-issue donnemartin/gitsome --issue_title "title" --issue_desc "desc"  # NOQA

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type user_repo: str
        :param user_repo: The user/repo.

        :type issue_title: str
        :param issue_title: The issue title.

        :type issue_desc: str
        :param issue_desc: The issue body (optional).
        """
        github.create_issue(user_repo, issue_title, issue_desc)

    @cli.command('create-repo')
    @click.argument('repo_name')
    @click.option('-d', '--repo_desc', required=False)
    @click.option('-pr', '--private', is_flag=True)
    @pass_github
    def create_repo(github, repo_name, repo_desc, private):
        """Create a repo.

        Usage:
            gh create-repo [repo_name] [-d/--repo_desc] [-pr/--private]

        Example(s):
            gh create-repo repo_name
            gh create-repo repo_name -d "desc"
            gh create-repo repo_name --repo_desc "desc"
            gh create-repo repo_name -pr
            gh create-repo repo_name --repo_desc "desc" --private

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type repo_name: str
        :param repo_name: The repo name.

        :type repo_desc: str
        :param repo_desc: The repo description (optional).

        :type private: bool
        :param private: Determines whether the repo is private.  Default: False.
        """
        github.create_repo(repo_name, repo_desc, private)

    @cli.command()
    @pass_github
    def emails(github):
        """List all the user's registered emails.

        Usage/Example(s):
            gh emails

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.
        """
        github.emails()

    @cli.command()
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def emojis(github, pager):
        """List all GitHub supported emojis.

        Usage:
            gh emojis [-p/--pager]

        Example(s):
            gh emojis | grep octo

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.emojis(pager)

    @cli.command()
    @click.argument('user_or_repo', required=False, default='')
    @click.option('-pr', '--private', is_flag=True, default=False)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def feed(github, user_or_repo, private, pager):
        """List all activity for the given user or repo.

        If `user_or_repo` is not provided, uses the logged in user's news feed
        seen while visiting https://github.com.  If `user_or_repo` is provided,
        shows either the public or `[-pr/--private]` feed activity of the user
        or repo.

        Usage:
            gh feed [user_or_repo] [-pr/--private] [-p/--pager]

        Examples:
            gh feed
            gh feed | grep foo
            gh feed donnemartin
            gh feed donnemartin -pr -p
            gh feed donnemartin --private --pager
            gh feed donnemartin/haxor-news -p

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type user_or_repo: str
        :param user_or_repo: The user or repo to list events for (optional).
            If no entry, defaults to the logged in user's feed.

        :type private: bool
        :param private: Determines whether to show the private events (True)
            or public events (False).

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.feed(user_or_repo, private, pager)

    @cli.command()
    @click.argument('user', required=False)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def followers(github, user, pager):
        """List all followers and the total follower count.

        Usage:
            gh followers [user] [-p/--pager]

        Example(s):
            gh followers
            gh followers -p
            gh followers octocat --pager

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type user: str
        :param user: The user login (optional).
            If None, returns the followers of the logged in user.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.followers(user, pager)

    @cli.command()
    @click.argument('user', required=False)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def following(github, user, pager):
        """List all followed users and the total followed count.

        Usage:
            gh following [user] [-p/--pager]

        Example(s):
            gh following
            gh following -p
            gh following octocat --pager

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type user: str
        :param user: The user login.
            If None, returns the followed users of the logged in user.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.following(user, pager)

    @cli.command('gitignore-template')
    @click.argument('language')
    @pass_github
    def gitignore_template(github, language):
        """Output the gitignore template for the given language.

        Usage:
            gh gitignore-template [language]

        Example(s):
            gh gitignore-template Python
            gh gitignore-template Python > .gitignore

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type language: str
        :param language: The language.
        """
        github.gitignore_template(language)

    @cli.command('gitignore-templates')
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def gitignore_templates(github, pager):
        """Output all supported gitignore templates.

        Usage:
            gh gitignore-templates

        Example(s):
            gh gitignore-templates
            gh gitignore-templates -p
            gh gitignore-templates --pager

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.gitignore_templates(pager)

    @cli.command()
    @click.argument('user_repo_number')
    @pass_github
    def issue(github, user_repo_number):
        """Output detailed information about the given issue.

        Usage:
            gh issue [user_repo_number]

        Example(s):
            gh issue donnemartin/saws/1

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type user_repo_number: str
        :param user_repo_number: The user/repo/issue_number.
        """
        github.issue(user_repo_number)

    @cli.command()
    @click.option('-f', '--issue_filter', required=False, default='subscribed')
    @click.option('-s', '--issue_state', required=False, default='open')
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def issues(github, issue_filter, issue_state, limit, pager):
        """List all issues matching the filter.

        Usage:
            gh issues [-f/--issue_filter] [-s/--issue_state] [-l/--limit] [-p/--pager]  # NOQA

        Example(s):
            gh issues
            gh issues -f assigned
            gh issues ---issue_filter created
            gh issues -s all -l 20 -p
            gh issues --issue_state closed --limit 20 --pager
            gh issues -f created -s all -p

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type issue_filter: str
        :param issue_filter: assigned, created, mentioned, subscribed (default).

        :type issue_state: str
        :param issue_state: all, open (default), closed.

        :type limit: int
        :param limit: The number of items to display.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.issues_setup(issue_filter, issue_state, limit, pager)

    @cli.command()
    @click.argument('license_name')
    @pass_github
    def license(github, license_name):
        """Output the license template for the given license.

        Usage:
            gh license [license_name]

        Example(s):
            gh license apache-2.0
            gh license mit > LICENSE

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type license_name: str
        :param license_name: The license name.
        """
        github.license(license_name)

    @cli.command()
    @pass_github
    def licenses(github):
        """Output all supported license templates.

        Usage/Example(s):
            gh licenses

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.
        """
        github.licenses()

    @cli.command()
    @click.option('-b', '--browser', is_flag=True)
    @click.option('-t', '--text_avatar', is_flag=True)
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def me(github, browser, text_avatar, limit, pager):
        """List information about the logged in user.

        Usage:
            gh me [-b/--browser] [-t/--text_avatar] [-l/--limit] [-p/--pager]

        Example(s):
            gh me
            gh me -b
            gh me --browser
            gh me -t -l 20 -p
            gh me --text_avatar --limit 20 --pager

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type browser: bool
        :param browser: Determines whether to view the profile
            in a browser, or in the terminal.

        :type text_avatar: bool
        :param text_avatar: Determines whether to view the profile
            avatar in plain text instead of ansi (default).
            On Windows this value is always set to True due to lack of
            support of `img2txt` on Windows.

        :type limit: int
        :param limit: The number of user repos to display.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.user_me(browser, text_avatar, limit, pager)

    @cli.command()
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def notifications(github, limit, pager):
        """List all notifications.

        Usage:
            gh notifications [-l/--limit] [-p/--pager]

        Example(s):
            gh notifications
            gh notifications -l 20 -p
            gh notifications --limit 20 --pager

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type limit: int
        :param limit: The number of items to display.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.notifications(limit, pager)

    @cli.command('octo')
    @click.argument('say', required=False)
    @pass_github
    def octocat(github, say):
        """Output an Easter egg or the given message from Octocat.

        Usage:
            gh octo [say]

        Example(s):
            gh octo
            gh octo "foo bar"

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type say: str
        :param say: What Octocat should say.
                If say is None, octocat speaks an Easter egg.
        """
        github.octocat(say)

    @cli.command('pull-request')
    @click.argument('user_repo_number')
    @pass_github
    def pull_request(github, user_repo_number):
        """Output detailed information about the given pull request.

        Usage:
            gh pull-request [user_repo_number]

        Example(s):
            gh pull-request donnemartin/saws/80

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type user_repo_number: str
        :param user_repo_number: The user/repo/pull_number.
        """
        github.issue(user_repo_number)

    @cli.command('pull-requests')
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def pull_requests(github, limit, pager):
        """List all pull requests.

        Usage:
            gh pull-requests [-l/--limit] [-p/--pager]

        Example(s):
            gh pull-requests
            gh pull-requests -l 20 -p
            gh pull-requests --limit 20 --pager

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type limit: int
        :param limit: The number of items to display.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.pull_requests(limit, pager)

    @cli.command('rate-limit')
    @pass_github
    def rate_limit(github):
        """Output the rate limit.  Not available for GitHub Enterprise.

        Logged in users can make 5000 requests per hour.
        See: https://developer.github.com/v3/#rate-limiting

        Usage/Example(s):
            gh rate-limit

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.
        """
        github.rate_limit()

    @cli.command('repos')
    @click.argument('repo_filter', required=False, default='')
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def repositories(github, repo_filter, limit, pager):
        """List all repos matching the given filter.

        Usage:
            gh repos [repo_filter] [-l/--limit] [-p/--pager]

        Example(s):
            gh repos
            gh repos "data-science"
            gh repos "data-science" -l 20 -p
            gh repos "data-science" --limit 20 --pager

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type repo_filter: str
        :param repo_filter:  The filter for repo names.
            Only repos matching the filter will be returned.
            If None, outputs all the logged in user's repos.

        :type limit: int
        :param limit: The number of items to display.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.repositories_setup(repo_filter, limit, pager)

    @cli.command('repo')
    @click.argument('user_repo')
    @pass_github
    def repository(github, user_repo):
        """Output detailed information about the given repo.

        Usage:
            gh repo [user_repo]

        Example(s):
            gh repo donnemartin/gitsome

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type user_repo: str
        :param user_repo: The user/repo.
        """
        github.repository(user_repo)

    @cli.command('search-issues')
    @click.argument('query')
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def search_issues(github, query, limit, pager):
        """Search for all issues matching the given query.

        Usage:
            gh search-issues [query] [-l/--limit] [-p/--pager]

        Example(s):
            gh search-issues "foo type:pr author:donnemartin" -l 20 -p
            gh search-issues "foobarbaz in:title created:>=2015-01-01" --limit 20 --pager  # NOQA

        Additional Example(s):
            Search issues that have your user name tagged @donnemartin:
                gh search-issues "is:issue donnemartin is:open" -p

            Search issues that have the most +1s:
                gh search-issues "is:open is:issue sort:reactions-+1-desc" -p

            Search issues that have the most comments:
                gh search-issues "is:open is:issue sort:comments-desc" -p

            Search issues with the "help wanted" tag:
                gh search-issues "is:open is:issue label:\"help wanted\"" -p

            Search all your open private issues:
                gh search-issues "is:open is:issue is:private" -p

        The query can contain any combination of the following supported
        qualifers:

        - `type` With this qualifier you can restrict the search to issues
          or pull request only.
        - `in` Qualifies which fields are searched. With this qualifier you
          can restrict the search to just the title, body, comments, or any
          combination of these.
        - `author` Finds issues created by a certain user.
        - `assignee` Finds issues that are assigned to a certain user.
        - `mentions` Finds issues that mention a certain user.
        - `commenter` Finds issues that a certain user commented on.
        - `involves` Finds issues that were either created by a certain user,
          assigned to that user, mention that user, or were commented on by
          that user.
        - `state` Filter issues based on whether they’re open or closed.
        - `labels` Filters issues based on their labels.
        - `language` Searches for issues within repositories that match a
          certain language.
        - `created` or `updated` Filters issues based on times of creation,
          or when they were last updated.
        - `comments` Filters issues based on the quantity of comments.
        - `user` or `repo` Limits searches to a specific user or
          repository.

        For more information about these qualifiers, see: http://git.io/d1oELA

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type query: str
        :param query: The search query.

        :type limit: int
        :param limit: The number of items to display.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.search_issues(query, limit, pager)

    @cli.command('search-repos')
    @click.argument('query')
    @click.option('-s', '--sort', required=False, default='')
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def search_repositories(github, query, sort, limit, pager):
        """Search for all repos matching the given query.

        Usage:
            gh search-repos [query] [-s/--sort] [-l/--limit] [-p/--pager]

        Example(s):
            gh search-repos "maps language:python" -s stars -l 20 -p
            gh search-repos "created:>=2015-01-01 stars:>=1000 language:python" --sort stars --limit 20 --pager  # NOQA

        The query can contain any combination of the following supported
        qualifers:

        - `in` Qualifies which fields are searched. With this qualifier you
          can restrict the search to just the repository name, description,
          readme, or any combination of these.
        - `size` Finds repositories that match a certain size (in
          kilobytes).
        - `forks` Filters repositories based on the number of forks, and/or
          whether forked repositories should be included in the results at
          all.
        - `created` or `pushed` Filters repositories based on times of
          creation, or when they were last updated. Format: `YYYY-MM-DD`.
          Examples: `created:<2011`, `pushed:<2013-02`,
          `pushed:>=2013-03-06`
        - `user` or `repo` Limits searches to a specific user or
          repository.
        - `language` Searches repositories based on the language they're
          written in.
        - `stars` Searches repositories based on the number of stars.

        For more information about these qualifiers, see: http://git.io/4Z8AkA

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type query: str
        :param query: The search query.

        :type sort: str
        :param sort: Optional: 'stars', 'forks', 'updated'.
            If not specified, sorting is done by query best match.

        :type limit: int
        :param limit: The number of items to display.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.search_repositories(query, sort, limit, pager)

    @cli.command()
    @click.argument('repo_filter', required=False, default='')
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def starred(github, repo_filter, limit, pager):
        """Output starred repos.

        Usage:
            gh starred [repo_filter] [-l/--limit] [-p/--pager]

        Example(s):
            gh starred
            gh starred foo -l 20 -p
            gh starred foo --limit 20 --pager

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type repo_filter: str
        :param repo_filter:  The filter for repo names.
            Only repos matching the filter will be returned.
            If None, outputs all starred repos.

        :type limit: int
        :param limit: The number of items to display.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.starred(repo_filter, limit, pager)

    @cli.command()
    @click.argument('language', required=False, default='Overall')
    @click.option('-w', '--weekly', is_flag=True)
    @click.option('-m', '--monthly', is_flag=True)
    @click.option('-D', '--devs', is_flag=True)
    @click.option('-b', '--browser', is_flag=True)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def trending(github, language, weekly, monthly, devs, browser, pager):
        """List trending repos for the given language.

        Usage:
            gh trending [language] [-w/--weekly] [-m/--monthly] [-D/--devs] [-b/--browser] [-p/--pager]  # NOQA

        Example(s):
            gh trending
            gh trending Python -w -p
            gh trending Python --weekly --devs --browser
            gh trending --browser

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type language: str
        :param language: The language (optional).
            If blank, shows 'Overall'.

        :type weekly: bool
        :param weekly: Determines whether to show the weekly rankings.
            Daily is the default.

        :type monthly: bool
        :param monthly: Determines whether to show the monthly rankings.
            Daily is the default.
            If both `monthly` and `weekly` are set, `monthly` takes precedence.

        :type devs: bool
        :param devs: determines whether to display the trending
                devs or repos.  Only valid with the -b/--browser option.

        :type browser: bool
        :param browser: Determines whether to view the profile
                in a browser, or in the terminal.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.trending(language, weekly, monthly, devs, browser, pager)

    @cli.command()
    @click.argument('user_id', required=True)
    @click.option('-b', '--browser', is_flag=True)
    @click.option('-t', '--text_avatar', is_flag=True)
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def user(github, user_id, browser, text_avatar, limit, pager):
        """List information about the given user.

        Usage:
            gh user [user_id] [-b/--browser] [-t/--text_avatar] [-l/--limit] [-p/--pager]  # NOQA

        Example(s):
            gh user octocat
            gh user octocat -b
            gh user octocat --browser
            gh user octocat -t -l 10 -p
            gh user octocat --text_avatar --limit 10 --pager

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type user_id: str
        :param user_id: The user id/login.
            If None, returns followers of the logged in user.

        :type browser: bool
        :param browser: Determines whether to view the profile
            in a browser, or in the terminal.

        :type text_avatar: bool
        :param text_avatar: Determines whether to view the profile
            avatar in plain text instead of ansi (default).
            On Windows this value is always set to True due to lack of
            support of `img2txt` on Windows.

        :type limit: int
        :param limit: The number of items to display.

        :type pager: bool
        :param pager: Determines whether to show the output in a pager,
            if available.
        """
        github.user(user_id, browser, text_avatar, limit, pager)

    @cli.command()
    @click.argument('index')
    @click.option('-b', '--browser', is_flag=True)
    @pass_github
    def view(github, index, browser):
        """View the given notification/repo/issue/pull_request/user index.

        This method is meant to be called after one of the following commands
        which outputs a table of notifications/repos/issues/pull_requests/users:

            gh repos
            gh search_repos
            gh starred

            gh issues
            gh pull_requests
            gh search_issues

            gh notifications
            gh trending

            gh user
            gh me

        Usage:
            gh view [index] [-b/--browser]

        Example(s):
            gh repos
            gh view 1

            gh starred
            gh view 1 -b
            gh view 1 --browser

        :type github: :class:`github.GitHub`
        :param github: An instance of `github.GitHub`.

        :type index: str
        :param index: Determines the index to view.

        :type browser: bool
        :param browser: Determines whether to view the profile
            in a browser, or in the terminal.
        """
        github.view(int(index), browser)
