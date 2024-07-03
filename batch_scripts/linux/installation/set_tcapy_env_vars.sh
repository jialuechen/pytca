#!/bin/bash

# This script has various configuration flags for pytca which need to be set
# It is unlikely you'll need to change many of these (except possibly the folder where pytca resides)

echo "Setting environment variables for pytca for current script (recommended to add these globally to /etc/environment)"

## Python environment settings #########################################################################################

# Folder where pytca is (note: if you will need to change this in pytca/conf/mongo.conf too)
export pytca_CUEMACRO=/home/$USER/cuemacro/pytca

# Is the Python environment either "conda" or "virtualenv"?
export pytca_PYTHON_ENV_TYPE="conda"
# export pytca_PYTHON_ENV=/home/$USER/py37tca/ # virtualenv folder or conda name
export pytca_PYTHON_ENV=py37tca # virtualenv folder or conda name
export pytca_PYTHON_ENV_BIN=/home/$USER/$pytca_PYTHON_ENV/bin/
export pytca_PYTHON_VERSION=3 # Only Python 3 is now supported

export CONDA_ACTIVATE=/home/$USER/anaconda3/bin/activate
export pytca_USER=$USER # which user to run pytca

export pytca_CELERY_WORKERS=14

# Add Anaconda to the path (you might need to change this)
# export PATH=~/anaconda3/bin:$PATH

## Database settings ###################################################################################################

export START_MYSQL=1
export START_MONGODB=1
export START_CLICKHOUSE=1

## Web server settings #################################################################################################

# Can use gunicorn with either apache or nginx (mod_wsgi can only be used with apache and is depreciated)
# recommended to use gunicorn with nginx
export pytca_PYTHON_STARTER='gunicorn' # 'gunicorn' ('mod_wsgi' is deprecated)
export pytca_WEB_SERVER="nginx" # apache or nginx

# Start other web interfaces? (we always start the default pytca web interface server)
# but we can also add other interfaces if we want
export START_pytca_API=1        # Start Gunicorn RESTful API
export START_pytca_BOARD=1      # Start Gunicorn pytcaboard web front-end

## Installation parameters #############################################################################################

export CONDA_FROM_YAML=1 # Install tca py37tca environment from environment_py37tca.yml
export COMPILE_REDIS_FROM_SOURCE=0 # Compiling from source is slower, instead we use Chris Rea's repo version of Redis

## Get Linux distribution ##############################################################################################

# Determine OS distribution
case "`/usr/bin/lsb_release -si`" in
  Ubuntu) export DISTRO="ubuntu" ;;
       *) export DISTRO="redhat"
esac

