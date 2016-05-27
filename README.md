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

## Working on the Django code
The Django code lives online in the GitHub repo <https://github.com/hackoregon/cropcompass-django>. During the provisioning step a `git clone` fetches this to `~vagrant`, where the nginx / uWSGI configuration expects to find it. As part of this process, the static files are collected.

If you need to work on the Django code inside the box, do the following:
1. If you're not in the `Crop Compass` team on GitHub, have someone add you to that team.
2. `vagrant ssh` into the running box. Then type `workon cropcompass`. Tab completion works here.
3. Browse to <http://localhost:8000> and verify the API is listening to you.
4. Identify yourself to Git if you plan to branch / commit / push changes:
```
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```
5. Do your thing, using the browser to verify your changes. If you need to re-collect the static files, do `cd ~/cropcompass; python3 manage.py collectstatic`. You might have to restart `nginx`: `sudo service nginx restart`.
6. The repo was cloned via the HTTPS endpoint. To push your changes, you'll need to enter your GitHub ID and GitHub password.

