#!/bin/bash

echo `date` "stopping app server"
sudo service uwsgi stop
echo `date` "backing up old cropcompass Django app"
mv ~/cropcompass ~/cropcompass-`date -Iseconds`
echo `date` "copying Django app from '/vagrant/django-app' to '~vagrant/cropcompass'"
cp -rp /vagrant/django-app ~vagrant/cropcompass
echo `date` "starting app server"
sudo service uwsgi start
