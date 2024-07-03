#!/bin/bash

# Demonstrates how to run a Python script in the Python environment setup for pytca (usually Anaconda)

export SCRIPT_FOLDER="$( dirname "$(readlink -f -- "$0")" )"
source $SCRIPT_FOLDER/installation/set_pytca_env_vars.sh

# set Python environment
source $SCRIPT_FOLDER/installation/activate_python_environment.sh

# Python command (add you python command here)
python $pytca_CUEMACRO/pytca/pytca_scripts/gen/dump_ncfx_to_csv.py