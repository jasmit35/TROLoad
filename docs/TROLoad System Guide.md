# TRO Load System Guide

## Deploying a release

### Pre-deployment check

Check that all the code in the development environment has been checked into GitHub.

Make sure the docker image has been recorded:

    * troloadbank - 2025.1.0)
    * troloadtrans -
    * trload???? -

and pushed to PyPi.

Make sure all of the severs in the target swarm have the /Volume/synology_nfs directory available. If not go to the instructions for the hardware and get it set up.

### Deployment

Use the ansible script to perform the deployment.

```
cd ~/devl/troload/ansible
```




```
make PLAYBOOK=deploy HOSTS=test_swarm, run-on-hosts

```














