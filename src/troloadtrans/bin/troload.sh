#!/bin/bash
set -euo pipefail

home_dir=$(dirname ${0})
home_dir=${home_dir%%'/bin'}
cd ${home_dir}

the_app=$(cat .python-version)

the_script=$(basename ${0})
the_script=${the_script%%'.sh'}.py

#  Run the script with parameters passed to this script
export PYENV_ROOT=$HOME/.pyenv
${PYENV_ROOT}/versions/${the_app}/bin/python python/${the_script} ${*}
