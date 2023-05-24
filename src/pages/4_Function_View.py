import streamlit as st

from lib.files import root_files_to_runs
from lib.helpers import display_newlines, display_side_by_side_selects
from lib.functions.graph_function import GraphingFunction
from lib.functions.y_vs_x import AnyXAnyY
from lib.run import Run

runs = root_files_to_runs()

def get_available_functions() -> list[GraphingFunction]:
    return [
        AnyXAnyY(),
    ]

functions = get_available_functions()

def get_runs_to_analyze():
    match st.session_state["function_view_display_select"]:
        case "all":
            runs_to_analyze = runs
        case "single":
            runs_to_analyze = [st.session_state["function_view_single_histogram_select"]]
        case "range":
            selected_runs = (st.session_state["function_view_range_from_select"], st.session_state["function_view_range_to_select"])
            selected_run_indices = tuple(runs.index(run) for run in selected_runs)

            start_index = min(selected_run_indices)
            end_index = max(selected_run_indices)

            runs_to_analyze = runs[start_index : end_index + 1]
        case "select":
            runs_to_analyze = st.session_state["function_view_select_histograms_select"]
        case other:
            raise ValueError(f"Display Type {other} is not valid!")
    return runs_to_analyze

def set_updated_state(new_value):
    st.session_state["function_view_changed"] = new_value

def run():
    set_updated_state(False)

    runs_to_analyze = get_runs_to_analyze()

    selected_function: GraphingFunction = st.session_state["function_view_select"]
    selected_function.accumulate(runs_to_analyze)

    graph = selected_function.graph if selected_function.graph is not None else None
    st.session_state["function_view_analysis_graph"] = graph

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    with st.sidebar:
        st.selectbox(
            "Runs",
            key="function_view_display_select",
            options=["all", "single", "range", "select"],
            format_func=lambda option: option.capitalize(),
            on_change=lambda: set_updated_state(True)
        )

        match st.session_state["function_view_display_select"]:
            case "all":
                pass
            case "single":
                st.selectbox(
                    "Run",
                    key="function_view_single_histogram_select",
                    options=runs,
                    format_func=lambda run: run.name,
                    on_change=lambda: set_updated_state(True)
                )
            case "range":
                display_side_by_side_selects(
                    left_select_kwargs={
                        "label": "From",
                        "key": "function_view_range_from_select",
                        "options": runs,
                        "format_func": lambda run: run.name,
                        "on_change": lambda: set_updated_state(True)
                    },
                    right_select_kwargs={
                        "label": "To",
                        "key": "function_view_range_to_select",
                        "options": runs,
                        "index": len(runs) - 1,
                        "format_func": lambda run: run.name,
                        "on_change": lambda: set_updated_state(True)
                    }
                )
            case "select":
                st.multiselect(
                    "Runs",
                    key="function_view_select_histograms_select",
                    options=runs,
                    format_func=lambda run: run.name,
                    on_change=lambda: set_updated_state(True)
                )
        st.selectbox(
            "function",
            key="function_view_select",
            options=functions,
            format_func=lambda accumulator: accumulator.name,
            on_change=lambda: set_updated_state(True)
        )
        if "function_view_changed" in st.session_state:
            if st.session_state["function_view_changed"]:
                st.text("Press run to update")
        st.session_state["function_view_select"].sidebar()
        st.button("Run", on_click=run)

    runs_to_analyze: list[Run] = get_runs_to_analyze()
    match st.session_state["function_view_display_select"]:
        case "all":
            analyzed_runs_text = "For all runs"
        case "single":
            analyzed_runs_text = "For " + runs_to_analyze[0].name
        case "range":
            analyzed_runs_text = f"From {runs_to_analyze[0].name} to {runs_to_analyze[-1].name}"
        case "select":
            num_runs_to_analyze = len(runs_to_analyze)
            if num_runs_to_analyze == 0:
                analyzed_runs_text = "For no runs?"
            else:
                analyzed_runs_text = "For " + "Run " if len(runs_to_analyze) == 1 else "Runs " + ", ".join([run.name for run in runs_to_analyze])

    st.markdown(f"""
        # Graphing {st.session_state["function_view_select"].name}
        ### {analyzed_runs_text}
    """)

    display_newlines(2)

    with st.empty():
        if "function_view_analysis_graph" in st.session_state:
            st.session_state["function_view_analysis_graph"]()