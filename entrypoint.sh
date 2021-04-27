#!/bin/sh -l

echo "Hello, World in entrypoint.sh"

# show list
ls -a

python src/main.py
