FROM ubuntu:18.04

COPY . /usr/alfred
WORKDIR /usr/alfred

COPY ./.alfred.conf /root/

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN ./installer.sh && ./generator.sh ins gen

RUN ./dist/alfred dev release --new
