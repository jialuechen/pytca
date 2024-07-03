#!/bin/bash

export SCRIPT_FOLDER="$( dirname "$(readlink -f -- "$0")" )"
source $SCRIPT_FOLDER/installation/set_pytca_env_vars.sh

sudo killall influxd
sudo influxd -config $pytca_CUEMACRO/pytca/conf/influxdb.conf