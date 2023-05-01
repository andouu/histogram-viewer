import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

from itertools import chain
from ...accumulator import SelectorAccumulator
from ..selectors.q_vs_run_number import QvsRunNumberSelector

class QvsRunNumberAccumulator(SelectorAccumulator):
    name = "Q vs Run Number"

    def _set_result(self):
        for selector in self.selectors:
            x, y = selector.get_xy()
            self.x.append(x)
            self.y.append(y)

        bar_chart = alt.Chart(self._data_as_dataframe()).mark_circle().encode(
            y="Q (MeV):Q",
            x="Run:N",
            color="Channel:N",
        )
        #bar_chart.configure_header()
        self._result = lambda: st.altair_chart(bar_chart, use_container_width=True)

    def on_start(self):
        pass

    def on_process(self):
        pass

    def on_complete(self):
        pass
    
    def _data_as_dataframe(self):
        return pd.DataFrame({
            "Q (MeV)": list(chain(*self.y)),
            "Channel": ["Channel 1", "Channel 3"] * len(self.y),
            "Run": np.repeat(self.x, 2)
        })
    
    def _t_files_as_selectors(self, t_files, run_list):
        return [QvsRunNumberSelector(t_file, run[0]) for t_file, run in zip(t_files, run_list)]