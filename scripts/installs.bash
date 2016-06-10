#!/bin/bash

# make a log directory
mkdir -p ~/logs

# set working directory
cd /vagrant

/vagrant/scripts/ubuntu.bash
/vagrant/scripts/postgresql.bash
/vagrant/scripts/virtualenvwrapper.bash
/vagrant/scripts/django.bash
/vagrant/scripts/django-app.bash
/vagrant/scripts/uwsgi.bash
/vagrant/scripts/nginx.bash
echo `date` "Provisioning complete - logs are in ~vagrant/logs"
