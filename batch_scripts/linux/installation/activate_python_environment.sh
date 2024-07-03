#!/bin/bash

# This will activate our Python environment which has been created for pytca
export SCRIPT_FOLDER="$( dirname "$(readlink -f -- "$0")" )"

if [ -d "$SCRIPT_FOLDER/installation/" ]; then
    source $SCRIPT_FOLDER/installation/set_pytca_env_vars.sh
elif [ -d "$SCRIPT_FOLDER/" ]; then
    source $SCRIPT_FOLDER/set_pytca_env_vars.sh
fi

echo 'Activating Python environment' $pytca_PYTHON_ENV '... and adding pytca to PYTHONPATH' $pytca_CUEMACRO
export PYTHONPATH=$pytca_CUEMACRO/:$PYTHONPATH

if [ $pytca_PYTHON_ENV_TYPE == "conda" ]; then
    echo 'Python env type' $pytca_PYTHON_ENV_TYPE 'and' $CONDA_ACTIVATE
    source $CONDA_ACTIVATE
    source activate $pytca_PYTHON_ENV
elif [ $pytca_PYTHON_ENV_TYPE == "virtualenv" ]; then
    echo 'Python env type ' $pytca_PYTHON_ENV_TYPE
    source $pytca_PYTHON_ENV/bin/activate
fi