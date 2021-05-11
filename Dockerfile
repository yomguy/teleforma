# Copyright 2013 Thatcher Peskens
# Copyright 2014-2015 Guillaume Pellerin
# Copyright 2014-2015 Thomas Fillon
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM parisson/telemeta:latest-dev

MAINTAINER Guillaume Pellerin <yomguy@parisson.com>

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /srv/app
RUN mkdir -p /srv/lib/teleforma

WORKDIR /srv

RUN apt-get update && apt-get install -y apt-transport-https
# COPY etc/apt/sources.list /etc/apt/
COPY requirements-debian.txt /srv
RUN apt-get update && \
    DEBIAN_PACKAGES=$(egrep -v "^\s*(#|$)" /srv/requirements-debian.txt) && \
    apt-get install -y --force-yes $DEBIAN_PACKAGES && \
    echo fr_FR.UTF-8 UTF-8 >> /etc/locale.gen && \
    locale-gen && \
    apt-get clean

ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

COPY requirements-dev.txt /srv
RUN pip install -r requirements-dev.txt --src /srv/lib

COPY requirements.txt /srv
RUN pip install -r requirements.txt

WORKDIR /srv/lib/teleforma
COPY setup.py /srv/lib/teleforma
COPY teleforma /srv/lib/teleforma
COPY README.rst /srv/lib/teleforma
RUN python setup.py develop

WORKDIR /srv/app

EXPOSE 8000
