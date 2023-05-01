import streamlit as st

from lib.files import get_default_root_files
from lib.plot import root_th1fs_to_plotly_histogram
from lib.helpers import display_grid, display_side_by_side_selects, display_channel_selector, display_graph_checkboxes

root_files = get_default_root_files()

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
            "options": root_files,
            "format_func": lambda data: data[0]
        },
        right_select_kwargs={
            "label": "To",
            "key": "histogram_range_to_select",
            "options": root_files,
            "index": len(root_files) - 1,
            "format_func": lambda data: data[0]
        }
    )
    st.button(
        "Flip Range",
        key="range_view_range_flip_button",
        on_click=handle_flip_range
    )
    channels, plot_title = display_channel_selector(
        display_mode_select_key="histogram_range_channel_display_select",
        single_select_key="histogram_range_single_channel_select",
        range_from_select_key="histogram_range_channel_range_from_select",
        range_to_select_key="histogram_range_channel_range_to_select",
        multiselect_key="histogram_range_channel_multiselect",
    )
    display_graph_checkboxes(
        log_y_checkbox_key="range_view_log_y_checkbox",
        translucent_bars_checkbox_key="range_view_translucent_bars_checkbox",
        superpose_channels_checkbox_key="range_view_superpose_channels_checkbox",
        translucent_bars_checkbox_default=True
    )
    st.number_input(
        "Columns",
        key="range_view_columns_input",
        min_value=1,
        step=1,
    )

histogram_range = (st.session_state["histogram_range_from_select"], st.session_state["histogram_range_to_select"])
st.markdown(f"# Displaying from {histogram_range[0][0]} to {histogram_range[1][0]}")

range_start_index = root_files.index(histogram_range[0])
range_end_index = root_files.index(histogram_range[1])

num_columns = st.session_state["range_view_columns_input"]

display_elements = map(
    lambda data: root_th1fs_to_plotly_histogram(
        data[1],
        plot_title=f"{data[0]} ({plot_title})",
        channels=channels,
        log_y=st.session_state["range_view_log_y_checkbox"],
        translucent_bars=st.session_state["range_view_translucent_bars_checkbox"],
        superpose_channels=st.session_state["range_view_superpose_channels_checkbox"]
    ),
    root_files[min(range_start_index, range_end_index) : max(range_start_index, range_end_index) + 1]
)
reverse_order = range_end_index < range_start_index
with st.spinner("Loading Histograms..."):
    display_grid(
        num_columns,
        list(display_elements),
        lambda column, elements, index: column.plotly_chart(elements[index], use_container_width=True),
        reverse_order,
    )