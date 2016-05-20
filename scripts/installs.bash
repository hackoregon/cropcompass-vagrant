#!/bin/bash

# make a log directory
mkdir -p ~/logs

# set working directory
cd /vagrant

# PostgreSQL repository
# http://www.postgresql.org/download/linux/ubuntu/
echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > pgdg.list
sudo mv pgdg.list /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo apt-get update > ~/logs/update
echo "Upgrading Ubuntu"
sudo apt-get -y upgrade > ~/logs/upgrade
echo "Installing Ubuntu packages"
sudo apt-get install -y \
  build-essential \
  libncurses5-dev \
  libreadline-dev \
  nginx-light \
  postgresql-9.4 \
  postgresql-9.4-postgis-2.2 \
  postgresql-client-9.4 \
  postgresql-contrib-9.4 \
  postgresql-server-dev-9.4 \
  python-dev \
  python-pip \
  python-virtualenv \
  python3-dev \
  vim-nox \
  virtualenvwrapper \
  > ~/logs/install
echo "Autoremoving unused packages"
sudo apt-get autoremove -y > ~/logs/autoremove
echo "Creating the PostgreSQL 'vagrant' user and database"
sudo su postgres -c "createuser -s vagrant"
createdb vagrant
createuser alex
virtualenv -p /usr/bin/python3.4 ~/cropcompass
source ~/cropcompass/bin/activate
pip install --upgrade pip
pip install -r /vagrant/scripts/requirements.txt 
