import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ROOT import TFile
from .run import Run

# ================================================================================================
# Helper Functions
# -----

def q_branch_to_dataframe(t_tree):
    measurements = []
    for entry in t_tree:
        measurements.append(entry.Q[0])

    return pd.DataFrame({ "charges": measurements })

# ================================================================================================
# Plotting Functions
# -----

def root_th1fs_to_plotly_histogram(run: Run, log_y: bool = False):
    t_file = TFile.Open(run.path, "r")
    data_tree = t_file.Get("T")
    dataframe = q_branch_to_dataframe(data_tree)
    
    run_number = run.run_number
    data_range = (-10, -0.1) if run_number < 670 else (-50, 0)
    return px.histogram(
        dataframe[dataframe.charges.between(left=data_range[0], right=data_range[1])],
        x="charges",
        log_y=log_y,
        title=run.name
    )

# ================================================================================================