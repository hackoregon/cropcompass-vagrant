# HackOregon UrbanDev Vagrant Environment

Fork this repository to generate a local testing environment.

Please help document any processes here!


## Vagrant Installation

Assuming VirtualBox.

See http://www.chocolatey.org for details on installing the Chocolatey package manager.

On Windows:

```
chocolatey install -y vagrant virtualbox virtualbox.extensions
vagrant plugin install vagrant-hostmanager
vagrant up
vagrant ssh
```

See vagrantup.com for more installation details


## Plugins Utliized

  - vagrant-hostmanager (1.8.1)
  - vagrant-vbguest (0.11.0)

```
vagrant plugin install vagrant-hostmanager
vagrant plugin install vagrant-reload
```

### VirtualBox
```
vagrant plugin install vagrant-vbguest
```

