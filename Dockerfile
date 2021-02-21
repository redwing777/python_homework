FROM docker.io/library/alpine:3.10
ENV CGO_ENABLED=0
# Configuration Parameters
ARG SERVICE_USER=auto-tester
ARG SERVICE_HOME=/home/${SERVICE_USER}
# Update apk repositories
RUN echo "@latestcommunity http://uk.alpinelinux.org/alpine/latest-stable/community" >> /etc/apk/repositories \
  && apk update \
# Install packages
  && apk add --no-cache --upgrade ca-certificates gcc libffi-dev musl-dev openssl-dev make \
  bash curl dbus-x11 git nano sudo py3-lxml linux-headers python3-dev docker g++ py3-pip
WORKDIR tmp
COPY ./requirements.txt .
RUN sudo pip3 install --upgrade pip \
  && pip3 --no-cache-dir install -r requirements.txt -U
USER root
