#!/bin/bash

export SCRIPT_FOLDER="$( dirname "$(readlink -f -- "$0")" )"
source $SCRIPT_FOLDER/installation/set_pytca_env_vars.sh

# set Python environment
source $SCRIPT_FOLDER/installation/activate_python_environment.sh

# run python scripts in pytca
python $pytca_CUEMACRO/pytca_scripts/gen/volatile_market_trade_data_gen.py