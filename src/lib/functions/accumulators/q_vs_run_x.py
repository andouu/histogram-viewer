import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
import plotly.figure_factory as ff

from ...accumulator import SelectorAccumulator
from ..selectors.q_vs_run_x import QvsRunXSelector
from ...plot import _root_charge_histogram_to_dataframe, root_th1fs_to_plotly_histogram

class QvsRunXAccumulator(SelectorAccumulator):
    name = "Q vs Run x"

    def _set_result(self):
        for selector in self.selectors:
            x, y = selector.get_xy()
            self.x.append(x)
            self.y.append(y)

        dataframe = self._data_as_dataframe()
        bar_chart = alt.Chart(dataframe, title="Q (a.u.) vs Run x").mark_circle().encode(
            y="Q:Q",
            x="Run x:Q",
            color="Run Name:N",
            tooltip=['Run Name', 'Channel', 'Run x', 'Q']
        )

        selector = self.selectors[0]
        channel_1_peak_1_range, channel_1_peak_2_range = selector.channel_1_peak_ranges
        channel_3_peak_1_range, channel_3_peak_2_range = selector.channel_3_peak_ranges

        t_file = selector.t_file

        channel_1_histogram = t_file.Get('channel_1_histogram')
        channel_3_histogram = t_file.Get('channel_3_histogram')

        channel_1_dataframe = _root_charge_histogram_to_dataframe(channel_1_histogram)
        channel_3_dataframe = _root_charge_histogram_to_dataframe(channel_3_histogram)

        peak_ranges_df = pd.concat([channel_1_dataframe, channel_3_dataframe])[
            channel_1_dataframe.x.between(left=channel_1_peak_1_range[0], right=channel_1_peak_1_range[1]) |
            channel_1_dataframe.x.between(left=channel_1_peak_2_range[0], right=channel_1_peak_2_range[1]) |
            channel_3_dataframe.x.between(left=channel_3_peak_1_range[0], right=channel_3_peak_1_range[1]) |
            channel_3_dataframe.x.between(left=channel_3_peak_2_range[0], right=channel_3_peak_2_range[1])
        ]

        run = self.run_list[0]
        channels_fig = root_th1fs_to_plotly_histogram(run[1], "Channels 1, 3", set([1, 3]))

        def _display_result():
            with st.container():
                st.altair_chart(bar_chart, use_container_width=True)
                st.plotly_chart(channels_fig.add_traces([
                    go.Bar(
                        x=peak_ranges_df["x"],
                        y=peak_ranges_df["y"],
                        name="Peak Fit Ranges"
                    ),
                ]), use_container_width=True)

        self._result = _display_result

    def on_start(self):
        pass

    def on_process(self):
        pass

    def on_complete(self):
        pass
    
    def _data_as_dataframe(self):
        data = {
            "Q": [],
            "Channel": [],
            "Run x": [],
            "Run Name": [],
        }
        for x, peaks in zip(self.x, self.y):
            channel_1_peaks = peaks["Channel 1"]
            channel_3_peaks = peaks["Channel 3"]

            data["Q"].extend(list(channel_1_peaks))
            data["Channel"].extend(["Channel 1", "Channel 1"])

            data["Q"].extend(list(channel_3_peaks))
            data["Channel"].extend(["Channel 3", "Channel 3"])

            run_x = x[0]
            data["Run x"].extend([run_x] * 4)

            run_name = x[1]
            data["Run Name"].extend([run_name] * 4)

        return pd.DataFrame(data)
    
    def _t_files_as_selectors(self, t_files, run_list):
        return [QvsRunXSelector(t_file, run[0]) for t_file, run in zip(t_files, run_list)]