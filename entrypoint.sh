#!/bin/sh -l

echo "Hello, World in entrypoint.sh"


# TODO: add release url

# コメントを検出する
# - 現状ではDockerfileに限らず取得
# ex) ./test/Dockerfile:2:# https://github.com/shin-shin-01/github-test/issues/2
FILE_COMMENT_RESULT=`find . -type f -print | xargs grep -s -n "#[^\n]*https://github.com/[^/]*/[^/]*/issues/\d*" `

# 改行 で split
# $'\n' not working in docker
IFS=$'
'

for result in $FILE_COMMENT_RESULT
do

python /myapp/src/main.py $result

done
