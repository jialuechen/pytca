#!/bin/bash

# script for starting plotly orca server, needs to start it via xvfb-run

export SCRIPT_FOLDER="$( dirname "$(readlink -f -- "$0")" )"
source $SCRIPT_FOLDER/installation/set_pytca_env_vars.sh

xvfb-run -a $pytca_CUEMACRO/pytca/orca-1.2.1-x86_64.AppImage "$@"