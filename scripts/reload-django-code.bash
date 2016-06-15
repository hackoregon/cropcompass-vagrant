#!/bin/bash

echo `date` "stopping app server"
sudo service uwsgi stop
echo `date` "backing up old cropcompass Django app"
export STAMP=`date -Iseconds`
cp -rp ~/cropcompass ~/cropcompass-${STAMP}
echo `date` "copying Django app from '/vagrant/django-app' to '~vagrant/cropcompass'"
diff -Naur /vagrant/django-app ~vagrant/cropcompass > ~vagrant/logs/${STAMP}.diff
cp -rp /vagrant/django-app/* ~vagrant/cropcompass/
echo `date` "starting app server"
sudo service uwsgi start
