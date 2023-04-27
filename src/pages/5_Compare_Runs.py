import streamlit as st

from lib.files import get_default_root_files
from lib.helpers import display_side_by_side_selects, display_channel_selector, display_checkbox
from lib.plot import plot_run_overlay

root_files = get_default_root_files()

with st.sidebar:
    display_side_by_side_selects(
        left_select_kwargs={
            "label": "Run 1",
            "key": "compare_view_run_1_select",
            "options": root_files,
            "format_func": lambda data: data[0]
        },
        right_select_kwargs={
            "label": "Run 2",
            "key": "compare_view_run_2_select",
            "options": root_files,
            "index": len(root_files) - 1,
            "format_func": lambda data: data[0]
        }
    )
    channels, plot_title = display_channel_selector(
        display_mode_select_key="compare_view_channel_display_select",
        single_select_key="compare_view_single_channel_select",
        range_from_select_key="compare_view_channel_range_from_select",
        range_to_select_key="compare_view_channel_range_to_select",
        multiselect_key="compare_view_channel_multiselect",
    )
    display_checkbox(key="compare_view_log_y_checkbox", label="Log Y Scale", default=True)
    display_checkbox(key="compare_view_translucent_bars_checkbox", label="Translucent Bars", default=True)

selected_run_1 = st.session_state["compare_view_run_1_select"]
selected_run_2 = st.session_state["compare_view_run_2_select"]

st.markdown(f"""
    # Comparing {selected_run_1[0]} and {selected_run_2[0]}
""")

overlay = plot_run_overlay(
    selected_run_1,
    selected_run_2,
    channels=channels,
    channels_string=plot_title,
    log_y=st.session_state["compare_view_log_y_checkbox"],
    translucent_bars=st.session_state["compare_view_translucent_bars_checkbox"]
)
st.plotly_chart(overlay, use_container_width=True)