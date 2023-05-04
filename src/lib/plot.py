import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ROOT import TFile

# ================================================================================================
# Helper Functions
# -----

def _root_charge_histograms_to_dataframes(t_file, channels):
    histograms = [t_file.Get(f"channel_{channel}_histogram") for channel in channels]
    dataframes = []
    for histogram in histograms:
        num_bins = histogram.GetNbinsX()
        bins = [histogram.GetBinCenter(i) for i in range(1, num_bins + 1)]
        values = [histogram.GetBinContent(i) for i in range(1, num_bins + 1)]
        dataframes.append(pd.DataFrame({"x": bins, "y": values}))

    return dataframes

def _combine_channels(t_file, channels):
    histograms = [t_file.Get(f"channel_{channel}_histogram") for channel in channels]
    data = {}
    for histogram in histograms:
        num_bins = histogram.GetNbinsX()
        bins = [histogram.GetBinCenter(i) for i in range(1, num_bins + 1)]
        values = [histogram.GetBinContent(i) for i in range(1, num_bins + 1)]
        for bin, value in zip(bins, values):
            if not bin in data:
                data[bin] = value
            else:
                data[bin] += value

    formatted_data = { "x": [], "y": [] }
    for bin, value in data.items():
        formatted_data["x"].append(bin)
        formatted_data["y"].append(value)
    
    return pd.DataFrame(formatted_data)



# ================================================================================================
# Plotting Functions
# -----

def root_th1fs_to_plotly_histogram(
    path: str,
    plot_title: str,
    channels: set[int] = set(range(0, 16)),
    log_y: bool = False,
    translucent_bars: bool = False,
    superpose_channels: bool = False
):
    t_file = TFile.Open(path, 'r')

    if superpose_channels:
        dataframes = _combine_channels(t_file, channels)
    else:
        dataframes = _root_charge_histograms_to_dataframes(t_file, channels)

    fig = go.Figure()

    if superpose_channels:
        fig.add_trace(go.Bar(x=dataframes["x"],
                             y=dataframes["y"],
                             marker={ "opacity": 0.65 if translucent_bars else 1 }))
    else:
        for i, channel in enumerate(channels):
            fig.add_trace(go.Bar(x=dataframes[i]["x"],
                                y=dataframes[i]["y"],
                                name=f"Channel {channel}",
                                marker={ "opacity": 0.65 if translucent_bars else 1 }))

    fig.update_layout(
        barmode="overlay",
        title={
            "text": plot_title
        }
    )

    if log_y:
        fig.update_yaxes(type="log")

    return fig

# ================================================================================================

def run_overlay_plot(runs, channels: set[int], channels_string: str, log_y: bool = False, translucent_bars: bool = False):
    t_files = [TFile.Open(run[1], 'r') for run in runs]

    run_data = [pd.concat(_root_charge_histograms_to_dataframes(t_file, channels)) for t_file in t_files]

    fig = go.Figure()

    for run_data, run in zip(run_data, runs):
        fig.add_trace(go.Bar(x=run_data["x"],
                             y=run_data["y"],
                             name=run[0],
                             marker={"opacity": 0.65 if translucent_bars else 1}))
    
    runs_string = ", ".join([run[0] for run in runs])

    fig.update_layout(
        barmode="overlay",
        title={
            "text": f"Overlaying {runs_string} for ({channels_string})"
        }
    )

    if log_y:
        fig.update_yaxes(type="log")

    return fig