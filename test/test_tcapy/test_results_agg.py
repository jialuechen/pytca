"""Tests results aggregation methods, such as the histogram generator
"""

__author__ = 'Jialue Chen'  # Saeed Amen / saeed@.com

#
# Copyright 2017  Ltd. - http//www..com / @
#
# See the License for the specific language governing permissions and limitations under the License.
#

from pytca.conf.constants import Constants
from pytca.util.timeseries import RandomiseTimeSeries
from pytca.util.loggermanager import LoggerManager
from pytca.util.utilfunc import UtilFunc

from pytca.analysis.algos.resultssummary import ResultsSummary

from test.config import *

logger = LoggerManager().getLogger(__name__)

constants = Constants()
util_func = UtilFunc()

logger.info('Make sure you have created folder ' + constants.csv_folder + ' & ' + constants.temp_data_folder +
            ' otherwise tests will fail')

eps = 10 ** -5

def test_histogram_generator():
    """Test histogram generator for results - in particular for instances where we have only 1 point
    """

    results_summary = ResultsSummary()

    df = RandomiseTimeSeries().create_random_time_series(max_points=1000, freq='minute', start='01 Jan 2018', end="01 Jun 2018")

    df_hist, df_pdf = results_summary._create_histogram_distribution(df)

    assert df_pdf is not None

    df['Col'] = 'something'
    df['Col'][0] = 'something-else'

    df_hist_pdf = results_summary.field_distribution(df, aggregate_by_field='Col', metric_name='price')

    # Should only have output for 'something' because 'something-else' only has one point, so can't construct distribution from it
    assert len(df_hist_pdf.columns) == 3

    df = RandomiseTimeSeries().create_random_time_series(max_points=1, freq='minute', start='01 Jan 2018', end="01 Jun 2018")

    df_hist, df_pdf = results_summary._create_histogram_distribution(df)

    # Should have empty plots because only 1 point from these
    assert df_hist.empty and df_pdf.empty

def test_field_bucketing():
    """Tests field bucketing by a label
    """

    results_summary = ResultsSummary()

    df = RandomiseTimeSeries().create_random_time_series(max_points=1000, freq='minute', start='01 Jan 2018', end="01 Jun 2018")
    df['Col'] = 'something'

    df_fields = results_summary.field_bucketing(df, metric_name='price', aggregation_metric='sum', aggregate_by_field='Col')

    assert df_fields.values[0] - df_fields['Col'].sum() < eps

    # Overwrite first point
    df['Col'][0] = 'something-else'

    df_fields = results_summary.field_bucketing(df, metric_name='price', aggregation_metric='mean', aggregate_by_field='Col')

    # Check the averages match
    assert df_fields['Col']['something-else'] - df['price'][0] < eps
    assert df_fields['Col']['something'] - df['price'][1:].mean() < eps
