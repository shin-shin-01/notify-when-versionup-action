#!/bin/sh -l

echo "Hello, World in entrypoint.sh"

echo "ls ====================="
ls -a

python /myapp/src/main.py
