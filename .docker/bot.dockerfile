# syntax=docker/dockerfile:1

FROM python:3.10.11-alpine3.18

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

CMD python3 -m bot
