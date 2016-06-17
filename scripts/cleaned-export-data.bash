#!/bin/bash

if [ -e ~vagrant/.cleaned-export-data ]
then
  echo `date` "Cleaned export data already loaded - exiting"
  exit
fi

echo `date` "stopping app server"
sudo service uwsgi stop

echo `date` "Restoring cleaned export data SQL dump"
curl -Ls \
  https://github.com/hackoregon/cropcompass-sql-dumps/raw/master/exports_historical_cleaned2016_06_16.sql \
  | psql > ~/logs/psql-cleaned 2>&1

echo `date` "Logging table details to ~vagrant/logs/tables-cleaned"
psql -c '\d+' > ~vagrant/logs/tables-cleaned

echo `date` "starting app server"
sudo service uwsgi start

touch ~vagrant/.cleaned-export-data
