FROM python:3.10.11-alpine3.18

ARG repo

RUN apk add --update --no-cache libc6-compat openssl git npm
RUN git clone ${repo} ./app

WORKDIR ./app

RUN pip3 install -r requirements.txt
RUN python3 -m prisma db push

CMD python3 -m bot
