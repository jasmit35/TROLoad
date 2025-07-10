#!/bin/bash

export app_name=troloadbank
export app_version=25.1.0.10

export app_home="/opt/app/troloadbank"
export app_nfs_home="/Volumes/synology_nfs/devl/troload"

docker run -d \
  --mount type=bind,source=${app_nfs_home}/logs,target=${app_home}/logs \
  --mount type=bind,source=${app_nfs_home}/reports,target=${app_home}/reports \
  --mount type=bind,source=${app_nfs_home}/stage,target=${app_home}/stage \
  jasmit/${app_name}:${app_version} -e devl

