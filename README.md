# HackOregon UrbanDev Vagrant Environment

Fork this repository to generate a local testing environment.

Please help document any processes here!

This is very much a work in progress.

Implements:
 - mysql-server
 - postgresql server
 - pgloader
 - nginx w/uwsgi
 - deployment of backend
 - deployment of frontend

After Vagrant Up:
 - NGINX will be available at http://localhost:8080
 - MySQL is avaialble at mysql://localhost:33306
 - Postgres is available at pgsql://localhost:55432
 - urbandev frontend and backend are cloned to the 'src' directory.
 - Databases will be populated from a dump file not included in this repository.


## Vagrant Installation

Ubuntu standard box we are using only implements the virtualbox provider.

You will need to install both VirtualBox and Vagrant for your operating system.

Then install the plugins below.

```
vagrant plugin install vagrant-hostmanager
vagrant plugin install vagrant-reload
vagrant plugin install vagrant-vbguest
vagrant up
vagrant ssh
```

See http://vagrantup.com for more installation details






