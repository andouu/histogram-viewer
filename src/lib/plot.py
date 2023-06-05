import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os
import json

from ROOT import TFile, TH1F
from .run import Run, CrystalType
from .path import get_file_stem

# ================================================================================================
# Helper Functions
# -----

with open("./config.json", "r") as config:
    data = json.load(config)
    CACHE_DIR = data["cacheDir"]

def _cache_t_file_path(t_file: TFile):
    return os.path.join(CACHE_DIR, f"{get_file_stem(t_file.GetName())}.root")

def _cache_df_file_path(t_file: TFile):
    return os.path.join(CACHE_DIR, f"{get_file_stem(t_file.GetName())}.parquet")

def _q_is_cached(t_file: TFile):
    t_file_exists = False
    df_cache_exists = False

    cache_t_file_path = _cache_t_file_path(t_file)
    if os.path.exists(cache_t_file_path) and os.path.isfile(cache_t_file_path):
        cache_file = TFile.Open(cache_t_file_path, "r")
        keys = [key.GetName() for key in cache_file.GetListOfKeys()]
        cache_file.Close()
        if "q_histogram" in keys:
            t_file_exists = True

    cache_df_file_path = _cache_df_file_path(t_file)
    if os.path.exists(cache_df_file_path) and os.path.isfile(cache_df_file_path):
        df_cache_exists = True

    return t_file_exists and df_cache_exists

def q_branch_to_dataframe(t_file: TFile, force_cache: bool = False):
    cache_t_file_path = _cache_t_file_path(t_file)

    cache_df_file_path = _cache_df_file_path(t_file)

    if not _q_is_cached(t_file) or force_cache:
        st.write(t_file.GetTitle())
        cache_file = TFile.Open(cache_t_file_path, "recreate")
        q_histogram = TH1F("q_histogram", "q_histogram", 256, -400, 400)

        measurements = []
        t_tree = t_file.Get("T")
        for entry in t_tree:
            q = entry.Q[0]
            q_histogram.Fill(q)
            measurements.append(q)

        q_histogram.Write()
        cache_file.Write()
        cache_file.Close()

        df = pd.DataFrame({ "charges": measurements })
        df.to_parquet(cache_df_file_path)

        return df
    else:        
        return pd.read_parquet(cache_df_file_path)

# ================================================================================================
# Plotting Functions
# -----

def root_th1fs_to_plotly_histogram(run: Run, log_y: bool = False, force_cache_data: bool = False):
    t_file = TFile.Open(run.path, "r")
    df = q_branch_to_dataframe(t_file, force_cache_data)
    data_range = (-10, -0.1) if run.crystal_type is CrystalType.Na22 else (-50, -0.1)
    df = df[df.charges.between(left=data_range[0], right=data_range[1])]

    return px.histogram(
        df,
        x="charges",
        log_y=log_y,
        title=run.name
    )

# ================================================================================================