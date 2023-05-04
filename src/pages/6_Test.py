import streamlit as st

from lib.files import ROOT_FILES_DIR, root_files_to_runs
from lib.plot import run_overlay_plot
from lib.helpers import display_graph_checkboxes

TEST_PATH_1 = ROOT_FILES_DIR + "2"
TEST_PATH_2 = ROOT_FILES_DIR + "3"
TEST_PATH_3 = ROOT_FILES_DIR + "4"
TEST_PATH_4 = ROOT_FILES_DIR + "5"
TEST_PATH_5 = ROOT_FILES_DIR + "6"

rf_1 = root_files_to_runs()
rf_2 = root_files_to_runs(TEST_PATH_1)
rf_3 = root_files_to_runs(TEST_PATH_2)
rf_4 = root_files_to_runs(TEST_PATH_3)
rf_5 = root_files_to_runs(TEST_PATH_4)
rf_6 = root_files_to_runs(TEST_PATH_5)

st.set_page_config(layout="wide")

with st.sidebar:
    display_graph_checkboxes(
        log_y_checkbox_key="test_view_log_y_checkbox",
        translucent_bars_checkbox_key="test_view_translucent_bars_checkbox",
        translucent_bars_checkbox_default=True,
        show_superpose_channels_checkbox=False
    )

st.header("Different Integration Windows")

which_run = 1
for i in [1, 3]:
    st.plotly_chart(
        run_overlay_plot(
            [rf_1[which_run], rf_3[which_run], rf_4[which_run], rf_5[which_run], rf_6[which_run]],
            set([i]),
            f"Channel {i}",
            log_y=st.session_state["test_view_log_y_checkbox"],
            translucent_bars=st.session_state["test_view_translucent_bars_checkbox"],
        ),
        use_container_width=True
    )