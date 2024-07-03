import os
import sys

pytca_home = os.environ['pytca_CUEMACRO']

sys.path.insert(0, pytca_home)
# os.chdir(user_home + '/cuemacro/pytca/pytcapro/vis/')

from pytca.vis.app_board import server as application
application.root_path = pytca_home  + '/pytca/vis/'