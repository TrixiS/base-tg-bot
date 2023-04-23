FROM python:3.10.11-bullseye

ARG repo

RUN git clone ${repo} ./app

WORKDIR ./app

RUN pip3 install -r requirements.txt
RUN python3 -m prisma db push

CMD git pull origin master && python3 -m prisma migrate deploy && python3 -m prisma db push && python3 -m bot