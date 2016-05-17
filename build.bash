#! /bin/bash -v

# script to build initial box

vagrant plugin install vagrant-hostmanager
vagrant plugin install vagrant-reload
vagrant plugin install vagrant-vbguest
vagrant up
