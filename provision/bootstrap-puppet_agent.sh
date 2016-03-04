#!/bin/bash

curl -o /tmp/puppet-repo.deb http://apt.puppetlabs.com/puppetlabs-release-pc1-trusty.deb
sudo dpkg -i /tmp/puppet-repo.deb
sudo aptitude update
sudo aptitude install puppet-agent -y
sudo update-rc.d puppet disable
