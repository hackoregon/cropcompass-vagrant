#!/bin/bash

echo `date` "Making cropcompass virtualenv"
virtualenv -p /usr/bin/python3 ~/Env/cropcompass > ~/logs/virtualenv 2>&1

echo `date` "Installing Django requirements"
source ~/Env/cropcompass/bin/activate
pip install --upgrade pip > ~/logs/pip 2>&1
pip install -r /vagrant/scripts/requirements.txt > ~/logs/requirements 2>&1

echo `date` "Running migrations"
pushd /vagrant/cropcompass
python3 manage.py migrate > ~/logs/migrate 2>&1
popd
