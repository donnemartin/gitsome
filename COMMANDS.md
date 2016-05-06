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
