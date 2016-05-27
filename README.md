# HackOregon Crop Compass Vagrant Environment

0. Find a place with wall power and reliable network connectivity.
1. Install git, Vagrant and VirtualBox on your host machine.
2. Open a host command window and do

    ```
    git clone git@github.com:hackoregon/cropcompass-vagrant
    cd cropcompass-vagrant
    git checkout django-offline
    ```
3. On Windows, do `.\build.bat`. On MacOS or Linux, do `./build.bat`.

This will take some time. If anything croaks, do a `vagrant ssh`. You can see all the log files in `~/logs`.

When the scripts finish, the Crop Compass Django app will be running. Browse to <http://localhost:8000> to test it.

To check whether the server is running, type `vagrant global-status` on the host. To stop the server, type `vagrant halt`. To start it again type `vagrant reload`.

## Troubleshooting
1. `vagrant ssh`. This will log you into the box as "vagrant".
2. `workon cropcompass`. This will activate the Crop Compass virtual environment.
3. The log files are in `~/logs`.
