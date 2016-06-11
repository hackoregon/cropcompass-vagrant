#!/bin/bash

echo `date` "Creating the PostgreSQL 'vagrant' user and database"
sudo su postgres -c "createuser -s vagrant"
sudo su vagrant
createdb vagrant
ex

echo `date` "Restoring SQL dump"
sudo su postgres -c "createuser -s alex"
curl -Ls https://github.com/hackoregon/cropcompass-sql-dumps/raw/master/agtechdump2016-05-19.sql \
  | psql > /home/vagrant/logs/psql 2>&1
