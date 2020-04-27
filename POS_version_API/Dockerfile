FROM python:3.8-alpine

RUN adduser -D api

RUN apk add bash vim

WORKDIR /home/api
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY src ./
COPY boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R api:api ./

USER api

VOLUME ["/templates"]
EXPOSE 5000
ENV TEMPLATES_DIR /templates
ENTRYPOINT ["./boot.sh"]
