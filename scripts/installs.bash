#!/bin/bash

sudo apt-get update
sudo apt-get install -y \
  apt-file \
  gunicorn3 \
  python3-django \
  python3-gunicorn
sudo apt-file update
