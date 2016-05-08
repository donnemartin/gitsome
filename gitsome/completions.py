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

COMPLETIONS_GH = {
    'configure': {
        'desc': "Configures gitsome.",
        'args': {},
        'opts': {},
    },
    'create-comment': {
        'desc': 'Creates a comment on the given issue.',
        'args': {
            'octocat/Spoon-Knife/1': 'str (req) user/repo/issue_number combo.',
        },
        'opts': {
            '-t': 'see associated -- option for details.',
            '--text': 'str (req) comment text.',
        },
    },
    'create-issue': {
        'desc': 'Creates an issue.',
        'args': {
            'octocat/Spoon-Knife': 'str (req) user/repository combo.',
        },
        'opts': {
            '-t': 'see associated -- option for details.',
            '--issue_title': 'str (req) issue title.',
            '-d': 'str (opt) issue description.',
            '--issue_desc': 'str (opt) issue description.',
        },
    },
    'create-repo': {
        'desc': 'Creates a repository.',
        'args': {
            'Spoon-Knife': 'str (req) repository name.',
        },
        'opts': {
            '-d': 'str (opt) repo description',
            '--repo_desc': 'str (opt) repo description.',
            '-pr': 'flag (opt) create a private repo',
            '--private': 'flag (opt) create a private repo',
        },
    },
    'emails': {
        'desc': "Lists all the user's registered emails.",
        'args': {},
        'opts': {},
    },
    'emojis': {
        'desc': 'Lists all GitHub supported emojis.',
        'args': {},
        'opts': {
            '-p': 'flag (req) show results in a pager.',
            '--pager': 'flag (req) show results in a pager.',
        },
    },
    'feed': {
        'desc': "Lists all activity for the given user or repo, if called with no arg, shows the logged in user's feed.",
        'args': {
            'octocat/Hello-World --pager': "str (opt) user or user/repository combo, if blank, shows the logged in user's feed.",
        },
        'opts': {
            '-pr': 'flag (req) also show private events.',
            '--private': 'flag (req) also show private events.',
            '-p': 'flag (req) show results in a pager.',
            '--pager': 'flag (req) show results in a pager.',
        },
    },
    'followers': {
        'desc': 'Lists all followers and the total follower count.',
        'args': {
            'octocat': "str (req) the user's login id, if blank, shows logged in user's info.",
        },
        'opts': {
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'following': {
        'desc': 'Lists all followed users and the total followed count.',
        'args': {
            'octocat': "str (req) the user's login id, if blank, shows logged in user's info.",
        },
        'opts': {
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'gitignore-template': {
        'desc': 'Outputs the gitignore template for the given language.',
        'args': {
            'Python': 'str (req) the language-specific .gitignore.',
        },
        'opts': {},
    },
    'gitignore-templates': {
        'desc': 'Outputs all supported gitignore templates.',
        'args': {},
        'opts': {
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'issue': {
        'desc': 'Outputs detailed information about the given issue.',
        'args': {
            'octocat/Spoon-Knife/1': 'str (req) user/repo/issue_number combo.',
        },
        'opts': {},
    },
    'issues': {
        'desc': 'Lists all issues matching the filter.',
        'args': {},
        'opts': {
            '-f': 'str (opt) "assigned", "created", "mentioned", "subscribed" (default).',
            '--issue_filter': 'str (opt) "assigned", "created", "mentioned", "subscribed" (default).',
            '-s': 'str (opt) "all", "open" (default), "closed".',
            '--issue_state': 'str (opt) "all", "open" (default), "closed".',
            '-l': 'flag (opt) num items to show, defaults to 1000.',
            '--limit': 'flag (opt) num items to show, defaults to 1000.',
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'license': {
        'desc': 'Outputs the license template for the given license.',
        'args': {
            'apache-2.0': 'str (req) the license name.',
        },
        'opts': {},
    },
    'licenses': {
        'desc': 'Outputs all supported license templates.',
        'args': {},
        'opts': {},
    },
    'me': {
        'desc': 'Lists information about the logged in user.',
        'args': {},
        'opts': {
            '-b': 'flag (opt) view profile in a browser instead of the terminal.',
            '--browser': 'flag (opt) view profile in a browser instead of the terminal.',
            '-t': 'see associated -- option for details.',
            '--text_avatar': 'flag (opt) view profile pic in plain text.',
            '-l': 'flag (opt) num items to show, defaults to 1000.',
            '--limit': 'flag (opt) num items to show, defaults to 1000.',
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'notifications': {
        'desc': 'Lists all notifications.',
        'args': {},
        'opts': {
            '-l': 'flag (opt) num items to show, defaults to 1000.',
            '--limit': 'flag (opt) num items to show, defaults to 1000.',
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'octo': {
        'desc': 'Outputs an Easter egg or the given message from Octocat.',
        'args': {
            '"Keep it logically awesome"': 'str (req) a message from Octocat, if empty, Octocat speaks an Easter egg.',
        },
        'opts': {},
    },
    'pull-request': {
        'desc': 'Outputs detailed information about the given pull request.',
        'args': {
            'octocat/Spoon-Knife/3': 'str (req) user/repo/pull_number combo.',
        },
        'opts': {},
    },
    'pull-requests': {
        'desc': 'Lists all pull requests.',
        'args': {},
        'opts': {
            '-l': 'flag (opt) num items to show, defaults to 1000.',
            '--limit': 'flag (opt) num items to show, defaults to 1000.',
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'rate-limit': {
        'desc': 'Outputs the rate limit.',
        'args': {},
        'opts': {},
    },
    'repo': {
        'desc': 'Outputs detailed information about the given repo.',
        'args': {
            'octocat/Spoon-Knife': 'str (req) user/repository combo.',
        },
        'opts': {},
    },
    'repos': {
        'desc': 'Lists all repos matching the given filter.',
        'args': {
            '"foo bar optional filter"': 'str (opt) filters repos by name.',
        },
        'opts': {
            '-l': 'flag (opt) num items to show, defaults to 1000.',
            '--limit': 'flag (opt) num items to show, defaults to 1000.',
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'search-issues': {
        'desc': 'Searches for all issues matching the given query.',
        'args': {
            '"foobarbaz in:title created:>=2015-01-01"': 'str (req) the search query.',
        },
        'opts': {
            '-s': 'str (opt) "stars", "forks", "updated", if blank, sorts by query best match.',
            '--sort': 'str (opt) "stars", "forks", "updated", if blank, sorts by query best match.',
            '-l': 'flag (opt) num items to show, defaults to 1000.',
            '--limit': 'flag (opt) num items to show, defaults to 1000.',
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'search-repos': {
        'desc': 'Searches for all repos matching the given query.',
        'args': {
            '"created:>=2015-01-01 stars:>=1500 language:python"': 'str (req) the search query.',
        },
        'opts': {
            '-s': 'str (opt) "stars", "forks", "updated", if blank, sorts by query best match.',
            '--sort': 'str (opt) "stars", "forks", "updated", if blank, sorts by query best match.',
            '-l': 'flag (opt) num items to show, defaults to 1000.',
            '--limit': 'flag (opt) num items to show, defaults to 1000.',
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'starred': {
        'desc': 'Outputs starred repos.',
        'args': {
            '"foo bar optional filter"': 'str (opt) filters repos by name.',
        },
        'opts': {
            '-l': 'flag (opt) num items to show, defaults to 1000.',
            '--limit': 'flag (opt) num items to show, defaults to 1000.',
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'trending': {
        'desc': 'Lists trending repos for the given language.',
        'args': {
            'Overall': 'str (opt) the language filter for trending repos, if blank, the overall rankings are shown.',
        },
        'opts': {
            '-w': 'flag (opt) show the weekly trending repos.',
            '--weekly': 'flag (opt) show the weekly trending repos.',
            '-m': 'flag (opt) show the monthly trending repos.',
            '--monthly': 'flag (opt) show the monthly trending repos.',
            '-D': 'flag (opt) view trending devs.  Only valid with -b/--browser.',
            '--devs': 'flag (opt) view trending devs.  Only valid with -b/--browser.',
            '-b': 'flag (opt) view profile in a browser instead of the terminal.',
            '--browser': 'flag (opt) view profile in a browser instead of the terminal.',
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'user': {
        'desc': 'Lists information about the given user.',
        'args': {
            'github --pager': "str (req) the user's login id.",
        },
        'opts': {
            '-b': 'flag (opt) view profile in a browser instead of the terminal.',
            '--browser': 'flag (opt) view profile in a browser instead of the terminal.',
            '-t': 'see associated -- option for details.',
            '--text_avatar': 'flag (opt) view profile pic in plain text.',
            '-l': 'flag (opt) num items to show, defaults to 1000.',
            '--limit': 'flag (opt) num items to show, defaults to 1000.',
            '-p': 'flag (opt) show results in a pager.',
            '--pager': 'flag (opt) show results in a pager.',
        },
    },
    'view': {
        'desc': 'Views the given repo or issue index in the terminal or a browser.',
        'args': {
            '1': 'int (req) the 1-based index to view.',
        },
        'opts': {
            '-b': 'flag (opt) view profile in a browser instead of the terminal.',
            '--browser': 'flag (opt) view profile in a browser instead of the terminal.',
        },
    },
}
META_LOOKUP_GH = {
    '10': 'limit: int (opt) limits the posts displayed',
    '"(?i)(Python|Django)"': ('regex_query: string (opt) applies a regular '
                              'expression comment filter'),
    '1': 'index: int (req) views the post index',
    '"user"': 'user:string (req) shows info on the specified user',
    'gh': 'Git auto-completer with GitHub integration.',
}
SUBCOMMANDS = {}


def build_meta_lookups():
    for subcommand, args_opts in COMPLETIONS_GH.items():
        META_LOOKUP_GH.update({subcommand: COMPLETIONS_GH[subcommand]['desc']})
        SUBCOMMANDS.update({subcommand: COMPLETIONS_GH[subcommand]['desc']})
        for opt, meta in args_opts['opts'].items():
            META_LOOKUP_GH.update({opt: meta})
        for arg, meta in args_opts['args'].items():
            META_LOOKUP_GH.update({arg: meta})


build_meta_lookups()
