import streamlit as st

from lib.plot import root_th1f_to_plotly_histogram
from lib.files import get_default_root_files
from lib.helpers import display_log_y_checkbox

root_files = get_default_root_files()
root_files.sort(key=lambda data: data[1])

# st.set_page_config(layout="centered")

with st.sidebar:
    st.header("Single Histogram View")
    st.selectbox(
        "Histogram",
        key="single_histogram_select",
        options=root_files,
        format_func=lambda data: data[0],
    )
    display_log_y_checkbox(key="single_view_log_y_checkbox")

with st.container():
    if "single_histogram_select" in st.session_state:
        root_file_data = st.session_state["single_histogram_select"]
        run_name = root_file_data[0]
        file_url = root_file_data[1]

        histogram = root_th1f_to_plotly_histogram(file_url, "hCharge", run_name, log_y=st.session_state["single_view_log_y_checkbox"])
    elif len(root_files) > 0:
        run_name = root_files[0][0]
        file_url = root_files[0][1]
        histogram = root_th1f_to_plotly_histogram(file_url, "hCharge", run_name, log_y=st.session_state["single_view_log_y_checkbox"])
        st.session_state["single_histogram_select"] = root_files[0]

    st.markdown("# Displaying " + run_name)
    st.plotly_chart(histogram, use_container_width=True)