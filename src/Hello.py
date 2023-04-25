# written by Andrew Zhou

import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    """
    # :wave: Hello!
    This is custom histogram viewer.

    There are 4 modes:
    - Single: Displays a single histogram
    - Range: Displays a range of histograms
    - Select: Displays a user selection of histograms
    - Function: Graphs a user-defined Y against a selection of runs
    """
)