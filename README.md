# HackOregon Crop Compass Vagrant Environment

0. Find a place with wall power and reliable network connectivity.
1. Install git, Vagrant and VirtualBox on your host machine.
2. If you need to make changes to the code, you'll need SSH keys on Github. See <https://help.github.com/categories/ssh/> for the setup details. Then, open a host command window and do

    ```
    git clone git@github.com:hackoregon/cropcompass-vagrant
    cd cropcompass-vagrant
    git checkout fixprovisionerrors
    ```
    
    If you don't need to make changes to the repo, clone it with 

    ```
    git clone https://github.com/hackoregon/cropcompass-vagrant
    ```
    
    Note that on Windows, some versions of Git will convert the line endings of text files from Unix (LF only) to DOS/Windows (CR-LF) format. If your Git does this, the Vagrant provisioning step will die a horrible death. I'm looking for an in-Vagrant fix, but meanwhile, make sure your Git is configured to not modify any line endings.
3. On Windows, do `.\build.bat`. On MacOS or Linux, do `./build.bat`.

This will take some time. If anything croaks, do a `vagrant ssh`. You can see all the log files in `~/logs`.

When the scripts finish, the Crop Compass Django app will be running. Browse to <http://localhost:8000> to test it. Also, do a `vagrant ssh`. The first time, you will see

```
$ vagrant ssh
Welcome to Ubuntu 14.04.4 LTS (GNU/Linux 3.13.0-86-generic x86_64)

 * Documentation:  https://help.ubuntu.com/

  System information as of Sat May 28 00:19:48 UTC 2016

  System load:  0.97              Processes:           82
  Usage of /:   3.5% of 39.34GB   Users logged in:     0
  Memory usage: 12%               IP address for eth0: 10.0.2.15
  Swap usage:   0%

  Graph this data and manage this system at:
    https://landscape.canonical.com/

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

0 packages can be updated.
0 updates are security updates.


virtualenvwrapper.user_scripts creating /home/vagrant/Env/premkproject
virtualenvwrapper.user_scripts creating /home/vagrant/Env/postmkproject
virtualenvwrapper.user_scripts creating /home/vagrant/Env/initialize
virtualenvwrapper.user_scripts creating /home/vagrant/Env/premkvirtualenv
virtualenvwrapper.user_scripts creating /home/vagrant/Env/postmkvirtualenv
virtualenvwrapper.user_scripts creating /home/vagrant/Env/prermvirtualenv
virtualenvwrapper.user_scripts creating /home/vagrant/Env/postrmvirtualenv
virtualenvwrapper.user_scripts creating /home/vagrant/Env/predeactivate
virtualenvwrapper.user_scripts creating /home/vagrant/Env/postdeactivate
virtualenvwrapper.user_scripts creating /home/vagrant/Env/preactivate
virtualenvwrapper.user_scripts creating /home/vagrant/Env/postactivate
virtualenvwrapper.user_scripts creating /home/vagrant/Env/get_env_details
vagrant@ubuntu:~$ 
```

The `virtualenvwrapper` lines will only appear the first time you `vagrant ssh` into the box. There is only one Python virtual environment - to activate it type `workon cropcompass`. See <https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-14-04> for the details on the nginx / uWSGI configuration if you need to change anything.

To check whether the server is running, type `vagrant global-status` on the host. To stop the server, type `vagrant halt`. To start it again type `vagrant reload`.

## Troubleshooting
1. `vagrant ssh`. This will log you into the box as "vagrant".
2. `workon cropcompass`. This will activate the Crop Compass virtual environment.
3. The log files are in `~/logs`.

## Host-side troubleshooting
Do a `vagrant global-status`. This will list all the boxes and what they're doing. Note that if a box is running when you reboot your host, Vagrant may or may not save it cleanly and may or may not restart it when the host comes back up. On my Linux host it does seem to do a clean save and restore, but to be safe you should do a `vagrant halt` before shutting down the host and a `vagrant up` after bringing the host back up.
