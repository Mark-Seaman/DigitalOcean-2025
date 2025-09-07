#!/bin/bash

# Traverse all directories, deepest first (bottom-up)
find . -depth -name "*[A-Z]*" | while read f; do
    newf=$(echo "$f" | tr 'A-Z' 'a-z')
    if [ "$f" != "$newf" ]; then
        git mv "$f" "$newf"
    fi
done