#!/bin/bash

if [ -e ~/logs/uwsgi ]
then
  echo `date` "uWSGI already installed - exiting"
  exit
fi

echo `date` "Installing uWSGI globally"
sudo pip3 install uwsgi > ~/logs/uwsgi 2>&1

echo `date` "Installing cropcompass uWSGI configuration"
sudo mkdir -p /etc/uwsgi/sites
sudo cp /vagrant/scripts/cropcompass.ini /etc/uwsgi/sites
sudo cp /vagrant/scripts/uwsgi.conf /etc/init
