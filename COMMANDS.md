# Commands

## GitHub Integration Commands Reference

Check out the handy [autocompleter with interactive help](https://github.com/donnemartin/haxor-news/blob/master/README.md#git-and-github-autocompleter-with-interactive-help) to guide you through each command.

### gh configure

Configure `gitsome`.

Attempts to authenticate the user and to set up the user's news feed.

If `gitsome` has not yet been configured, calling a `gh` command that requires authentication will automatically invoke the `configure` command.

Usage/Example(s):

    $ gh configure

#### Authentication

To properly integrate with GitHub, you will be asked to enter a user name and either a password or a [personal access token](https://github.com/settings/tokens).  **If you use two-factor authentication, you must log in with a personal access token**, for more details see this [ticket](https://github.com/sigmavirus24/github3.py/issues/387).

Visit the following page to generate a token:

[https://github.com/settings/tokens](https://github.com/settings/tokens)

`gitsome` will need the 'repo' and 'user' permissions.

#### Authentication Source Code

Curious what's going on behind the scenes with authentication?  Check out the [authentication source code](https://github.com/donnemartin/gitsome/blob/master/gitsome/config.py#L156-L269).

#### User Feed

`gitsome` will need your news feed url to run the `gh feed` command with no arguments.

To integrate `gitsome` with your news feed, visit the following url while logged into GitHub:

[https://github.com](https://github.com)

You will be asked to enter the url found when clicking 'Subscribe to your news feed', which will look something like this:

    https://github.com/donnemartin.private.atom?token=TOKEN

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

If `user_or_repo` is not provided, uses the logged in user's news feed seen while visiting https://github.com.  If `user_or_repo` is provided, shows either the public or `[-p/--private]` feed activity of the user or repo.

Usage:

    $ gh feed [user_or_repo] [-p/--private] [-p/--pager]

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
    $ gh issues ---issue_filter created
    $ gh issues -s all -l 20 -p
    $ gh issues --issue_state closed --limit 20 --pager
    $ gh issues -f created -s all -p

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

### gh licenses

Output all supported license templates.

Usage/Licenses:

    $ gh licenses

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
