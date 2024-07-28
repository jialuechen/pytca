#!/bin/bash

export SCRIPT_FOLDER="$( dirname "$(readlink -f -- "$0")" )"
export SCRIPT_FOLDER="$( dirname "$(readlink -f -- "$SCRIPT_FOLDER")" )"
source $SCRIPT_FOLDER/batch_scripts/linux/installation/set_pytca_env_vars.sh
source $SCRIPT_FOLDER/batch_scripts/linux/installation/activate_python_environment.sh

echo 'Batch folder' $SCRIPT_FOLDER
echo ' pytca' $pytca_

# pytest | tee pytca_pytest.log

py.test --cov-report term-missing --cov pytca --verbose | tee pytest.log

# | tee pytest.log

# if we want to run tests for a particular file we can do this
# pytest -v /home/pytcauser//pytca/tests/test_pytca/test_data_read_write.py

#      #- ./test:/pytca/test