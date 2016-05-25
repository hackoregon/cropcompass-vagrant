#!/bin/bash

echo "Creating the PostgreSQL 'vagrant' user and database"
sudo su postgres -c "createuser -s vagrant"
createdb vagrant

echo "Restoring SQL dump"
createuser alex
rm -f agtechdump2016-05-19.sql
wget --quiet https://www.dropbox.com/s/t6t1r3x6a4lp0zi/agtechdump2016-05-19.sql
psql < /vagrant/agtech*sql > ~/logs/psql 2>&1
