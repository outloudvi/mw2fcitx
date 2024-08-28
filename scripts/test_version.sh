#!/bin/bash
VERSION=$(grep PKG_VERSION mw2fcitx/version.py | sed -E 's/PKG_VERSION = "(.*)"/\1/g')
echo "Expected version: $VERSION"
grep "version = \"$VERSION\"" pyproject.toml && echo "OK!" || (
    echo "BAD! Actual version: $(grep version pyproject.toml)"
    exit 1
)
