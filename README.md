# HackOregon Crop Compass Vagrant Environment

0. Find a place with wall power and reliable network connectivity.
1. Install git, Vagrant and VirtualBox on your host machine.
2. Open a host command window and do

    ```
    git clone git@github.com:hackoregon/cropcompass-vagrant
    cd cropcompass-vagrant
    git checkout fixissue3
    ```
3. On Windows, do `.\build.bat`. On MacOS or Linux, do `./build.bat`.

This will take some time. If anything croaks, do a `vagrant ssh`. You can see all the log files in `~/logs`.

When the scripts finish, the Crop Compass Django app will be running. Browse to `localhost:8000` to test it.

To check whether the server is running, type `vagrant global-status` on the host. To stop the server, type `vagrant halt`. To start it again type `vagrant reload`.

## Troubleshooting
1. `vagrant ssh`. This will log you into the box as "vagrant".
2. `workon cropcompass`. This will activate the Crop Compass virtual environment.
3. The log files are in `~/logs`.

## Working on the Django code
First of all, Vagrant mounts the host `cropcompass-vagrant` Git repository (where the Vagrantfile lives) onto `/vagrant` in the guest. So you can change files in the repository or in the guest and they'll be changed in both places. Of course, you can only interact with GitHub from the host.

Second, during the provisioning, the script that installs Django copies the Django API code from `/vagrant/cropcompass` to `/home/vagrant/cropcompass`. The server points to this copy!

So if you want to work on the Django code:
1. `sudo service nginx stop`. This will stop the server.
2. `workon cropcompass`. This will activate the Python virtualenv.
3. Go into `/vagrant/cropcompass`. As noted above, this is mirrored on the host.
4. `./manage.py runserver 0.0.0.0:8000 &`. This will start a development server. Browse to `localhost:8000` to see your results.
5. Work on the Django code. When you have the results you want, do the following:
    1. Stop the development server: `kill -TERM %1`.
    2. Back up and replace the Django code the server is using:
    ```
    cd ~vagrant
    rm -fr cropcompass.bak; mv cropcompass cropcompass.bak
    cp -rp /vagrant/cropcompass ~vagrant
    ```
    3. Restart the server: `sudo service nginx start`.
6. On the host, do your Git operations for the modified code.
