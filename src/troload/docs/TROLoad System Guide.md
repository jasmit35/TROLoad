# TRO Load System Guide


## Deploying a new release to Prod
**If FireStarter has not been updated to specify a release, stage the desired release in the /tmp directory before running auto_update. Then be sure to select the option to use the existing tar file.**

```
cd /tmp
git clone https://github.com/jasmit35/TROLoad.git --branch release/v1.0.0
```

### Archive the existing version:

```
cd ~/prod/
tar -czvf TROLoad_2022_06_26.tar.gz TROLoad
```

### Clean up any much older archives and the current version:

```
cd ~/prod/
ll
rm TROLoad_2021*
rm -rf TROLoad
```

### Use auto-update to install the new release:

```
export ENVIRONMENT=prod
auto-update -e prod -a troload
```
### Update .db_secrets.env
The secrets files are not stored on GitHub because the contain user names and passwords. You need to manually copy the files:

```
cd /Users/jeff/prod/TROLoad/local/etc
cp /Users/jeff/devl/TROLoad/local/etc/.db_secrets.env .
```



# Requirements.txt
