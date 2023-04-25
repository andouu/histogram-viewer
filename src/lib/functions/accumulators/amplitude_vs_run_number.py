import streamlit as st
import pandas as pd
import altair as alt

from ...accumulator import SelectorAccumulator
from ..selectors.amplitude_vs_run_number import AmplitudeVsRunNumberSelector

class AmplitudeVsRunNumberAccumulator(SelectorAccumulator):
    name = "Amplitude vs Run Number"

    def _set_result(self):
        for selector in self.selectors:
            x, y = selector.get_xy()
            self.x.append(x)
            self.y.append(y)

        bar_chart = alt.Chart(self._data_as_dataframe()).mark_bar().encode(
            y="Amplitude",
            x="Run"
        )
        self._result = lambda: st.altair_chart(bar_chart, use_container_width=True)

    def on_start(self):
        pass

    def on_process(self):
        pass

    def on_complete(self):
        pass

    def _data_as_dataframe(self):
        return pd.DataFrame({
            "Amplitude": self.x,
            "Run": self.y
        })
    
    def _t_files_as_selectors(self, t_files, run_list):
        return [AmplitudeVsRunNumberSelector(t_file, run[0]) for t_file, run in zip(t_files, run_list)]