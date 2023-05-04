# written by Andrew Zhou

import streamlit as st

from lib.helpers import display_uw_logo

st.set_page_config(layout="wide")
display_uw_logo()

st.markdown(
    """
    # :wave: Hello!
    This is custom histogram viewer.

    There are 5 modes:
    - Single: Displays a single histogram
    - Range: Displays a range of histograms
    - Select: Displays a user selection of histograms
    - Function: Executes user-defined functions against a selection of runs
    - Compare: Overlays two runs over each other
    
    Docs can be found at https://to-be-implemented.com
    """
)