import streamlit as st

from lib.files import root_files_to_runs
from lib.plot import root_th1fs_to_plotly_histogram
from lib.helpers import display_grid, display_channel_selector, display_graph_checkboxes
from lib.run import Run

runs = root_files_to_runs()

st.set_page_config(layout="wide")

with st.sidebar:
    st.header("Select Histogram View")
    st.multiselect(
        "Select",
        key="select_view_select",
        options=runs,
        format_func=lambda run: run.name,
    )
    channels, plot_title = display_channel_selector(
        display_mode_select_key="select_view_channel_display_select",
        single_select_key="select_view_single_channel_select",
        range_from_select_key="select_view_channel_range_from_select",
        range_to_select_key="select_view_channel_range_to_select",
        multiselect_key="select_view_channel_multiselect",
    )
    display_graph_checkboxes(
        log_y_checkbox_key="select_view_log_y_checkbox",
        translucent_bars_checkbox_key="select_view_translucent_bars_checkbox",
        superpose_channels_checkbox_key="select_view_superpose_channels_checkbox",
        translucent_bars_checkbox_default=True
    )
    st.number_input(
        "Columns",
        key="select_view_columns_select",
        min_value=1,
        step=1,
    )

selected_runs: list[Run] = st.session_state["select_view_select"]

displayed_runs = map(
    lambda data: root_th1fs_to_plotly_histogram(data, log_y=st.session_state["select_view_log_y_checkbox"]),
    selected_runs
)
display_elements = list(displayed_runs)

num_displayed_runs = len(display_elements)
if num_displayed_runs == 0:
    st.markdown("# No Runs Selected")
elif num_displayed_runs == 1:
    st.markdown(f"# Displaying {selected_runs[0].name}")
elif num_displayed_runs < 3:
    display_string = ", ".join([run.name for run in selected_runs])
    st.markdown("# Displaying " + display_string)
else:
    display_string = ", ".join([run.name for run in selected_runs][0 : 2]) + f", (+ {len(selected_runs) - 2} more)"
    st.markdown("# Displaying " + display_string)

with st.spinner("Loading Histograms..."):
    display_grid(
        st.session_state["select_view_columns_select"],
        display_elements,
        lambda column, elements, index: column.plotly_chart(elements[index], use_container_width=True),
    )