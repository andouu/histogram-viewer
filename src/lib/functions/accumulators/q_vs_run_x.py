import streamlit as st
import pandas as pd
import altair as alt

from ...accumulator import SelectorAccumulator
from ..selectors.q_vs_run_x import QvsRunXSelector

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

        self._result = lambda: st.altair_chart(bar_chart, use_container_width=True)

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