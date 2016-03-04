#!/bin/bash
cd /vagrant/provision/puppet

sudo /opt/puppetlabs/bin/puppet apply ./manifests/misc.pp --modulepath=./modules
sudo /opt/puppetlabs/bin/puppet apply ./manifests/nginx.pp --modulepath=./modules
sudo /opt/puppetlabs/bin/puppet apply ./manifests/mysql.pp --modulepath=./modules
sudo /opt/puppetlabs/bin/puppet apply ./manifests/urbandev_frontend.pp --modulepath=./modules
sudo /opt/puppetlabs/bin/puppet apply ./manifests/urbandev_backend.pp --modulepath=./modules
