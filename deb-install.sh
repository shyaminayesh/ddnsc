#!/usr/bin/env bash
# Purpose: Script to install ddnsc on Debian systems. 
# 	This will most likely work on Ubuntu, but it has not been tested yet.
# Maintainer: jahway603

PKGNAME="ddnsc"
CONF_FILE="$PKGNAME.conf"

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run with sudo or as root. Try again." 
   exit 1
fi

echo ""
echo "checking ddnsc dependencies & installing missing ones..."
echo ""
REQUIRED_PKG_0="python3"
REQUIRED_PKG_1="python3-systemd"
REQUIRED_PKG_2="python3-requests"
REQUIRED_PKG_3="python-is-python3"

PKG_OK_0=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG_0 | grep "install ok installed")
echo Checking for $REQUIRED_PKG_0: $PKG_OK_0
if [ "" = "$PKG_OK_0" ]; then
  echo "No $REQUIRED_PKG_0. Setting up $REQUIRED_PKG_0."
  apt-get --yes install $REQUIRED_PKG_0
fi

PKG_OK_1=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG_1 | grep "install ok installed")
echo Checking for $REQUIRED_PKG_1: $PKG_OK_1
if [ "" = "$PKG_OK_1" ]; then
  echo "No $REQUIRED_PKG_1. Setting up $REQUIRED_PKG_1."
  apt-get --yes install $REQUIRED_PKG_1
fi

PKG_OK_2=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG_2 | grep "install ok installed")
echo Checking for $REQUIRED_PKG_2: $PKG_OK_2
if [ "" = "$PKG_OK_2" ]; then
  echo "No $REQUIRED_PKG_2. Setting up $REQUIRED_PKG_2."
  apt-get --yes install $REQUIRED_PKG_2
fi

PKG_OK_3=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG_3 | grep "install ok installed")
echo Checking for $REQUIRED_PKG_3: $PKG_OK_3
if [ "" = "$PKG_OK_3" ]; then
  echo "No $REQUIRED_PKG_3. Setting up $REQUIRED_PKG_3."
  apt-get --yes install $REQUIRED_PKG_3
fi

echo ""
echo "ddnsc dependencies are now installed"
echo "Continuing with ddnsc installation."
echo ""

# backup config file if it currently exists
if [ -f "/etc/$PKGNAME/$CONF_FILE" ]
then
    echo "Backing up current $CONF_FILE"
    mv /etc/$PKGNAME/$CONF_FILE /etc/$PKGNAME/$CONF_FILE.backup
	echo ""
fi

# create necessary directories on system
install -d /usr/share/$PKGNAME
install -d /etc/$PKGNAME

# install main application
cp $PKGNAME.py /usr/share/$PKGNAME/

# Copy required files
cp -r plugins /usr/share/$PKGNAME/
cp -r helpers /usr/share/$PKGNAME/

# Copy config file
install -Dm600 .configs/ddnsc.conf /etc/$PKGNAME/$CONF_FILE

# Copy SERVICE ( systemd )
install -D .configs/ddnsc.service /usr/lib/systemd/system/$PKGNAME.service

echo ""
echo "Install for $PKGNAME is now complete on your Debian system. Enjoy."
