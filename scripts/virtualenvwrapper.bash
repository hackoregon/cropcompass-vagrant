#!/bin/bash

if [ -e /usr/local/bin/virtualenvwrapper.sh ]
then
  echo "virtualenvwrapper already installed - exiting"
  exit
fi

# https://virtualenvwrapper.readthedocs.io/en/latest/index.html
echo `date` "Installing virtualenv wrapper"
sudo pip3 install virtualenv virtualenvwrapper > ~/logs/virtualenvwrapper 2>&1
echo "set bg=dark" >> ~/.vimrc
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "export WORKON_HOME=~/Env" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
mkdir -p ~/Env
