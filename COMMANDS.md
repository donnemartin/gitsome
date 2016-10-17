# Commands

## GitHub Integration Commands Reference

Check out the handy [autocompleter with interactive help](https://github.com/donnemartin/gitsome/blob/master/README.md#git-and-github-autocompleter-with-interactive-help) to guide you through each command.

### gh configure

Configure `gitsome`.

Attempts to authenticate the user and to set up the user's news feed.

If `gitsome` has not yet been configured, calling a `gh` command that requires authentication will automatically invoke the `configure` command.

Usage/Example(s):

    $ gh configure

For GitHub Enterprise users, run with the `-e/--enterprise` flag:

    $ gh configure -e

#### Authentication

To properly integrate with GitHub, you will be asked to enter a user name and either a password or a [personal access token](https://github.com/settings/tokens).  If you use two-factor authentication, you will also need to enter your 2FA code, or you can log in with a personal access token.

Visit the following page to generate a token:

[https://github.com/settings/tokens](https://github.com/settings/tokens)

`gitsome` will need the 'repo' and 'user' permissions.

![Imgur](http://i.imgur.com/1C7gBHz.png)

#### GitHub Enterprise

GitHub Enterprise users will be asked to enter the GitHub Enterprise url and whether they want to verify SSL certificates.

#### Authentication Source Code

Curious what's going on behind the scenes with authentication?  Check out the [authentication source code](https://github.com/donnemartin/gitsome/blob/master/gitsome/config.py#L177-L328).

#### User Feed

`gitsome` will need your news feed url to run the `gh feed` command with no arguments.

![Imgur](http://i.imgur.com/2LWcyS6.png)

To integrate `gitsome` with your news feed, visit the following url while logged into GitHub:

[https://github.com](https://github.com)

You will be asked to enter the url found when clicking 'Subscribe to your news feed', which will look something like this:

    https://github.com/donnemartin.private.atom?token=TOKEN

![Imgur](http://i.imgur.com/f2zvdIm.png)

### gh create-comment

Create a comment on the given issue.

Usage:

    $ gh create-comment [user_repo_number] [-t/--text]

Param(s):

```
:type user_repo_number: str
:param user_repo_number: The user/repo/issue_number.
```

Option(s):

```
:type text: str
:param text: The comment text.
```

Example(s):

    $ gh create-comment donnemartin/saws/1 -t "hello world"
    $ gh create-comment donnemartin/saws/1 --text "hello world"

### gh create-issue

Create an issue.

Usage:

    $ gh create-issue [user_repo] [-t/--issue_title] [-d/--issue_desc]

Param(s):

```
:type user_repo: str
:param user_repo: The user/repo.
```

Option(s):

```
:type issue_title: str
:param issue_title: The issue title.

:type issue_desc: str
:param issue_desc: The issue body (optional).
```

Example(s):

    $ gh create-issue donnemartin/gitsome -t "title"
    $ gh create-issue donnemartin/gitsome -t "title" -d "desc"
    $ gh create-issue donnemartin/gitsome --issue_title "title" --issue_desc "desc"

### gh create-repo

Create a repo.

Usage:

    $ gh create-repo [repo_name] [-d/--repo_desc] [-pr/--private]

Param(s):

```
:type repo_name: str
:param repo_name: The repo name.
```

Option(s):

```
:type repo_desc: str
:param repo_desc: The repo description (optional).

:type private: bool
:param private: Determines whether the repo is private.
    Default: False.
```

Example(s):

    $ gh create-repo repo_name
    $ gh create-repo repo_name -d "desc"
    $ gh create-repo repo_name --repo_desc "desc"
    $ gh create-repo repo_name -pr
    $ gh create-repo repo_name --repo_desc "desc" --private

### gh emails

List all the user's registered emails.

Usage/Example(s):

    $ gh emails

### gh emojis

List all GitHub supported emojis.

Usage:

    $ gh emojis [-p/--pager]

Option(s):

```
:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh emojis
    $ gh emojis -p
    $ gh emojis --pager

### gh feed

List all activity for the given user or repo.

If `user_or_repo` is not provided, uses the logged in user's news feed seen while visiting https://github.com.  If `user_or_repo` is provided, shows either the public or `[-pr/--private]` feed activity of the user or repo.

Usage:

    $ gh feed [user_or_repo] [-pr/--private] [-p/--pager]

Param(s):

```
:type user_or_repo: str
:param user_or_repo: The user or repo to list events for (optional).
    If no entry, defaults to the logged in user's feed.
```

Option(s):

```
:type private: bool
:param private: Determines whether to show the private events (True)
    or public events (False).

:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh feed
    $ gh feed | grep foo
    $ gh feed donnemartin
    $ gh feed donnemartin -pr -p
    $ gh feed donnemartin --private --pager
    $ gh feed donnemartin/haxor-news -p

#### News Feed

![Imgur](http://i.imgur.com/2LWcyS6.png)

#### User Activity Feed

![Imgur](http://i.imgur.com/kryGLXz.png)

#### Repo Activity Feed

![Imgur](http://i.imgur.com/d2kxDg9.png)

### gh following

List all followed users and the total followed count.

Usage:

    $ gh following [user] [-p/--pager]

Param(s):

```
:type user: str
:param user: The user login.
    If None, returns the followed users of the logged in user.
```

Option(s):

```
:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh following
    $ gh following -p
    $ gh following octocat --pager

![Imgur](http://i.imgur.com/bjUmbf3.png)

Also check out the [`gh user`](#gh-user) command.

### gh followers

List all followers and the total follower count.

Usage:

    $ gh followers [user] [-p/--pager]

Param(s):

```
:type user: str
:param user: The user login (optional).
    If None, returns the followers of the logged in user.
```

Option(s):

```
:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh followers
    $ gh followers -p
    $ gh followers octocat --pager

### gh gitignore-template

Output the gitignore template for the given language.

Usage:

    $ gh gitignore-template [language]

Param(s):

```
:type language: str
:param language: The language.
```

Example(s):

    $ gh gitignore-template Python
    $ gh gitignore-template Python > .gitignore

![Imgur](http://i.imgur.com/S5m5ZcO.png)

### gh gitignore-templates

Output all supported gitignore templates.

Usage:

    $ gh gitignore-templates [-p/--pager]

Option(s):

```
:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh gitignore-templates
    $ gh gitignore-templates -p
    $ gh gitignore-templates --pager

![Imgur](http://i.imgur.com/u8qYx1s.png)

### gh issue

Output detailed information about the given issue.

Usage:

    $ gh issue [user_repo_number]

Param(s):

```
:type user_repo_number: str
:param user_repo_number: The user/repo/issue_number.
```

Example(s):

    $ gh issue donnemartin/saws/1

![Imgur](http://i.imgur.com/ZFv9MuV.png)

### gh issues

List all issues matching the filter.

Usage:

    $ gh issues [-f/--issue_filter] [-s/--issue_state] [-l/--limit] [-p/--pager]

Option(s):

```
:type issue_filter: str
:param issue_filter: assigned, created, mentioned, subscribed (default).

:type issue_state: str
:param issue_state: all, open (default), closed.

:type limit: int
:param limit: The number of items to display.

:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh issues
    $ gh issues -f assigned
    $ gh issues --issue_filter created
    $ gh issues -s all -l 20 -p
    $ gh issues --issue_state closed --limit 20 --pager
    $ gh issues -f created -s all -p

![Imgur](http://i.imgur.com/AB5zxxo.png)

### gh license

Output the license template for the given license.

Usage:

    $ gh license [license_name]

Param(s):

```
:type license_name: str
:param license_name: The license name.
```

Example(s):

    $ gh license apache-2.0
    $ gh license mit > LICENSE

![Imgur](http://i.imgur.com/zJHVxaA.png)

### gh licenses

Output all supported license templates.

Usage/Licenses:

    $ gh licenses

![Imgur](http://i.imgur.com/S9SbMLJ.png)

### gh me

List information about the logged in user.

Displaying the avatar will require [installing the optional `PIL` dependency](#installing-pil).

Usage:

    $ gh me [-b/--browser] [-t/--text_avatar] [-l/--limit] [-p/--pager]

Option(s):

```
:type browser: bool
:param browser: Determines whether to view the profile
    in a browser, or in the terminal.

:type text_avatar: bool
:param text_avatar: Determines whether to view the profile
    avatar in plain text.
    On Windows this value is always set to True due to lack of
    support of `img2txt` on Windows.

:type limit: int
:param limit: The number of user repos to display.

:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh me
    $ gh me -b
    $ gh me --browser
    $ gh me -t -l 20 -p
    $ gh me --text_avatar --limit 20 --pager

![Imgur](http://i.imgur.com/csk5j0S.png)

### gh notifications

List all notifications.

Usage:

    $ gh notifications [-l/--limit] [-p/--pager]

Option(s):

```
:type limit: int
:param limit: The number of items to display.

:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh notifications
    $ gh notifications -l 20 -p
    $ gh notifications --limit 20 --pager

![Imgur](http://i.imgur.com/uwmwxsW.png)

### gh octo

Output an Easter egg or the given message from Octocat.

Usage:

    $ gh octo [say]

Param(s):

```
:type say: str
:param say: What Octocat should say.
        If say is None, octocat speaks an Easter egg.
```

Example(s):

    $ gh octo
    $ gh octo "foo bar"

![Imgur](http://i.imgur.com/bNzCa5p.png)

### gh pull-request

Output detailed information about the given pull request.

Usage:

    $ gh pull-request [user_repo_number]

Param(s):

```
:type user_repo_number: str
:param user_repo_number: The user/repo/pull_number.
```

Example(s):

    $ gh pull-request donnemartin/saws/80

![Imgur](http://i.imgur.com/3MtKjKy.png)

### gh pull-requests

List all pull requests.

Usage:

    $ gh pull-requests [-l/--limit] [-p/--pager]

Option(s):

```
:type limit: int
:param limit: The number of items to display.

:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh pull-requests
    $ gh pull-requests -l 20 -p
    $ gh pull-requests --limit 20 --pager

![Imgur](http://i.imgur.com/4A2eYM9.png)

### gh rate-limit

Output the rate limit.  Not available for GitHub Enterprise.

Usage/Example(s):

    $ gh rate-limit

### gh repo

Output detailed information about the given repo.

Usage:

    $ gh repo [user_repo]

Param(s):

```
:type user_repo: str
:param user_repo: The user/repo.
```

Example(s):

    $ gh repo donnemartin/haxor-news

![Imgur](http://i.imgur.com/XFMpWCI.png)

### gh repos

List all repos matching the given filter.

Usage:

    $ gh repos [repo_filter] [-l/--limit] [-p/--pager]

Param(s):

```
:type repo_filter: str
:param repo_filter:  The filter for repo names.
    Only repos matching the filter will be returned.
    If None, outputs all the logged in user's repos.
```

Option(s):

```
:type limit: int
:param limit: The number of items to display.

:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh repos
    $ gh repos aws
    $ gh repos aws -l 20 -p
    $ gh repos aws --limit 20 --pager

![Imgur](http://i.imgur.com/YXWPWma.png)

### gh search-issues

Search for all issues matching the given query.

For more information about the query qualifiers, visit the [searching issues reference](https://help.github.com/articles/searching-issues/).

Usage:

    $ gh search-issues [query] [-l/--limit] [-p/--pager]

Param(s):

```
:type query: str
:param query: The search query.

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
```

Option(s):

```
:type limit: int
:param limit: The number of items to display.

:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh search-issues "foo type:pr author:donnemartin" -l 20 -p
    $ gh search-issues "foobarbaz in:title created:>=2015-01-01" --limit 20 --pager


Additional Example(s):

```
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
```

![Imgur](http://i.imgur.com/DXXxkBD.png)

### gh search-repos

Search for all repos matching the given query.

For more information about the query qualifiers, visit the [searching repos reference](https://help.github.com/articles/searching-repositories/).

Usage:

    $ gh search-repos [query] [-s/--sort] [-l/--limit] [-p/--pager]

Param(s):

```
:type query: str
:param query: The search query.

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
```

Option(s):

```
:type sort: str
:param sort: Optional: 'stars', 'forks', 'updated'.
    If not specified, sorting is done by query best match.

:type limit: int
:param limit: The number of items to display.

:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh search-repos "maps language:python" -s stars -l 20 -p
    $ gh search-repos "created:>=2015-01-01 stars:>=1000 language:python" --sort stars --limit 20 --pager

![Imgur](http://i.imgur.com/kazXWWY.png)

### gh starred

Output starred repos.

Usage:

    $ gh starred [repo_filter] [-l/--limit] [-p/--pager]

Param(s):

```
:type repo_filter: str
:param repo_filter:  The filter for repo names.
    Only repos matching the filter will be returned.
    If None, outputs all starred repos.
```

Option(s):

```
:type limit: int
:param limit: The number of items to display.

:type pager: bool
:param pager: Determines whether to show the output in a pager,
    if available.
```

Example(s):

    $ gh starred
    $ gh starred foo -l 20 -p
    $ gh starred foo --limit 20 --pager

![Imgur](http://i.imgur.com/JB88Kw8.png)

### gh trending

List trending repos for the given language.

Usage:

    $ gh trending [language] [-w/--weekly] [-m/--monthly] [-D/--devs] [-b/--browser] [-p/--pager]

Param(s):

```
:type language: str
:param language: The language (optional).
    If blank, shows 'Overall'.
```

Option(s):

```
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
```

Example(s):

    $ gh trending
    $ gh trending Python -w -p
    gh trending Python --weekly --devs --browser
    $ gh trending --browser

![Imgur](http://i.imgur.com/Dx77HFW.png)

### gh user

List information about the given user.

Displaying the avatar will require [installing the optional `PIL` dependency](#installing-pil).

Usage:

    $ gh user [user_id] [-b/--browser] [-t/--text_avatar] [-l/--limit] [-p/--pager]

Param(s):

```
:type user_id: str
:param user_id: The user id/login.
    If None, returns followers of the logged in user.
```

Option(s):

```
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
```

Example(s):

    $ gh user octocat
    $ gh user octocat -b
    $ gh user octocat --browser
    $ gh user octocat -t -l 10 -p
    $ gh user octocat --text_avatar --limit 10 --pager

![Imgur](http://i.imgur.com/xVoVPVe.png)

### gh view

View the given notification/repo/issue/pull_request/user index in the terminal or a browser.

This method is meant to be called after one of the following commands
which outputs a table of notifications/repos/issues/pull_requests/users:

    gh repos
    gh search-repos
    gh starred

    gh issues
    gh pull-requests
    gh search-issues

    gh notifications
    gh trending

    gh user
    gh me

Usage:

    $ gh view [index] [-b/--browser]

Param(s):

```
:type index: str
:param index: Determines the index to view.
```

Option(s):

```
:type browser: bool
:param browser: Determines whether to view the profile
    in a browser, or in the terminal.
```

Example(s):

    $ gh repos
    $ gh view 1

    $ gh starred
    $ gh view 1 -b
    $ gh view 1 --browser

![Imgur](http://i.imgur.com/NVEwGbV.png)

### Option: View in a Pager

Many `gh` commands support a `-p/--pager` option that displays results in a pager, where available.

Usage:

    $ gh <command> [param] [options] -p
    $ gh <command> [param] [options] --pager

### Option: View in a Browser

Many `gh` commands support a `-b/--browser` option that displays results in your default browser instead of your terminal.

Usage:

    $ gh <command> [param] [options] -b
    $ gh <command> [param] [options] --browser
