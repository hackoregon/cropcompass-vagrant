#!/bin/bash

if [ -e ~/Env/cropcompass ]
then
  echo `date` "Django already installed - exiting"
  exit
fi

echo `date` "Making and activating 'cropcompass' virtualenv"
mkdir -p ~/Env
virtualenv -p /usr/bin/python3 ~/Env/cropcompass > ~/logs/virtualenv 2>&1
source ~/Env/cropcompass/bin/activate

echo `date` "Installing Django requirements"
pip install --upgrade pip > ~/logs/pip 2>&1
pip install -r /vagrant/scripts/requirements.txt > ~/logs/requirements 2>&1

echo `date` "Cloning Django application code from GitHub to '~vagrant'"
pushd ~vagrant
git clone https://github.com/hackoregon/cropcompass-django.git cropcompass \
  > ~/logs/django-clone 2>&1
popd

pushd ~/cropcompass
echo `date` "Running migrations"
python3 manage.py migrate > ~/logs/migrate 2>&1
echo `date` "Collecting static assets"
python3 manage.py collectstatic --noinput > ~/logs/static 2>&1
popd
