FROM ubuntu:18.04
# TODO: fix if closed  https://github.com/shin-shin-01/github-test/issues/3

COPY . /app
# TODO: fix if new veresion released  https://github.com/shin-shin-01/notify-when-versionup-action/releases
RUN make /app
CMD python /app/app.py
