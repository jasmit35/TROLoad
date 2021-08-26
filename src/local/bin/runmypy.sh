#!/bin/bash
#
#  runmypy.sh - This script is used to configure the Python virtual environment and
#               execute a Python script from cron.
#
#  Split the first parameter (python script location)
the_dir=$(dirname ${1})
the_script=$(basename ${1})

#  Activate the projects virtual environment
export PATH=$HOME/.pyenv/bin:$PATH
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

python_dir="$HOME/dbsec/local/python"
export PYTHONPATH=$PYTHONPATH:${python_dir}

cd ${the_dir}

#  Run the script with parameters passed to this script minus the first one
shift
python ${the_script} ${*}
