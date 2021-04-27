#!/bin/sh -l

echo "Hello, World in entrypoint.sh"

echo "===================="
pwd

echo "ls ====================="
ls -a
echo "ls / ===================="
ls -a /
echo "ls /github =============="
ls -a /github
echo "ls /github/workspace ===="
ls -a /github/workspace
echo "ls /github/workflow ======"
ls -a /github/workflow

python /myapp/src/main.py
