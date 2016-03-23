# coding: utf-8
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
    @click.argument('index')
    @click.option('-b', '--browser', is_flag=True)
    @pass_github
    def view(github, index, browser):
        """Views the given index in a browser.

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
            * index: An int that specifies the index to open in a browser.
                For example, calling gh repositories will list repos with a
                0-based index for each repo.  Calling gh view [index] will
                open the url for the associated repo in a browser.
            * browser: A boolean that determines whether to view in a
                web browser or a terminal.

        Returns:
            None.
        """
        github.view(int(index), browser)

    @cli.command()
    @click.argument('user_login')
    @click.argument('repo_name')
    @click.argument('issue_title')
    @click.argument('issue_body', required=False)
    @pass_github
    def create_issue(github, user_login, repo_name, issue_title, issue_body):
        """Creates an issue.

        Example(s):
            gh donnemartin gitsome "issue title"
            gh donnemartin gitsome "issue title" "issue body"

        Args:
            * user_login: A string representing the user login.
            * repo_name: A string representing the repo name.
            * issue_title: A string representing the issue title.
            * issue_body: A string representing the issue body (optional).

        Returns:
            None.
        """
        issue = github.api.create_issue(user_login,
                                        repo_name,
                                        issue_title,
                                        issue_body)
        click.echo('Created issue: ' + issue.title)
        github.issue(user_login, repo_name, issue.number)

    @cli.command()
    @click.argument('repo_name')
    @click.argument('repo_desc', required=False)
    @click.option('-p', '--private', is_flag=True)
    @pass_github
    def create_repo(github, repo_name, repo_desc, private):
        """Creates a repo.

        Example(s):
            gh create_repo "repo name"
            gh create_repo "repo name" "repo description"
            gh create_repo "repo name" "repo description" -p
            gh create_repo "repo name" "repo description" --private

        Args:
            * repo_name: A string representing the repo name.
            * repo_desc: A string representing the repo description (optional).
            * private: A boolean that determines whether the repo is private.
                Default: False.

        Returns:
            None.
        """
        repo = github.api.create_repository(repo_name,
                                            repo_desc,
                                            private=private)
        click.secho('Created repo: ' + repo.full_name, fg='blue')

    @cli.command()
    @pass_github
    def emails(github):
        """Lists all the user's registered emails.

        Example(s):
            gh emails

        Args:
            * None.

        Returns:
            None.
        """
        github.print_items(github.api.emails(), headers='keys')

    @cli.command()
    @pass_github
    def events(github):
        """Lists all public events.

        Examples:
            gh events | grep foo
            gh events | less

        Args:
            * None.

        Returns:
            None.
        """
        events = github.api.all_events()
        table = []
        for event in events:
            table.append([event.created_at,
                          event.actor,
                          event.type,
                          github.format_repo(event.repo)])
        github.print_table(table,
                           headers=['created at', 'user', 'type', 'repo'])

    @cli.command()
    @pass_github
    def emojis(github):
        """Lists all GitHub supported emojis.

        Example(s):
            gh emojis | grep octo

        Args:
            * None.

        Returns:
            None.
        """
        github.print_items(github.listify(github.api.emojis()),
                                          headers=['emoji'])

    @cli.command()
    @pass_github
    def feeds(github):
        """Lists GitHub's timeline resources.

        Requires authentication with user/pass, cannot be used with tokens
        due to a limitation with the GitHub API itself.

        TODO: Results in an exception with github3.py.

        Example(s):
            gh feeds

        Args:
            * None.

        Returns:
            None.

        Raises:
            TypeError: Seems to be a github3.py bug.
        """
        click.secho('This command is temporarily unavailable.', fg='red')
        # github.api.feeds()

    @cli.command()
    @click.argument('user_login', required=False)
    @pass_github
    def followers(github, user_login):
        """Lists all followers and the total follower count.

        Example(s):
            gh followers
            gh followers donnemartin

        Args:
            * user_login: A string representing the user login.
                If None, returns followers of the logged in user.

        Returns:
            None.
        """
        if user_login is None:
            user_login = github.user_login
        users = github.api.followers_of(user_login)
        table = []
        for user in users:
            table.append([user.login, user.html_url])
        github.print_table(table, headers=['user', 'profile'])
        click.secho(
            'Followers: ' + str(github.api.user(user_login).followers_count),
            fg='blue')

    @cli.command()
    @click.argument('user_login', required=False)
    @pass_github
    def following(github, user_login):
        """Lists all followed users and the total followed count.

        Example(s):
            gh following
            gh following donnemartin

        Args:
            * user_login: A string representing the user login.
                If None, returns the followed users of the logged in user.

        Returns:
            None.
        """
        if user_login is None:
            user_login = github.user_login
        users = github.api.followed_by(user_login)
        table = []
        for user in users:
            table.append([user.login, user.html_url])
        github.print_table(table, headers=['user', 'profile'])
        click.secho(
            'Following ' + str(github.api.user(user_login).following_count),
            fg='blue')

    @cli.command()
    @click.argument('language')
    @pass_github
    def gitignore_template(github, language):
        """Outputs the gitignore template for the given language.

        Example(s):
            gh gitignore_template Python
            gh gitignore_template Python > .gitignore

        Args:
            * language: A string representing the language.

        Returns:
            None.
        """
        template = github.api.gitignore_template(language)
        if template:
            click.echo(template)
        else:
            click.secho('Invalid template requested, run the following ' \
                       'command to see available templates:\n' \
                       '    gh gitignore_templates',
                       fg='red')

    @cli.command()
    @pass_github
    def gitignore_templates(github):
        """Outputs all supported gitignore templates.

        Example(s):
            gh gitignore_templates

        Args:
            * None.

        Returns:
            None.
        """
        github.print_items(
            github.listify(github.api.gitignore_templates()),
                           headers=['language'])

    @cli.command()
    @click.argument('user_login')
    @click.argument('repo_name')
    @click.argument('issue_number')
    @pass_github
    def issue(github, user_login, repo_name, issue_number):
        """Outputs detailed information about the given issue.

        Example(s):
            gh donnemartin saws 1

        Args:
            * user_login: A string representing the user login.
            * repo_name: A string representing the repo name.
            * issue_number: An int representing the issue number.

        Returns:
            None.
        """
        github.issue(user_login, repo_name, issue_number)

    @cli.command()
    @click.argument('issue_filter', required=False, default='subscribed')
    @click.argument('state', required=False, default='open')
    @pass_github
    def issues(github, issue_filter, state):
        """Lists all issues.

        Example(s):
            gh issues
            gh issues assigned
            gh issues created all | grep foo

        Args:
            * issue_filter: A string with the following accepted values:
                'assigned', 'created', 'mentioned', 'subscribed' (default).
            * state: A string with the following accepted values:
                'all', 'open' (default), 'closed'.

        Returns:
            None.
        """
        github.issues(issue_filter, state)

    @cli.command()
    @click.option('-b', '--browser', is_flag=True)
    @click.option('-a', '--ansi', is_flag=True)
    @pass_github
    def me(github, browser, ansi):
        """Lists information about the logged in user.

        Example(s):
            gh me
            gh me -b
            gh me --browser
            gh me -a
            gh me --ansi

        Args:
            * browser: A Boolean that determines whether to view the profile
                in a browser, or in the terminal.
            * ansi: A boolean that determines whether to view the profile
                avatar in a ansi, or plain text.

        Returns:
            None.
        """
        if browser:
            url = 'https://github.com/' + github.user_login
            webbrowser.open(url)
        else:
            user = github.api.me()
            github.avatar(user.avatar_url, ansi)
            click.echo('')
            click.secho(user.login, fg='blue')
            if user.company is not None:
                click.secho('company:', user.company, fg='blue')
            if user.location is not None:
                click.secho('location:', user.location, fg='blue')
            if user.email is not None:
                click.secho('email: ' + user.email, fg='blue')
            click.secho('followers: ' + str(user.followers_count), fg='blue')
            click.secho('following: ' + str(user.following_count), fg='blue')
            click.echo('')
            github.repositories(github.api.repositories())

    @cli.command()
    @pass_github
    def notifications(github):
        """Lists all notifications.

        TODO: Always results in an empty list.  Possible github3.py bug.

        Example(s):
            gh notifications

        Args:
            * None.

        Returns:
            None.
        """
        click.secho('This command is temporarily unavailable.', fg='red')
        # github.print_items(github.api.notifications(participating=True),
        #                    headers=['notification'])

    @cli.command()
    @click.argument('say', required=False)
    @pass_github
    def octocat(github, say):
        """Outputs an Easter egg or the given message from Octocat.

        Example(s):
            gh octocat
            gh octocat "foo bar"

        Args:
            * say: A string for octocat to say.
                If say is None, octocat speaks an Easter egg.

        Returns:
            None.
        """
        output = str(github.api.octocat(say))
        output = output.replace('\\n', '\n')
        click.echo(output)

    @cli.command()
    @click.argument('user_login')
    @click.argument('repo_name')
    @click.argument('issue_number')
    @pass_github
    def pull_request(github, user_login, repo_name, issue_number):
        """Outputs detailed information about the given pull request.

        Example(s):
            gh pull_request donnemartin awesome-aws 2

        Args:
            * user_login: A string representing the user login.
            * repo_name: A string representing the repo name.
            * issue_number: An int representing the issue number.

        Returns:
            None.
        """
        github.issue(user_login, repo_name, issue_number)

    @cli.command()
    @pass_github
    def pull_requests(github):
        """Lists all pull requests.

        Example(s):
            gh pull_requests

        Args:
            * None.

        Returns:
            None.
        """
        pull_requests = []
        repositories = github.api.repositories()
        for repository in repositories:
            repo_pulls = repository.pull_requests()
            for repo_pull in repo_pulls:
                pull_requests.append(repo_pull)
        table = []
        for pull_request in pull_requests:
            user_login, repo_name = pull_request.repository
            repo = user_login.strip('repos/') + '/' + repo_name
            table.append([pull_request.number,
                          repo,
                          pull_request.title])
        # Sort by repo, pull request number
        table = sorted(table, key=itemgetter(1, 0))
        github.print_table(table, headers=['#', 'repo', 'title'])

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
