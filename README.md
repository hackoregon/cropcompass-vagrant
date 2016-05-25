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

## Starting the development server
1. `vagrant ssh`. This will log you into the box as "vagrant"
2. `source ~/cropcompass/bin/activate`. This will activate the virtual environment
3. ``cd /vagrant/cropcompass`. This will put you in the server directory
4. `python manange.py runserver 0.0.0.0:8000`. This will start the development server listening on port 8000.
5. Browse to <http://localhost:8000>.
