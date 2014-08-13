#!/usr/bin/env bash

if [ "$(whoami)" != "root" ]; then
    echo "You must run this as root!"
    exit 1
fi

apt-get update
apt-get install -y libpq-dev python-dev git-core python-pip
pip install -r "/home/vagrant/boutique/requirements/development.txt"

echo " Finished."
