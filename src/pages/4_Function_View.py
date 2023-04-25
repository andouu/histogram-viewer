import streamlit as st

from ROOT import TFile
from lib.files import get_default_root_files
from lib.helpers import display_newlines
from lib.functions.accumulators.q_vs_run_number import QvsRunNumberAccumulator
from lib.functions.accumulators.amplitude_vs_run_number import AmplitudeVsRunNumberAccumulator

st.set_page_config(layout="wide")

root_files = get_default_root_files()

@st.cache_data
def get_available_functions():
    return [
        QvsRunNumberAccumulator(),
        AmplitudeVsRunNumberAccumulator(),
    ]

functions = get_available_functions()

def get_runs_to_analyze():
    match st.session_state["function_view_display_select"]:
        case "all":
            runs_to_analyze = root_files
        case "single":
            runs_to_analyze = [st.session_state["function_view_single_histogram_select"]]
        case "range":
            selected_runs = (st.session_state["function_view_range_from_select"], st.session_state["function_view_range_to_select"])
            selected_run_indices = tuple(root_files.index(run) for run in selected_runs)

            start_index = min(selected_run_indices)
            end_index = max(selected_run_indices)

            runs_to_analyze = root_files[start_index : end_index]
        case "select":
            runs_to_analyze = st.session_state["function_view_select_histograms_select"]
        case other:
            raise ValueError(f"Display Type {other} is not valid!")
    return runs_to_analyze

# selected_function_name = st.session_state["function_view_select"].name
# st.markdown(f"# Displaying {selected_function_name} for All Runs")

def run_accumulator():
    runs_to_analyze = get_runs_to_analyze()

    selected_accumulator = st.session_state["function_view_select"]
    selected_accumulator.accumulate(runs_to_analyze)

    st.session_state["function_view_analysis_result"] = selected_accumulator.get_result()

with st.sidebar:
    st.selectbox(
        "Runs",
        key="function_view_display_select",
        options=["all", "single", "range", "select"],
        format_func=lambda option: option.capitalize(),
    )

    match st.session_state["function_view_display_select"]:
        case "all":
            pass
        case "single":
            st.selectbox(
                "Run",
                key="function_view_single_histogram_select",
                options=root_files,
                format_func=lambda data: data[0],
            )
        case "range":
            st.selectbox(
                "From",
                key="function_view_range_from_select",
                options=root_files,
                format_func=lambda data: data[0],
            )
            st.selectbox(
                "To",
                key="function_view_range_to_select",
                options=root_files,
                index=len(root_files) - 1,
                format_func=lambda data: data[0],
            )
        case "select":
            st.multiselect(
                "Runs",
                key="function_view_select_histograms_select",
                options=root_files,
                format_func=lambda data: data[0],
            )

    st.selectbox(
        "function",
        key="function_view_select",
        options=functions,
        format_func=lambda accumulator: accumulator.name
    )
    st.button("Run", on_click=run_accumulator)

runs_to_analyze = get_runs_to_analyze()
match st.session_state["function_view_display_select"]:
    case "all":
        analyzed_runs_text = "For all runs"
    case "single":
        analyzed_runs_text = "For " + runs_to_analyze[0][0]
    case "range":
        analyzed_runs_text = f"From {runs_to_analyze[0][0]} to {runs_to_analyze[-1][0]}"
    case "select":
        num_runs_to_analyze = len(runs_to_analyze)
        if num_runs_to_analyze == 0:
            analyzed_runs_text = "For no runs?"
        else:
            analyzed_runs_text = "For " + "Run " if len(runs_to_analyze) == 1 else "Runs " + ", ".join([run[0] for run in runs_to_analyze])

st.markdown(f"""
    # Graphing {st.session_state["function_view_select"].name}
    ### {analyzed_runs_text}
""")

display_newlines(2)

with st.empty():
    if "function_view_analysis_result" in st.session_state:
        st.session_state["function_view_analysis_result"]()