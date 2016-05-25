#!/bin/bash

echo `date` "Configuring nginx"
sudo cp /vagrant/scripts/cropcompass.nginx /etc/nginx/sites-available/cropcompass
sudo ln -s /etc/nginx/sites-available/cropcompass /etc/nginx/sites-enabled

echo `date` "Ngnix configtest"
sudo service nginx configtest

echo "Starting uwsgq and nginx"
sudo service nginx restart
sudo service uwsgi start
