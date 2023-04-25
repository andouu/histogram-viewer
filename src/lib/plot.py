import streamlit as st
import plotly.express as px

from ROOT import TFile

def root_th1f_to_plotly_histogram(path: str, histogram_name: str, plot_title: str, log_y: bool = False):
    tfile = TFile.Open(path, 'r')
    histogram = tfile.Get(histogram_name)

    num_bins = histogram.GetNbinsX()
    x = [histogram.GetBinCenter(i) for i in range(1, num_bins)]
    y = [histogram.GetBinContent(i) for i in range(1, num_bins)]

    fig = px.bar(x=x, y=y, barmode="overlay", title=plot_title, log_y=log_y)

    return fig