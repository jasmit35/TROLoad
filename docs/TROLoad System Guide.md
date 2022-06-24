# TRO Load System Guide

## Deploying a new release to Test
**If FireStarter has not been updated to specify a release, stage the desired release in the /tmp directory before running auto_update. Then be sure to select the option to use the existing tar file.**

```
cd /tmp
git clone https://github.com/jasmit35/TROLoad.git --branch release/v1.0.0
```
### Hide the existing version:

```
cd ~/test/troload
mkdir .old_2022_06_23
mv * .old_2022_06_23
```

### Clean up any older versions:

```
cd ~/test/troload
ll
rm -rf .old_2021*
```

### Use auto-update to install the new release:

```
export ENVIRONMENT=test
auto-update -e test -a troload
```
### Update .db_secrets.env
The secrets files are not stored on GitHub because the contain user names and passwords. You need to manually copy the files:

```
cd /Users/jeff/test/TROLoad/local/etc
cp /Users/jeff/devl/TROLoad/local/etc/.db_secrets.env .
```



