import streamlit as st

from math import ceil

def calculate_number_of_rows(num_columns, num_elements):
    return ceil(num_elements / num_columns)

def display_grid(num_columns, elements, render_func, reverse_order = False, debug = False):
    num_rows = calculate_number_of_rows(num_columns, len(elements))
    index_count = len(elements) - 1 if reverse_order else 0

    if debug: _display_debug_element(reverse_order, len(elements), num_rows, num_columns)

    for i in range(0, num_rows):
        column_indexes = [index_count - j if reverse_order else index_count + j for j in range(0, num_columns)]
        with st.container():
            columns_and_indexes = zip(st.columns(num_columns), column_indexes)
            for (column, index) in columns_and_indexes:
                if index < 0 or index >= len(elements):
                    continue

                render_func(column, elements, index)

        if reverse_order:
            index_count -= num_columns
        else:
            index_count += num_columns

def _display_debug_element(reverse_order, num_elements, num_rows, num_columns):
    with st.expander("Debug Details"):
        st.write("Reverse Order: " + "True" if reverse_order else "False")
        st.write("Num of Elements: " + str(num_elements))
        st.write("Number of Rows: " + str(num_rows))
        st.write("Number of Columns: " + str(num_columns))

def display_checkbox(key, label, default = False, **kwargs):
    if not key in st.session_state:
        st.session_state[key] = default

    st.checkbox(label, key=key, value=st.session_state[key], **kwargs)

def display_newlines(num_newlines):
    for i in range(num_newlines):
        st.text("")

def display_range_select(from_select_kwargs, to_select_kwargs):
    col_1, col_2 = st.columns(2)

    with col_1:
        st.selectbox(**from_select_kwargs)

    with col_2:
        st.selectbox(**to_select_kwargs)

def display_channel_selector(
    display_mode_select_key: str,
    single_select_key: str,
    range_from_select_key: str,
    range_to_select_key: str,
    multiselect_key: str,
    label: str = "Channel Display"
):
    st.selectbox(
        label,
        key=display_mode_select_key,
        options=["all", "single", "range", "custom"],
        index=3,
        format_func=lambda option: option.capitalize()
    )
    match st.session_state[display_mode_select_key]:
        case "all":
            pass
        case "single":
            st.selectbox(
                "Channel",
                key=single_select_key,
                options=list(range(0, 16)),
                index=1
            )
        case "range":
            display_range_select(
                from_select_kwargs={
                    "label": "From",
                    "key": range_from_select_key,
                    "options": list(range(0, 16)),
                    "index": 1
                },
                to_select_kwargs={
                    "label": "To",
                    "key": range_to_select_key,
                    "options": list(range(0, 16)),
                    "index": 3
                }
            )
        case "custom":
            st.multiselect(
                "Channels",
                key=multiselect_key,
                options=list(range(0, 16)),
                default=[1, 3],
                format_func=lambda channel_num: "Channel " + str(channel_num)
            )

    match st.session_state[display_mode_select_key]:
        case "all":
            channels = set(range(0, 16))
            plot_title = "Channels 0 - 16"
        case "single":
            selected_channel = st.session_state[single_select_key]
            channels = set([selected_channel])
            plot_title = "Channel " + str(selected_channel)
        case "range":
            bound_1 = st.session_state[range_from_select_key]
            bound_2 = st.session_state[range_to_select_key]
            channels = sorted(set(range(bound_1, bound_2)))
            plot_title = f"Channels {min(bound_1, bound_2)} - {max(bound_1, bound_2)}"
        case "custom":
            channels = sorted(set(st.session_state[multiselect_key]))
            plot_title = "Channels " + ", ".join([str(channel) for channel in sorted(channels)])
        case _:
            channels = set()
            plot_title = "Unknown"
    
    return (channels, plot_title)