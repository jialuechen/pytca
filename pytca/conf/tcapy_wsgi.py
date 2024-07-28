import os
import sys

pytca_home = os.environ['pytca_']

sys.path.insert(0, pytca_home)
# os.chdir(user_home + '//pytca/pytcapro/vis/')

from pytca.vis.app import server as application
application.root_path = pytca_home  + '/pytca/vis/'