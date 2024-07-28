# preferred to use apache/gunicorn (easier to support Python 3) instead of apache/wsgi (more for Python 2)

# if we need to run apache/wsgi for Python 3, then needs some patching of mod_wsgi
# as suggested in http://devmartin.com/blog/2015/02/how-to-deploy-a-python3-wsgi-application-with-apache2-and-debian/

import os
import sys

try:
    pytca_ = os.environ['pytca_']
    python_home = os.environ['pytca_PYTHON_ENV']
except:
    user_home = os.environ['USER']

    # if pytca_ not set globally (or the Python environment for pytca), we need to specify it here
    pytca_ = '/home/' + user_home + '//'
    python_home = '/home/' + user_home + '/py36tca/'

activate_this = python_home + '/bin/activate_this.py'

execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, pytca_)
# os.chdir(pytca_+ '/pytcapro/vis/')

from pytca.vis.app import server as application
application.root_path = pytca_ + '/pytca/vis/'