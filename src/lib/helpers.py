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

def display_log_y_checkbox(key, label="Log Y Scale"):
    if not key in st.session_state:
        st.session_state[key] = False

    st.checkbox(label, key=key, value=st.session_state[key])

def display_newlines(num_newlines):
    for i in range(num_newlines):
        st.text("")