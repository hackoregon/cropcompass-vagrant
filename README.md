# HackOregon Crop Compass Vagrant Environment

0. Find a place with wall power and reliable network connectivity.
1. Install git, Vagrant and VirtualBox on your host machine.
2. If you need to make changes to the code, you'll need SSH keys on Github. See <https://help.github.com/categories/ssh/> for the setup details.

    Note that on Windows, some versions of Git will convert the line endings of text files from Unix (LF only) to DOS/Windows (CR-LF) format. If your Git does this, the Vagrant provisioning step will die a horrible death. Make sure your Git is configured to not modify any line endings.
3. If you don't need to make changes to the code, do

    ```
    git clone https://github.com/hackoregon/cropcompass-vagrant
    cd cropcompass-vagrant
    git checkout db20160609
    ```
    
    If you ***do*** need to make changes to the code, clone it with 
    ```
    git clone git@github.com:hackoregon/cropcompass-vagrant
    cd cropcompass-vagrant
    git checkout db20160609
    ```
    
3. On Windows, do `.\build.bat`. On MacOS or Linux, do `./build.bat`.

This will take some time. If anything croaks, do a `vagrant ssh`. You can see all the log files in `~/logs`.

When the scripts finish, the Crop Compass Django app will be running. Browse to <http://localhost:8000> to test it. Also, do a `vagrant ssh`. The first time, you will see

```
$ vagrant ssh

[ stuff deleted ]

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

To check whether the server is running, type `vagrant global-status` on the host. To stop the server, type `vagrant halt`. To start it again type `vagrant up`. To reboot it type `vagrant reload`.

## Operational notes
`vagrant global-status` will list all the boxes and what they're doing.

Note that if a box is running when you shut down or reboot your host, Vagrant may or may not save it cleanly and may or may not restart it when the host comes back up. To be safe, do a `vagrant halt` before shutting down or rebooting the host and a `vagrant up` after bringing the host back up.

## Troubleshooting
1. `vagrant ssh`. This will log you into the box as "vagrant".
2. `workon cropcompass`. This will activate the Crop Compass virtual environment.
3. The log files are in `~/logs`.
