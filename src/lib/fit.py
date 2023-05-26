import numpy as np
import streamlit as st
import scipy.stats as stats
import pandas as pd

from ROOT import TFile, TF1, TObject
from scipy.signal import find_peaks
from .run import Run, PeakType
from .plot import q_branch_to_dataframe

ROOT_CACHE_FILE_PATH = "/Users/andou/Documents/Pioneer/midas-stuff/streamlit_cache.root"

def _fit(histogram, center: float, percent_margin: float = 4):
    margin_as_decimal = float(percent_margin / 100)
    x_lower_bound, x_upper_bound = (center * (1 - margin_as_decimal), center * (1 + margin_as_decimal))
    histogram.Fit("gaus", "LQ0", "", x_lower_bound, x_upper_bound)
    f = histogram.GetFunction("gaus")
    f.ResetBit(TF1.kNotDraw)
    histogram.Write(histogram.GetName(), TObject.kOverwrite)

    return f.GetParameter(1)

def _single_mu(run: Run):
    t_file = TFile.Open(run.path)
    data = q_branch_to_dataframe(t_file)
    t_file.Close()
    histogram, bin_edges = np.histogram(data.charges.tolist(), bins=128)
    max_count_bin_index = np.argmax(histogram)

    mu_guess = (bin_edges[max_count_bin_index] + bin_edges[max_count_bin_index]) / 2
    return mu_guess

def _multi_mu(run: Run):
    t_file = TFile.Open(run.path)
    data: pd.DataFrame = q_branch_to_dataframe(t_file)
    t_file.Close()

    search_range = run.peak_search_range
    data = data[data.charges.between(left=search_range[0], right=search_range[1])]

    if len(data) <= 1:
        return None

    histogram, bin_edges = np.histogram(data.charges, bins=128, density=True)

    x_axis = np.linspace(bin_edges.min(), bin_edges.max(), 128)
    
    kde = stats.gaussian_kde(data.charges)
    kde_curve = kde.pdf(x_axis)

    peaks, _ = find_peaks(kde_curve)
    peak_coordinates = [(bin_edges[peak], histogram[peak]) for peak in peaks]
    peak_coordinates.sort(key=lambda coord: coord[1], reverse=True)
    two_peaks = peak_coordinates[0:2]

    return [coordinate[0] for coordinate in two_peaks]


def get_peaks(t_file: TFile, run: Run, force_cache: bool = False):
    if run.peak_type is PeakType.SINGLE:
        return _single_mu(run)
    else:
        return _multi_mu(run)
