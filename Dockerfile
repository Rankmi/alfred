FROM ubuntu:18.04

COPY . /usr/alfred
WORKDIR /usr/alfred 

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN ./installer.sh && ./generator.sh ins gen

ARG gh_token
ENV env_gh_token="Token = $gh_token"

RUN echo "[GLOBAL]" > /root/.alfred.conf
RUN echo $env_gh_token >> /root/.alfred.conf

RUN ./dist/alfred release new
