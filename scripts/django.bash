#!/bin/bash

echo `date` "Making cropcompass virtualenv"
virtualenv -p /usr/bin/python3 ~/Env/cropcompass > ~/logs/virtualenv 2>&1

echo `date` "Installing Django requirements"
source ~/Env/cropcompass/bin/activate
pip install --upgrade pip > ~/logs/pip 2>&1
pip install -r /vagrant/scripts/requirements.txt > ~/logs/requirements 2>&1

echo `date` "Initializing cropcompass project"
cp -rp /vagrant/cropcompass ~

pushd ~/cropcompass
echo `date` "Running migrations"
python3 manage.py migrate > ~/logs/migrate 2>&1
echo `date` "Collecting static assets"
echo "STATIC_ROOT = os.path.join(BASE_DIR, \"static/\")" >> cropcompass/settings.py
python3 manage.py collectstatic --noinput > ~/logs/static 2>&1
popd
