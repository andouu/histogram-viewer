import streamlit as st

from lib.files import get_default_root_files
from lib.plot import root_th1f_to_plotly_histogram
from lib.helpers import display_grid, display_log_y_checkbox

root_files = get_default_root_files()

with st.sidebar:
    st.header("Select Histogram View")
    st.multiselect(
        "Select",
        key="select_view_select",
        options=root_files,
        format_func=lambda data: data[0],
    )
    display_log_y_checkbox(key="select_view_log_y_checkbox")
    st.number_input(
        "Columns",
        key="select_view_columns_select",
        min_value=1,
        step=1,
    )

runs = st.session_state["select_view_select"]

displayed_runs = map(
    lambda data: root_th1f_to_plotly_histogram(data[1], "hCharge", data[0], log_y=st.session_state["select_view_log_y_checkbox"]),
    runs
)
display_elements = list(displayed_runs)

num_displayed_runs = len(display_elements)
if num_displayed_runs == 0:
    st.markdown("# No Runs Selected")
elif num_displayed_runs == 1:
    st.markdown(f"# Displaying {runs[0][0]}")
elif num_displayed_runs < 3:
    display_string = ", ".join([run[0] for run in runs])
    st.markdown("# Displaying " + display_string)
else:
    display_string = ", ".join([run[0] for run in runs][0 : 2]) + f", (+ {len(runs) - 2} more)"
    st.markdown("# Displaying " + display_string)

with st.spinner("Loading Histograms..."):
    display_grid(
        st.session_state["select_view_columns_select"],
        display_elements,
        lambda column, elements, index: column.plotly_chart(elements[index], use_container_width=True),
    )