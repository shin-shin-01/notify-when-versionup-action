FROM ubuntu:18.04
# TODO: fix if closed -> https://api.github.com/repos/octocat/hello-world/issues/42# https://api.github.com/repos/octocat/hello-world/issues/42

COPY . /app
RUN make /app
CMD python /app/app.py
