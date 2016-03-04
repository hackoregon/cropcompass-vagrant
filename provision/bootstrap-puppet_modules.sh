#!/bin/bash

if [ ! -d ~/.rvm ]; then
  gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
  \curl -sSL https://get.rvm.io | bash -s stable --ruby=2.2.1
  source ~/.bashrc
  source ~/.bash_profile
fi

gem install librarian-puppet

cd /vagrant/provision/puppet
librarian-puppet install
