#!/usr/bin/env bash

flake8 --max-line-length=80 --exclude=build,docs,scratch,docs,html2text.py,compat.py,xonsh,lib,parser.table.py,parser.out,parser_test_table.py,parser_table.py,completions.py,completions_git.py,tests/data/*,.tox/,.eggs/ .
