# TRO Load System Guide

## Steps to upgrade Test and Prod environments to a new version.

### Hide the existing version:

`cd ~/test/troload`

`mkdir .old`

`mv * .old`


### Use the standard auto-update to download and install the latest version from github:

`export ENVIRONMENT=devl`

`. ~/.bash_profile`

`auto-update -e test -a troload`


