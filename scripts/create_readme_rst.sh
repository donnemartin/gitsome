#!/usr/bin/env bash

pandoc --from=markdown --to=rst --output=docs/source/README.rst README.md
pandoc --from=markdown --to=rst --output=README.rst README.md