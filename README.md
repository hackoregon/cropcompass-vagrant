# HackOregon Crop Compass Vagrant Environment

0. Find a place with wall power and reliable network connectivity.
1. Install git, Vagrant and VirtualBox on your host machine.
2. Open a host command window and do

    ```
    git clone git@github.com:hackoregon/cropcompass-vagrant
    cd cropcompass-vagrant
    git checkout master
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

## Working on the Django code
The Django code lives online in the GitHub repo <https://github.com/hackoregon/cropcompass-django>. During the provisioning step a `git clone` fetches this to `~vagrant`, where the nginx / uWSGI configuration expects to find it. As part of this process, the static files are collected.

If you need to work on the Django code inside the box, do the following:

1. If you're not in the `Crop Compass` team on GitHub, have someone add you to that team.
2. `vagrant ssh` into the running box. Then type `workon cropcompass`. Tab completion works here.
3. Browse to <http://localhost:8000> and verify the API is listening to you.
4. Identify yourself to Git if you plan to branch / commit / push changes:

    * git config --global user.email "you@example.com"
    * git config --global user.name "Your Name"

5. Do your thing, using the browser to verify your changes. You might have to restart nginx: `sudo service nginx restart`.
    If you need to re-collect the static files, do `cd ~/cropcompass; python3 manage.py collectstatic`.
6. The repo was cloned via the HTTPS endpoint. To push your changes, you'll need to enter your GitHub ID and GitHub password. If you have two-factor enabled, you'll probably need your 2FA device handy.
