#!/bin/bash

echo `date` "Autoremoving unused packages"
sudo apt-get autoremove -y > ~/logs/autoremove 2>&1

# PostgreSQL repository
# http://www.postgresql.org/download/linux/ubuntu/
echo `date` "Attaching PostgreSQL package repositories"
echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > pgdg.list
sudo mv pgdg.list /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

echo `date` "Syncing Ubuntu repositories"
sudo apt-get update > ~/logs/update 2>&1

echo `date` "Upgrading Ubuntu"
sudo apt-get -y upgrade > ~/logs/upgrade 2>&1

echo `date` "Installing Ubuntu packages"
sudo apt-get install -y \
  build-essential \
  git \
  libncurses5-dev \
  libreadline-dev \
  nginx \
  postgresql-9.5 \
  postgresql-9.5-postgis-2.2 \
  postgresql-client-9.5 \
  postgresql-contrib-9.5 \
  postgresql-server-dev-9.5 \
  python-dev \
  python-pip \
  python3-dev \
  python3-pip \
  vim-nox \
  > /home/ubuntu/logs/install 2>&1
