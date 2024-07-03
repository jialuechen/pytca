#!/bin/bash

export SCRIPT_FOLDER="$( dirname "$(readlink -f -- "$0")" )"
source $SCRIPT_FOLDER/installation/set_pytca_env_vars.sh

# Celery log
tail -f $pytca_CUEMACRO/log/mongo.log ---disable-inotify