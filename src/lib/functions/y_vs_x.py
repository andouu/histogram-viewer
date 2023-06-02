import os
import streamlit as st
import pandas as pd
import plotly.express as px

from ROOT import TFile
from typing import Callable, Any
from multiprocessing import current_process
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from .graph_function import GraphingFunction, Selector, AltairDataType
from ..run import Run
from ..fit import get_peaks

def get_q(*, t_file, run: Run):
    return get_peaks(t_file, run)

def get_run_name(*, t_file, run: Run):
    return run.name

# =====================================================================

def get_xy(
    get_x: Callable[[TFile, Run], Any],
    get_y: Callable[[TFile, Run], Any],
    t_file: TFile,
    run: Run
):
    return (get_x(t_file=t_file, run=run), get_y(t_file=t_file, run=run))

class AnyXAnyY(GraphingFunction):
    name = "Custom Y vs X"
    functions: list[Selector] = [
        Selector(
            name="Q",
            func=get_q,
        ),
        Selector(
            name="Run Name",
            func=get_run_name,
        )
    ]

    def __init__(self):
        super().__init__()
        self._update_funcs()
        self.invalid_points = {}

    def _update_funcs(self):
        if not current_process().name == "MainProcess":
            return
        
        if "any_x_any_y_select_x" not in st.session_state:
            st.session_state["any_x_any_y_select_x"] = self.functions[1]
        if "any_x_any_y_select_y" not in st.session_state:
            st.session_state["any_x_any_y_select_y"] = self.functions[0]

        self.x_func = st.session_state["any_x_any_y_select_x"]
        self.y_func = st.session_state["any_x_any_y_select_y"]
        self.get_x = self.x_func.func
        self.get_y = self.y_func.func

    def _swap_funcs(self):
        tmp = self.x_func
        self.x_func = self.y_func
        self.y_func = tmp

        st.session_state["any_x_any_y_select_x"] = self.x_func
        st.session_state["any_x_any_y_select_y"] = self.y_func

    def sidebar(self):
        self._update_funcs()

        col_1, col_2 = st.columns(2)

        with col_1:
            st.selectbox(
                key="any_x_any_y_select_y",
                label="Y Variable",
                options=self.functions,
                format_func=lambda func: func.name,
                on_change=self._update_funcs
            )

        with col_2:
            st.selectbox(
                key="any_x_any_y_select_x",
                label="X Variable",
                options=self.functions,
                format_func=lambda func: func.name,
                on_change=self._update_funcs
            )

        st.button(label="Swap Axes", on_click=self._swap_funcs)

    def _multiprocess_runs(self, runs: list[Run]):
        results = []
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = []
            for run in runs:
                t_file = TFile.Open(run.path, "r")

                future = executor.submit(get_xy, self.get_x, self.get_y, t_file, run)
                futures.append(future)

                t_file.Close()
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except BrokenProcessPool as err:
                    raise Exception(err)
        return results
    
    def _prune_data(self) -> None:
        indices_to_delete = []
        x_axis_name = self.x_func.name
        y_axis_name = self.y_func.name
        self.invalid_points = { x_axis_name: [], y_axis_name: [] }

        for i, data_point in enumerate(zip(self.x, self.y)):
            x, y = data_point
            if x is None or y is None:
                self.invalid_points[x_axis_name].append(x)
                self.invalid_points[y_axis_name].append(y)
                indices_to_delete.append(i)

        indices_to_delete.sort(reverse=True)
        for index in indices_to_delete:
            del self.x[index]
            del self.y[index]

    def accumulate(self, runs):
        MULTIPROCESS = False
        self._update_funcs()

        if MULTIPROCESS:

            self.runs = runs
            self.on_start()

            results = self._multiprocess_runs(runs)

            x, y = (data for data in zip(*results))
            self.x = x
            self.y = y

            self.on_end()
        else:
            super().accumulate(runs)
        
        self._prune_data()

    def data_as_dataframe(self):
        def _match(x, y):
            valid_list_like_classes = (list, set, tuple)

            x_is_list_like = isinstance(x, valid_list_like_classes)
            y_is_list_like = isinstance(y, valid_list_like_classes)

            x_len = len(x) if x_is_list_like else 1
            y_len = len(y) if y_is_list_like else 1

            x_values = list(x) * y_len if x_is_list_like else [x] * y_len
            y_values = list(y) * x_len if y_is_list_like else [y] * x_len

            return (x_values, y_values)

        x_func_name = self.x_func.name
        y_func_name = self.y_func.name
        
        data = {
            x_func_name: [],
            y_func_name: [],
            "Crystal Type": []
        }

        # Only write run name if it's not already one of the axes
        write_run_name = "Run Name" not in data
        if write_run_name:
            data["Run Name"] = []

        for x, y, run in zip(self.x, self.y, self.runs):
            formatted_x, formatted_y = _match(x, y)

            data[x_func_name].extend(formatted_x)
            data[y_func_name].extend(formatted_y)
            if write_run_name:
                data["Run Name"].extend([run.name] * (len(formatted_x) + len(formatted_y)))

            data["Crystal Type"].extend([run.crystal_type.value] * len(formatted_x))

        return pd.DataFrame(data)

    def graph(self):
        dataframe = self.data_as_dataframe()

        x_func_name = self.x_func.name
        y_func_name = self.y_func.name
        
        scatter_plot = px.scatter(dataframe, x=x_func_name, y=y_func_name, color="Run Name", symbol="Crystal Type")

        with st.container():
            st.plotly_chart(scatter_plot, use_container_width=True)
            if len(self.invalid_points.keys()) > 0:
                first_key = next(iter(self.invalid_points))
                num_invalid_points = len(self.invalid_points[first_key])
                st.text(f"There was a problem fitting {num_invalid_points} points.")

                df = pd.DataFrame(self.invalid_points)
                df.index.name = "Invalid Points"
                st.dataframe(df, use_container_width=True)
