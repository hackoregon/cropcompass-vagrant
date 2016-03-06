#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
export DEBIAN_PRIORITY=critical

APT_GET_CMD='apt-get -y -o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold"'

##
# Function: print_header
#
function print_header {
  echo " "
  echo "##"
  echo "# $1"
  echo "#"
}

##
# Puppet Bootstrap
#
print_header 'Replacing Puppet Agent...'
sudo $APT_GET_CMD install aptitude curl git  > /dev/null 2>&1
curl -o /tmp/puppet-repo.deb http://apt.puppetlabs.com/puppetlabs-release-pc1-trusty.deb --silent
sudo dpkg -i /tmp/puppet-repo.deb  > /dev/null 2>&1
sudo $APT_GET_CMD update  > /dev/null 2>&1
sudo $APT_GET_CMD install puppet-agent  > /dev/null 2>&1
sudo update-rc.d puppet disable  > /dev/null 2>&1

##
# Package Cleanup
#
print_header 'Cleaning Up Package Manager...'
sudo $APT_GET_CMD autoremove  > /dev/null 2>&1
sudo $APT_GET_CMD purge `dpkg -l | grep ^rc | awk '{print $2}'` > /dev/null 2>&1

##
# Package Upgrade
#
print_header 'Upgrade Packages...'
sudo $APT_GET_CMD upgrade  > /dev/null 2>&1

##
# Setup RVM and Puppet Librarian
#
print_header 'Setup RVM and librarian puppet'

# cleanup
#rm -rf ~/.rvm
#rm -rf /vagrant/puppet/.tmp
#rm -rf /vagrant/puppet/.librarian

if [ ! -d ~/.rvm ]; then
  gpg --no-tty -q --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
  \curl -sSL https://get.rvm.io --silent | bash -s stable --ruby=2.2.1 --quiet-curl
fi

source ~/.bashrc
source ~/.bash_profile

gem install librarian-puppet puppet > /dev/null 2>&1

print_header 'Installing Puppet Modules Specified in puppet/Puppetfile...'
cd /vagrant/puppet
librarian-puppet install > /dev/null 2>&1
