#!/bin/sh -l

echo "Hello, World in entrypoint.sh"

# github actions inputs
GITHUB_TOKEN=$1
GITHUB_REPOSITORY=$2
GITHUB_DEFAULT_BRANCH=$3

# issue と release url が同一行に記載されていたら別々に処理できなくなるため
# コメント検出を２回に分けて行い 処理を分ける

# ISSUE ==========================================
# コメントを検出する
# ex) ./test/Dockerfile:2:# https://github.com/shin-shin-01/github-test/issues/2
FILE_COMMENT_RESULT=`find . -name Dockerfile | xargs grep -s -n "#.*https://github.com/[^/]*/[^/]*/issues/\d*" `

# 改行 で split
# $'\n' not working in docker
IFS=$'
'

for result in $FILE_COMMENT_RESULT
do

python /myapp/src/main.py $GITHUB_TOKEN $GITHUB_REPOSITORY $GITHUB_DEFAULT_BRANCH "issue" $result

done

# RELEASE ==========================================
# コメントを検出する
# ex) ./test/Dockerfile:2:# https://github.com/shin-shin-01/github-test/releases
FILE_COMMENT_RESULT=`find . -name Dockerfile | xargs grep -s -n "#.*https://github.com/[^/]*/[^/]*/releases" `

# 改行 で split
# $'\n' not working in docker
IFS=$'
'

for result in $FILE_COMMENT_RESULT
do

python /myapp/src/main.py $GITHUB_TOKEN $GITHUB_REPOSITORY $GITHUB_DEFAULT_BRANCH "release" $result

done
