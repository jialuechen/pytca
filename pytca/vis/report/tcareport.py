from __future__ import print_function

__author__ = 'Jialue Chen'  # Saeed Amen / saeed@.com

#
# Copyright 2018  Ltd. - http//www..com / @
#
# See the License for the specific language governing permissions and limitations under the License.
#

from pytca.vis.report.computationreport import ComputationReport, JinjaRenderer

class TCAReport(ComputationReport):
    """Creates an HTML or PDF report from TCA results, which can be written to disk or returned as a string/binary
    for display elsewhere (eg. to be output by a webserver). Uses Renderer objects to write to HTML/convert to PDF.
    Preferred to use JinjaRender for TCAReport

    """

    def __init__(self, tca_results, title='TCA Report / generated by pytca', renderer=JinjaRenderer(), text_dict={}):
        super(TCAReport, self).__init__(tca_results, title=title, renderer=renderer)

        self._text_dict = text_dict

    def _layout_computation_results_to_html(self, embed_chart='offline_embed_js_div'):

        # Make sure to convert the dataframes into Plotly Figures first
        self._computation_results.render_computation_charts()

        tca_request = self._computation_request

        textpreamble_dict = {}
        charts_dict = {}
        text_dict = self._text_dict
        tables_dict = {}

        # Add some text at the beginning
        textpreamble_dict['Introduction'] = self._create_text_html(self._computation_results.text_preamble, add_hr=False)

        # Generate the HTML for all the sparse market charts
        charts_dict['Markets and trade/order charts'] = self._create_chart_html(self._computation_results.sparse_market_charts,
                                                      embed_chart=embed_chart)

        # Generate the HTML for all the timeline charts
        charts_dict['Timeline charts'] = self._create_chart_html(self._computation_results.timeline_charts, embed_chart=embed_chart)

        # Generate the HTML for all the bar charts
        charts_dict['Bar charts'] = self._create_chart_html(self._computation_results.bar_charts, embed_chart=embed_chart)

        # Generate the HTML for all the probability distribution charts
        charts_dict['PDF charts'] \
            = self._create_chart_html(self._computation_results.dist_charts, embed_chart=embed_chart)

        # Generate the HTML for all the scatter charts
        charts_dict['Scatter charts'] = self._create_chart_html(self._computation_results.scatter_charts, embed_chart=embed_chart)

        # Generate the HTML for all the scatter charts
        charts_dict['Heatmap charts'] = self._create_chart_html(self._computation_results.heatmap_charts, embed_chart=embed_chart)

        # Include the HTML for tables
        tables_dict['Tables'] = self._create_table_html(self._computation_results.styled_tables)

        # Create a summary of the parameters of the TCA request
        listpoints_dict = {}

        listpoints_dict['Ticker'] = self._create_text_html(self._util_func.pretty_str_list(tca_request.ticker), add_hr=False)
        listpoints_dict['Date'] = self._create_text_html(str(tca_request.start_date) + ' - ' + str(tca_request.finish_date), add_hr=False)

        if tca_request.metric_calcs is not None:
            if tca_request.metric_calcs != []:
                listpoints_dict['Metric'] = self._create_text_html(
                    self._util_func.pretty_str_list([m.get_metric_name().replace('_', ' ') for m in tca_request.metric_calcs]), add_hr=False)

        return {'text' : text_dict, 'charts' : charts_dict, 'tables' : tables_dict, 'textpreamble' : textpreamble_dict, 'listpoints' : listpoints_dict}
