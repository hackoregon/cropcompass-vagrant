#!/bin/bash

# make a log directory
mkdir -p ~/logs

# set working directory
cd /vagrant

echo `date`; /vagrant/scripts/ubuntu.bash
echo `date`; /vagrant/scripts/postgresql.bash
echo `date`; /vagrant/scripts/virtualenvwrapper.bash
echo `date`; /vagrant/scripts/django.bash
echo `date`
