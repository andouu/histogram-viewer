import streamlit as st

from math import ceil
from streamlit_extras.app_logo import add_logo
from streamlit_extras.let_it_rain import rain

def display_uw_logo():
    add_logo("assets/uw.png", height=110)

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
    for _ in range(num_newlines):
        st.text("")

def display_side_by_side_selects(left_select_kwargs, right_select_kwargs):
    col_1, col_2 = st.columns(2)

    with col_1:
        st.selectbox(**left_select_kwargs)

    with col_2:
        st.selectbox(**right_select_kwargs)

def display_graph_checkboxes(
    log_y_checkbox_key: str = "",
    log_y_checkbox_label: str = "Log y",
    log_y_checkbox_default: bool = False,
    show_log_y_checkbox: bool = True,
):
    if show_log_y_checkbox:
        display_checkbox(key=log_y_checkbox_key, label=log_y_checkbox_label, default=log_y_checkbox_default)