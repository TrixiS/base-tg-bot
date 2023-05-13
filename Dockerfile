FROM python:3.10.11-alpine3.18

ARG repo

RUN apk add --update --no-cache git
RUN git clone ${repo} ./app

WORKDIR ./app

RUN pip3 install -r requirements.txt

CMD python3 -m bot
