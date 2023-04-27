import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ROOT import TFile


def _root_charge_histograms_to_dataframes(t_file, channels):
    histograms = [t_file.Get(f"channel_{channel}_histogram")
                  for channel in channels]
    dataframes = []
    for histogram in histograms:
        num_bins = histogram.GetNbinsX()
        bins = [histogram.GetBinCenter(i) for i in range(1, num_bins + 1)]
        values = [histogram.GetBinContent(i) for i in range(1, num_bins + 1)]
        dataframes.append(pd.DataFrame({"x": bins, "y": values}))

    return dataframes

def root_th1fs_to_plotly_histogram(
    path: str,
    plot_title: str,
    channels: set[int] = set(range(0, 16)),
    log_y: bool = False,
    translucent_bars: bool = False
    ):
    t_file = TFile.Open(path, 'r')

    dataframes = _root_charge_histograms_to_dataframes(t_file, channels)

    fig = go.Figure()

    for i, channel in enumerate(channels):
        fig.add_trace(go.Bar(x=dataframes[i]["x"],
                             y=dataframes[i]["y"],
                             name=f"Channel {channel}",
                             marker={"opacity": 0.65 if translucent_bars else 1}))

    fig.update_layout(
        barmode="overlay",
        title={
            "text": plot_title
        }
    )

    if log_y:
        fig.update_yaxes(type="log")

    return fig
