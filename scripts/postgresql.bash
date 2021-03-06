#!/bin/bash

if [ -e ~vagrant/.postgresql ]
then
  echo `date` "PostgreSQL provisioning already done - exiting"
  exit
fi

echo `date` "Creating the PostgreSQL 'vagrant' user and database"
sudo su postgres -c "createuser -s vagrant"
createdb vagrant

echo `date` "Restoring SQL dump"
createuser alex
curl -Ls https://github.com/hackoregon/cropcompass-sql-dumps/raw/master/agtechdump2016-06-09.sql \
  | psql > ~/logs/psql 2>&1

echo `date` "Logging table details to ~vagrant/logs/tables"
psql -c '\d+' > ~vagrant/logs/tables

touch ~vagrant/.postgresql
