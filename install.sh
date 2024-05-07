#!/bin/bash
#
# This file installes the application from the working directory to the system
# file system. It will also install python dependencies and create a tar ball. 
# This file is inteded to be used during development.
#
# Author: Lowkey 
# Email: public3838@bahnhof.se
# Licese: GPLv3
# Version: 1.0
#

# Detect different Linux distributions to be able to install differently as 
# needed. CURRENTLY NOT USED. REDHAT/FEDORA is assumed.
if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
elif [ -f /etc/fedora-release ]; then
    # Older Fedora ...
    OS=Fedora
    VER=$(cat /etc/fedora-release)
elif type lsb_release >/dev/null 2>&1; then
    # linuxbase.org
    OS=$(lsb_release -si)
    VER=$(lsb_release -sr)
elif [ -f /etc/lsb-release ]; then
    # For some versions of Debian/Ubuntu without lsb_release command
    . /etc/lsb-release
    OS=$DISTRIB_ID
    VER=$DISTRIB_RELEASE
elif [ -f /etc/debian_version ]; then
    # Older Debian/Ubuntu/etc.
    OS=Debian
    VER=$(cat /etc/debian_version)
# elif [ -f /etc/SuSe-release ]; then
#     # Older SuSE/etc.
#     ...
# elif [ -f /etc/redhat-release ]; then
#     # Older Red Hat, CentOS, etc.
#     ...
else
    # Fall back to uname, e.g. "Linux <version>", also works for BSD, etc.
    OS=$(uname -s)
    VER=$(uname -r)
fi

# Inform user
echo "$OS"
echo "$VER"
echo "Installing lsusbblk"

# Install dependencies
sudo dnf install python3-colorama
sudo dnf install python3-pyudev
sudo dnf install python3-pyusb

# Install manpages 
/usr/bin/gzip -v -c lsusbblk.1 > lsusbblk.1.gz
sudo /usr/bin/install -v -m 644 -o root -g root lsusbblk.1.gz /usr/share/man/man1/

# Insall application and set permissions
sudo /usr/bin/mkdir -v -p /usr/share/lsusbblk/lib
sudo /usr/bin/chown -v -R root:root /usr/share/lsusbblk
sudo /usr/bin/chmod -v -R 755 /usr/share/lsusbblk 
sudo /usr/bin/install -v -m 644 -o root -g root lib/* /usr/share/lsusbblk/lib
sudo /usr/bin/install -v -m 755 -o root -g root lsusbblk /usr/share/lsusbblk/

# Create /usr/bin logical link
sudo /bin/ln -v -f -s /usr/share/lsusbblk/lsusbblk /usr/bin/lsusbblk

# Create tar ball
/bin/tar cvzf lsusbblk.gz install_lsusbblk.sh lsusbblk lib/__init__.py lib/classutil.py lib/confutil.py lib/formatutil.py lib/usbblk.py 

echo "Installation complete"
