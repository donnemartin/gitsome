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

from operator import itemgetter
import urllib
import webbrowser

import click

from .github import GitHub


pass_github = click.make_pass_decorator(GitHub)


class GitHubCli(object):
    """Encapsulates the GitHubCli.

    Attributes:
        * None.
    """

    @click.group()
    @click.pass_context
    def cli(ctx):
        """Main entry point for GitHubCli.

        Args:
            * ctx: An instance of click.core.Context that stores an instance
                 of GitHub used to interact with the GitHub API.

        Returns:
            None.
        """
        # Create a GitHub object and remember it as as the context object.
        # From this point onwards other commands can refer to it by using the
        # @pass_github decorator.
        ctx.obj = GitHub()

    @cli.command()
    @pass_github
    def configure(github):
        """Configures gitsome.

        Example(s):
            gh configure

        Args:
            * github: An instance of github.GitHub.

        Returns:
            None.
        """
        github.configure()

    @cli.command('create-comment')
    @click.argument('user_repo_number')
    @click.option('-t', '--text')
    @pass_github
    def create_comment(github, user_repo_number, text):
        """Creates a comment on the given issue.

        Example(s):
            gh create_comment donnemartin/saws/1 --text "hello world"

        Args:
            * github: An instance of github.GitHub.
            * user_repo_number: A string representing the
                user/repo/issue number.
            * text: A string representing the comment text.

        Returns:
            None.
        """
        github.create_comment(user_repo_number, text)

    @cli.command('create-issue')
    @click.argument('user_repo')
    @click.option('-t', '--issue_title')
    @click.option('-d', '--issue_desc', required=False)
    @pass_github
    def create_issue(github, user_repo, issue_title, issue_desc):
        """Creates an issue.

        Example(s):
            gh donnemartin gitsome -t "issue title"
            gh donnemartin gitsome -t "issue title" -b "issue body"

        Args:
            * github: An instance of github.GitHub.
            * user_repo: A string representing the user/repo.
            * issue_title: A string representing the issue title.
            * issue_desc: A string representing the issue body (optional).

        Returns:
            None.
        """
        github.create_issue(user_repo, issue_title, issue_desc)

    @cli.command('create-repo')
    @click.argument('repo_name')
    @click.option('-d', '--repo_desc', required=False)
    @click.option('-pr', '--private', is_flag=True)
    @pass_github
    def create_repo(github, repo_name, repo_desc, private):
        """Creates a repo.

        Example(s):
            gh create_repo "repo name"
            gh create_repo "repo name" --repo_desc "desc"
            gh create_repo "repo name" -pr
            gh create_repo "repo name" --private

        Args:
            * github: An instance of github.GitHub.
            * repo_name: A string representing the repo name.
            * repo_desc: A string representing the repo description (optional).
            * private: A boolean that determines whether the repo is private.
                Default: False.

        Returns:
            None.
        """
        github.create_repo(repo_name, repo_desc, private)

    @pass_github
    def emails(github):
        """Lists all the user's registered emails.

        Example(s):
            gh emails

        Args:
            * github: An instance of github.GitHub.

        Returns:
            None.
        """
        github.emails()

    @cli.command()
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def emojis(github, pager):
        """Lists all GitHub supported emojis.

        Example(s):
            gh emojis | grep octo

        Args:
            * github: An instance of github.GitHub.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        github.emojis(pager)

    @cli.command()
    @click.argument('user_or_repo', required=False, default='')
    @click.option('-pr', '--private', is_flag=True, default=False)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def feed(github, user_or_repo, private, pager):
        """Lists all activity for the given user or repo.

        If blank, lists the logged in user's news feed.

        Examples:
            gh feed | grep foo
            gh feed | less -r
            gh feed donnemartin --private
            gh feed donnemartin/haxor-news

        Args:
            * github: An instance of github.GitHub.
            * user_or_repo: A string representing the user or repo to list
                events for.  If no entry, defaults to the logged in user's feed.
            * private: A boolean that determines whether to show the private
                events (True) or public events (False).
                Only works for the currently logged in user.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        github.feed(user_or_repo, private, pager)

    @cli.command()
    @click.argument('user', required=False)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def followers(github, user, pager):
        """Lists all followers and the total follower count.

        Example(s):
            gh followers
            gh followers donnemartin

        Args:
            * github: An instance of github.GitHub.
            * user: A string representing the user login.
                If None, returns followers of the logged in user.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        github.followers(user, pager)

    @cli.command()
    @click.argument('user', required=False)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def following(github, user, pager):
        """Lists all followed users and the total followed count.

        Example(s):
            gh following
            gh following donnemartin

        Args:
            * github: An instance of github.GitHub.
            * user: A string representing the user login.
                If None, returns the followed users of the logged in user.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        github.following(user, pager)

    @cli.command('gitignore-template')
    @click.argument('language')
    @pass_github
    def gitignore_template(github, language):
        """Outputs the gitignore template for the given language.

        Example(s):
            gh gitignore Python
            gh gitignore Python > .gitignore

        Args:
            * github: An instance of github.GitHub.
            * language: A string representing the language.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        github.gitignore_template(language)

    @cli.command('gitignore-templates')
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def gitignore_templates(github, pager):
        """Outputs all supported gitignore templates.

        Example(s):
            gh gitignores

        Args:
            * github: An instance of github.GitHub.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        github.gitignore_templates(pager)

    @cli.command()
    @click.argument('user_repo_number')
    @pass_github
    def issue(github, user_repo_number):
        """Outputs detailed information about the given issue.

        Example(s):
            gh issue donnemartin/saws/1

        Args:
            * github: An instance of github.GitHub.
            * user_repo_number: A string representing the
                user/repo/issue number.

        Returns:
            None.
        """
        github.issue(user_repo_number)

    @cli.command()
    @click.option('-f', '--issue_filter', required=False, default='subscribed')
    @click.option('-s', '--issue_state', required=False, default='open')
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def issues(github, issue_filter, issue_state, limit, pager):
        """Lists all issues matching the filter.

        Example(s):
            gh issues
            gh issues --issue_state closed --limit 20
            gh issues "foo bar" assigned
            gh issues created | grep foo

        Args:
            * github: An instance of github.GitHub.
            * issue_filter: A string with the following accepted values:
                'assigned', 'created', 'mentioned', 'subscribed' (default).
            * issue_state: A string with the following accepted values:
                'all', 'open' (default), 'closed'.
            * limit: An int that specifies the number of items to show.
                Optional, defaults to 1000.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        github.issues_setup(issue_filter, issue_state, limit, pager)

    @cli.command()
    @click.argument('license_name')
    @pass_github
    def license(github, license_name):
        """Outputs the license template for the given license.

        Example(s):
            gh license "MIT"
            gh license "MIT" > LICENSE

        Args:
            * github: An instance of github.GitHub.
            * license_name: A string representing the license name.

        Returns:
            None.
        """
        github.license(license_name)

    @cli.command()
    @pass_github
    def licenses(github):
        """Outputs all supported license templates.

        Example(s):
            gh licenses

        Args:
            * github: An instance of github.GitHub.

        Returns:
            None.
        """
        github.licenses()

    @cli.command()
    @click.option('-b', '--browser', is_flag=True)
    @click.option('-t', '--text_avatar', is_flag=True)
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def me(github, browser, text_avatar, limit, pager):
        """Lists information about the logged in user.

        Example(s):
            gh me
            gh me 20
            gh me -b
            gh me --browser
            gh me -a
            gh me --text_avatar
            gh me --limit 20

        Args:
            * github: An instance of github.GitHub.
            * limit: An int that specifies the number of items to show.
                Optional, defaults to 1000.
            * browser: A Boolean that determines whether to view the profile
                in a browser, or in the terminal.
            * text_avatar: A boolean that determines whether to view the profile
                avatar in plain text.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        github.user_me(browser, text_avatar, limit, pager)

    @cli.command()
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def notifications(github, limit, pager):
        """Lists all notifications.

        Example(s):
            gh notifications

        Args:
            * github: An instance of github.GitHub.
            * limit: An int that specifies the number of items to show.
                Optional, defaults to 1000.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        github.notifications(limit, pager)

    @cli.command('octo')
    @click.argument('say', required=False)
    @pass_github
    def octocat(github, say):
        """Outputs an Easter egg or the given message from Octocat.

        Example(s):
            gh octocat
            gh octocat "foo bar"

        Args:
            * github: An instance of github.GitHub.
            * say: A string for octocat to say.
                If say is None, octocat speaks an Easter egg.

        Returns:
            None.
        """
        github.octocat(say)

    @cli.command('pull-request')
    @click.argument('user_repo_number')
    @pass_github
    def pull_request(github, user_repo_number):
        """Outputs detailed information about the given pull request.

        Example(s):
            gh pr donnemartin/awesome-aws/2

        Args:
            * github: An instance of github.GitHub.
            * user_repo_number: A string representing the user/repo/number.

        Returns:
            None.
        """
        github.issue(user_repo_number)

    @cli.command('pull-requests')
    @click.option('-l', '--limit', required=False, default=1000)
    @click.option('-p', '--pager', is_flag=True)
    @pass_github
    def pull_requests(github, limit, pager):
        """Lists all pull requests.

        Example(s):
            gh prs
            gh prs --limit 20

        Args:
            * github: An instance of github.GitHub.
            * limit: An int that specifies the number of items to show.
                Optional, defaults to 1000.
            * pager: A boolean that determines whether to show the results
                in a pager, where available.

        Returns:
            None.
        """
        github.pull_requests(limit, pager)

    @cli.command()
    @pass_github
    def rate_limit(github):
        """Outputs the rate limit.

        Example(s):
            gh rate_limit

        Args:
            * None.

        Returns:
            None.
        """
        click.echo('Rate limit: ' + str(github.api.ratelimit_remaining))

    @cli.command('repo')
    @click.argument('user_login')
    @click.argument('repo_name')
    @pass_github
    def repository(github, user_login, repo_name):
        """Outputs detailed information about the given repo.

        Example(s):
            gh repo donnemartin gitsome

        Args:
            * user_login: A string representing the user login.
            * repo_name: A string representing the repo name.

        Returns:
            None.
        """
        github.repository(user_login, repo_name)

    @cli.command('repos')
    @pass_github
    def repositories(github):
        """Lists all repos.

        Example(s):
            gh repos

        Args:
            * None.

        Returns:
            None.
        """
        github.repositories(github.api.repositories())

    @cli.command()
    @click.argument('query')
    @pass_github
    def search_issues(github, query):
        """Searches all issues with the given query.

        The query can contain any combination of the following supported
        qualifers:

        - ``type`` With this qualifier you can restrict the search to issues
          or pull request only.
        - ``in`` Qualifies which fields are searched. With this qualifier you
          can restrict the search to just the title, body, comments, or any
          combination of these.
        - ``author`` Finds issues created by a certain user.
        - ``assignee`` Finds issues that are assigned to a certain user.
        - ``mentions`` Finds issues that mention a certain user.
        - ``commenter`` Finds issues that a certain user commented on.
        - ``involves`` Finds issues that were either created by a certain user,
          assigned to that user, mention that user, or were commented on by
          that user.
        - ``state`` Filter issues based on whether they’re open or closed.
        - ``labels`` Filters issues based on their labels.
        - ``language`` Searches for issues within repositories that match a
          certain language.
        - ``created`` or ``updated`` Filters issues based on times of creation,
          or when they were last updated.
        - ``comments`` Filters issues based on the quantity of comments.
        - ``user`` or ``repo`` Limits searches to a specific user or
          repository.

        For more information about these qualifiers, see: http://git.io/d1oELA

        Example(s):
            gh search_issues "foo type:pr author:donnemartin"
            gh search_issues "foo in:title created:>=2015-01-01" | less

        Args:
            * query: A string representing the search query.

        Returns:
            None.
        """
        click.secho('Searching issues on GitHub...', fg='blue')
        issues = github.api.search_issues(query)
        table = []
        try:
            for issue in issues:
                table.append([issue.score,
                             issue.issue.number,
                             github.format_repo(issue.issue.repository),
                             issue.issue.title])
        except AttributeError:
            # github3.py sometimes throws the following during iteration:
            # AttributeError: 'NoneType' object has no attribute 'get'
            pass
        # Sort by score, repo, issue number
        table = sorted(table, key=itemgetter(0, 2, 1), reverse=True)
        github.print_table(table, headers=['score', '#', 'repo', 'title'])

    @cli.command('search_repos')
    @click.argument('query')
    @click.argument('sort', required=False, default=None)
    @pass_github
    def search_repositories(github, query, sort):
        """Searches all repos with the given query.

        The query can contain any combination of the following supported
        qualifers:

        - ``in`` Qualifies which fields are searched. With this qualifier you
          can restrict the search to just the repository name, description,
          readme, or any combination of these.
        - ``size`` Finds repositories that match a certain size (in
          kilobytes).
        - ``forks`` Filters repositories based on the number of forks, and/or
          whether forked repositories should be included in the results at
          all.
        - ``created`` or ``pushed`` Filters repositories based on times of
          creation, or when they were last updated. Format: ``YYYY-MM-DD``.
          Examples: ``created:<2011``, ``pushed:<2013-02``,
          ``pushed:>=2013-03-06``
        - ``user`` or ``repo`` Limits searches to a specific user or
          repository.
        - ``language`` Searches repositories based on the language they're
          written in.
        - ``stars`` Searches repositories based on the number of stars.

        For more information about these qualifiers, see: http://git.io/4Z8AkA

        Example(s):
            gh search_repos "maps language:python" stars | less
            gh search_repos "created:>=2015-01-01 stars:>=1000 language:python"

        Args:
            * query: A string representing the search query.
            * sort: A string that determines sorting (optional).
                'stars', 'forks', 'updated'.
                If not specified, sorting is done by query best match.

        Returns:
            None.
        """
        click.secho('Searching repos on GitHub...', fg='blue')
        repos = github.api.search_repositories(query, sort)
        table = []
        number = 0
        try:
            for repo in repos:
                table.append([number,
                              repo.score,
                              repo.repository.full_name,
                              repo.repository.stargazers_count,
                              repo.repository.forks_count])
                number += 1
        except AttributeError:
            # github3.py sometimes throws the following during iteration:
            # AttributeError: 'NoneType' object has no attribute 'get'
            pass
        # Sort by score, repo
        table = sorted(table, key=itemgetter(1, 2), reverse=True)
        github.build_repo_urls(table, url_index=0, repo_index=2)
        github.print_table(table, headers=['#', 'score', 'repo',
                                           'stars', 'forks'])

    @cli.command()
    @click.argument('repo_filter', required=False, default='')
    @pass_github
    def starred(github, repo_filter):
        """Outputs starred repos.

        Example(s):
            gh starred foo

        Args:
            * repo_filter: A string representing a filter for repo names.
                Only repos matching the filter will be returned.
                If None, outputs all starred repos.

        Returns:
            None.
        """
        github.repositories(github.api.starred(), repo_filter.lower())

    @cli.command()
    @click.argument('index')
    @click.option('-b', '--browser', is_flag=True)
    @pass_github
    def view(github, index, browser):
        """Views the given repo or issue index in the terminal or a browser.

        This method is meant to be called after one of the following commands
        which outputs a table of repos or issues:

            gh repos
            gh search_repos
            gh starred

            gh issues
            gh pull_requests
            gh search_issues

        Example(s):
            gh view repos
            gh view 0

            gh view starred
            gh view 0 -b
            gh view 0 --browser

        Args:
            * github: An instance of github.GitHub.
            * index: An int that specifies the index to view.
                For example, calling gh repos will list repos with a
                1-based index for each repo.  Calling gh view [index] will
                view the contents of the url for the associated repo.
            * browser: A boolean that determines whether to view in a
                web browser or a terminal.

        Returns:
            None.
        """
        github.view(int(index), browser)
