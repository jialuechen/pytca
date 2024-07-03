#!/bin/bash

# Starts the pytca web application
# 1) gets pytca enviroment variables
# 2) kills existing pytca processes (celery, gunicorn etc.)
# 3) activates pytca Python environment
# 4) starts gunicorn (if necessary)
# 5) restarts web server (Apache or Nginx)
# 6) clears Redis cache
# 7) starts celery for batch processing of TCA requests

# Note that on some instances of Linux this may not fetch the required directory (it has been tested with RedHat)
export SCRIPT_FOLDER="$( dirname "$(readlink -f -- "$0")" )"
source $SCRIPT_FOLDER/installation/set_pytca_env_vars.sh

# Set Python environment
source $SCRIPT_FOLDER/installation/activate_python_environment.sh

echo 'Batch folder' $SCRIPT_FOLDER
echo 'Cuemacro pytca' $pytca_CUEMACRO

# Kill all Python and Celery process and stop webserver
echo 'Killing any existing Python and celery processes...'
# sudo killall python
sudo killall celery
sudo killall gunicorn
sudo killall httpd
sudo killall apache2

# Make sure permissions set properly
sudo setenforce 0

# Create log folder (if it doesn't exist already)
mkdir -p $pytca_CUEMACRO/log/

# To run tests
mkdir -p /tmp/pytca
mkdir -p /tmp/csv

if [ $pytca_PYTHON_STARTER == "gunicorn" ]; then
    echo 'Start Gunicorn to interact with Flask/Dash app'

    # Always start default 'pytca' web interface
    gunicorn --bind 127.0.0.1:8090 --workers 4 --threads 6 --preload --chdir $pytca_CUEMACRO/pytca/conf/ \
    --access-logfile $pytca_CUEMACRO/log/gunicorn_pytca_access.log \
    --error-logfile $pytca_CUEMACRO/log/gunicorn_pytca_error.log \
    --log-level DEBUG \
    pytca_wsgi:application &

    # Start 'pytca' RESTful API
    if [ $START_pytca_API == 1 ]; then
        echo 'Start Gunicorn for RESTful API...'
        gunicorn --bind 127.0.0.1:8091 --workers 4 --threads 6 --preload --chdir $pytca_CUEMACRO/pytca/conf/ \
        --access-logfile $pytca_CUEMACRO/log/gunicorn_pytca_access.log \
        --error-logfile $pytca_CUEMACRO/log/gunicorn_pytca_error.log \
        --log-level DEBUG \
        pytcaapi_wsgi:application &

    fi

    # Start 'pytcaboard' web interface
    if [ $START_pytca_BOARD == 1 ]; then
        echo 'Start Gunicorn for pytcaboard...'
        gunicorn --bind 127.0.0.1:8092 --workers 4 --threads 6 --preload --chdir $pytca_CUEMACRO/pytca/conf/ \
        --access-logfile $pytca_CUEMACRO/log/gunicorn_pytca_access.log \
        --error-logfile $pytca_CUEMACRO/log/gunicorn_pytca_error.log \
        --log-level DEBUG \
        pytcaboard_wsgi:application &

    fi

    # (We can add many different additional gunicorn instances here here too)

    # --log-file $pytca_CUEMACRO/log/gunicorn_pytca.log \
    # --log-level DEBUG \&
elif [ $pytca_PYTHON_STARTER == "mod_wsgi" ]; then
    echo 'Using mod_wsgi to interact with Flask/Dash app (make sure paths are set in pytca.wsgi are set correctly before installation)'
fi

echo 'Python is ' $pytca_PYTHON_ENV

echo 'Restarting webserver...' $pytca_WEB_SERVER

# Restart webserver
if [ $DISTRO == "ubuntu" ]; then
    if [ "$pytca_WEB_SERVER" == "apache" ]; then
        sudo service nginx stop
        sudo service apache2 restart
    elif [ "$pytca_WEB_SERVER" == "nginx" ]; then
        sudo service apache2 stop
        sudo service nginx restart
    fi

elif [ $DISTRO == "redhat"  ]; then
    if [ "$pytca_WEB_SERVER" == "apache" ]; then
        sudo service nginx stop
        sudo service httpd restart
    elif [ "$pytca_WEB_SERVER" == "nginx" ]; then
        sudo service httpd stop
        sudo service nginx restart
    fi
fi

echo 'Flush Celery cache...'

# Purge every message from the "celery" queue everything on celery (not strcitly necessary if using Redis, as flushing in next line)
# celery purge -f

# Flush redis of everything in cache (saved dataframes and message queue)
echo 'Flushing Redis cache...'

redis-cli flushall

echo 'Current working folder (set to notebook folder by default - so works with test trade files)'
cd $pytca_CUEMACRO/pytca_notebooks
echo $PWD

echo 'About to start celery...'
celery -A pytca.conf.celery_calls worker --purge --discard --loglevel=debug -Q celery --concurrency=$pytca_CELERY_WORKERS -f $pytca_CUEMACRO/log/celery.log &