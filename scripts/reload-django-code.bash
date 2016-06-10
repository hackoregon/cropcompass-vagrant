#!/bin/bash

echo `date` "stopping app server"
sudo service uwsgi stop
echo `date` "Copying Django app from '/vagrant/django-app' to '~vagrant/cropcompass'"
cp -rp /vagrant/django-app ~vagrant/cropcompass
echo `date` "starting app server"
sudo service uwsgi start
