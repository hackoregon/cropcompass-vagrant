#!/bin/bash

if [ -d ~vagrant/cropcompass ]
then
  echo `date` "Django app already provisioned - exiting"
  exit
fi
exit

echo `date` "Copying Django app from '/vagrant/django-app' to '~vagrant/cropcompass'"
cp -rp /vagrant/django-app ~vagrant/cropcompass

pushd ~/cropcompass
echo `date` "Running migrations"
python3 manage.py migrate > ~/logs/migrate 2>&1
echo `date` "Collecting static assets"
python3 manage.py collectstatic --noinput > ~/logs/static 2>&1
popd
