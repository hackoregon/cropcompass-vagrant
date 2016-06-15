#!/bin/bash

if [ -e ~/Env/cropcompass ]
then
  echo `date` "Django already installed - exiting"
  exit
fi

echo `date` "Making and activating 'cropcompass' virtualenv"
mkdir -p /home/vagrant/Env
virtualenv -p /usr/bin/python3 ~/Env/cropcompass > ~/logs/virtualenv 2>&1
source ~/Env/cropcompass/bin/activate

echo `date` "Installing Django requirements"
pip install --upgrade pip > ~/logs/pip 2>&1
pip install -r /vagrant/scripts/requirements.txt > ~/logs/requirements 2>&1
