import streamlit as st

from lib.plot import root_th1fs_to_plotly_histogram
from lib.files import root_files_to_runs
from lib.helpers import display_graph_checkboxes
from lib.run import Run

runs = root_files_to_runs()

st.set_page_config(layout="wide")

with st.sidebar:
    st.header("Single Histogram View")
    st.selectbox(
        "Histogram",
        key="single_histogram_select",
        options=runs,
        format_func=lambda run: run.name,
    )
    display_graph_checkboxes(log_y_checkbox_key="single_view_log_y_checkbox")

with st.container():
    if "single_histogram_select" in st.session_state:
        run: Run = st.session_state["single_histogram_select"]
        histogram = root_th1fs_to_plotly_histogram(run, st.session_state["single_view_log_y_checkbox"])
    elif len(runs) > 0:
        run: Run = runs[0]
        histogram = root_th1fs_to_plotly_histogram(run)
        st.session_state["single_histogram_select"] = run

    st.markdown("# Displaying " + run.name)
    st.plotly_chart(histogram, use_container_width=True)