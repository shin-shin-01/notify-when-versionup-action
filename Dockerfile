FROM python:latest

RUN mkdir /myapp
ADD . /myapp

WORKDIR /myapp

RUN pip install -r requirements.txt

RUN chmod +x /myapp/entrypoint.sh

ENTRYPOINT ["/myapp/entrypoint.sh"]
