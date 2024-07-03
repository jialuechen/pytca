#!/bin/bash

# This file with create a virtual environment for Python3 which can be specifically used with pytca, so it does not
# impact other Python applications on the server

export SCRIPT_FOLDER="$( dirname "$(readlink -f -- "$0")" )"
source $SCRIPT_FOLDER/set_pytca_env_vars.sh

if [ $pytca_PYTHON_ENV_TYPE == "virtualenv" ]; then
    if [ $pytca_PYTHON_VERSION == 3 ]; then
        echo 'Creating Python3 virtualenv...'
        sudo pip3 install virtualenv
        virtualenv -p /usr/bin/python3 $pytca_PYTHON_ENV
    fi

    source $pytca_PYTHON_ENV_BIN/activate
elif [ $pytca_PYTHON_ENV_TYPE == "conda" ]; then
    echo 'Creating Python3 conda...'
    source $CONDA_ACTIVATE

    # Can be quite slow to update conda (also latest versions can have issues!)
    conda update -n base conda --yes
    conda remove --name $pytca_PYTHON_ENV --all --yes

    if [ $CONDA_FROM_YAML == 1 ]; then
        source $pytca_CUEMACRO/batch_scripts/linux/installation/install_conda_from_env_yaml.sh
        source activate $pytca_PYTHON_ENV
    elif [ $CONDA_FROM_YAML == 0 ]; then
        # Sometimes might help to try an older version of conda - https://github.com/conda/conda/issues/9004
        # conda install conda=4.6.14
        conda create -n $pytca_PYTHON_ENV python=3.7 --yes
    fi

    source activate $pytca_PYTHON_ENV
fi