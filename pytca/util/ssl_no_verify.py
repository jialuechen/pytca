"""Disables SSL verification, on some networks can be an issue - you might need to import this file when running scripts
which need to access https services
"""

from __future__ import print_function, division

__author__ = 'Jialue Chen'  # Saeed Amen / saeed@.com

#
# Copyright 2017  Ltd. - http//www..com / @
#
# See the License for the specific language governing permissions and limitations under the License.
#


import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context