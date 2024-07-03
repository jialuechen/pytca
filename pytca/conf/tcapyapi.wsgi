# preferred to use apache/gunicorn (easier to support Python 3) instead of apache/wsgi (more for Python 2)

# if we need to run apache/wsgi for Python 3, then needs some patching of mod_wsgi
# as suggested in http://devmartin.com/blog/2015/02/how-to-deploy-a-python3-wsgi-application-with-apache2-and-debian/

import os
import sys

try:
    pytca_cuemacro = os.environ['pytca_CUEMACRO']
    python_home = os.environ['pytca_PYTHON_ENV']
except:
    user_home = os.environ['USER']

    # if pytca_CUEMACRO not set globally (or the Python environment for pytca), we need to specify it here
    pytca_cuemacro = '/home/' + user_home + '/cuemacro/'
    python_home = '/home/' + user_home + '/py36tca/'

activate_this = python_home + '/bin/activate_this.py'

execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, pytca_cuemacro)
# os.chdir(pytca_cuemacro+ '/pytcapro/vis/')

from pytcapro.api.app_api import server as application
application.root_path = pytca_cuemacro + '/pytcapro/api/'