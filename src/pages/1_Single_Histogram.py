import streamlit as st

from lib.plot import root_th1fs_to_plotly_histogram
from lib.files import get_default_root_files
from lib.helpers import display_channel_selector, display_graph_checkboxes

root_files = get_default_root_files()
root_files.sort(key=lambda data: data[1])

with st.sidebar:
    st.header("Single Histogram View")
    st.selectbox(
        "Histogram",
        key="single_histogram_select",
        options=root_files,
        format_func=lambda data: data[0],
    )
    channels, plot_title = display_channel_selector(
        display_mode_select_key="single_histogram_channel_display_select",
        single_select_key="single_histogram_single_channel_select",
        range_from_select_key="single_histogram_channel_range_from_select",
        range_to_select_key="single_histogram_channel_range_to_select",
        multiselect_key="single_histogram_channel_multiselect",
    )
    display_graph_checkboxes(
        log_y_checkbox_key="single_view_log_y_checkbox",
        translucent_bars_checkbox_key="single_view_translucent_bars_checkbox",
        superpose_channels_checkbox_key="single_view_superpose_channels_checkbox",
        translucent_bars_checkbox_default=True
    )

with st.container():
    if "single_histogram_select" in st.session_state:
        root_file_data = st.session_state["single_histogram_select"]
        run_name = root_file_data[0]
        file_url = root_file_data[1]

        histogram = root_th1fs_to_plotly_histogram(
            file_url,
            plot_title=plot_title,
            channels=channels,
            log_y=st.session_state["single_view_log_y_checkbox"],
            translucent_bars=st.session_state["single_view_translucent_bars_checkbox"],
            superpose_channels=st.session_state["single_view_superpose_channels_checkbox"]
        )
    elif len(root_files) > 0:
        run_name = root_files[0][0]
        file_url = root_files[0][1]
        histogram = root_th1fs_to_plotly_histogram(
            file_url,
            plot_title=plot_title,
            channels=channels,
            log_y=st.session_state["single_view_log_y_checkbox"],
            translucent_bars=st.session_state["single_view_translucent_bars_checkbox"],
            superpose_channels=st.session_state["single_view_superpose_channels_checkbox"]
        )
        st.session_state["single_histogram_select"] = root_files[0]

    st.markdown("# Displaying " + run_name)
    st.plotly_chart(histogram, use_container_width=True)