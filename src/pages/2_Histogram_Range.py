import streamlit as st

from lib.files import root_files_to_runs
from lib.plot import root_th1fs_to_plotly_histogram
from lib.helpers import display_grid, display_side_by_side_selects, display_graph_checkboxes

runs = root_files_to_runs()

st.set_page_config(layout="wide")

def handle_flip_range():
    tmp = st.session_state["histogram_range_from_select"]
    st.session_state["histogram_range_from_select"] = st.session_state["histogram_range_to_select"]
    st.session_state["histogram_range_to_select"] = tmp

with st.sidebar:
    st.header("Range of Histograms View")
    display_side_by_side_selects(
        left_select_kwargs={
            "label": "From",
            "key": "histogram_range_from_select",
            "options": runs,
            "format_func": lambda run: run.name
        },
        right_select_kwargs={
            "label": "To",
            "key": "histogram_range_to_select",
            "options": runs,
            "index": min(len(runs) - 1, 5),
            "format_func": lambda run: run.name
        }
    )
    st.button(
        "Flip Range",
        key="range_view_range_flip_button",
        on_click=handle_flip_range
    )
    display_graph_checkboxes(log_y_checkbox_key="range_view_log_y_checkbox")
    st.number_input(
        "Columns",
        key="range_view_columns_input",
        min_value=1,
        step=1,
    )

histogram_range = (st.session_state["histogram_range_from_select"], st.session_state["histogram_range_to_select"])
st.markdown(f"# Displaying from {histogram_range[0].name} to {histogram_range[1].name}")

range_start_index = runs.index(histogram_range[0])
range_end_index = runs.index(histogram_range[1])

num_columns = st.session_state["range_view_columns_input"]

display_elements = map(
    lambda run: root_th1fs_to_plotly_histogram(run, log_y=st.session_state["range_view_log_y_checkbox"]),
    runs[min(range_start_index, range_end_index) : max(range_start_index, range_end_index) + 1]
)
reverse_order = range_end_index < range_start_index
with st.spinner("Loading Histograms..."):
    display_grid(
        num_columns,
        list(display_elements),
        lambda column, elements, index: column.plotly_chart(elements[index], use_container_width=True),
        reverse_order,
    )