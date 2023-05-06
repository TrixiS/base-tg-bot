FROM python:3.10.11-bullseye

ARG repo

RUN git clone ${repo} ./app

WORKDIR ./app

RUN pip3 install -r requirements.txt
RUN python3 -m prisma db push

CMD python3 -m bot
