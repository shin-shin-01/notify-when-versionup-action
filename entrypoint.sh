#!/bin/sh -l

echo "Hello, World in entrypoint.sh"

# show list
ls -a
ls -a /
ls -a /github
ls -a /github/workspace
ls -a /github/workflow

python /myapp/src/main.py
